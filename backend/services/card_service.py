"""
卡片服务层

本模块提供卡片相关的业务逻辑，包括：
- 获取列表下的所有卡片
- 创建新卡片
- 获取指定卡片
- 更新卡片
- 删除卡片
- 移动卡片（同列表内或跨列表）

需求：3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 4.1, 4.3, 5.3
"""

from datetime import datetime
from config import db
from models.card import Card
from models.list import List
from models.board import Board
from utils.exceptions import NotFoundError, ValidationError, ForbiddenError
from utils.validators import (
    validate_required_fields, 
    validate_non_empty_string, 
    validate_string_length, 
    validate_positive_integer,
    validate_type
)


def verify_card_ownership(card_id, user_id):
    """
    验证卡片是否属于指定用户（通过 list -> board -> user_id）
    
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    
    Args:
        card_id (int): 卡片 ID
        user_id (int): 用户 ID
        
    Raises:
        NotFoundError: 当卡片不存在时
        ForbiddenError: 当卡片所属看板不属于该用户时
    """
    card = Card.query.get(card_id)
    if not card:
        raise NotFoundError(
            "卡片不存在",
            details={'resource': 'card', 'id': card_id}
        )
    
    # 获取卡片所属的列表
    list_obj = List.query.get(card.list_id)
    if not list_obj:
        raise NotFoundError(
            "列表不存在",
            details={'resource': 'list', 'id': card.list_id}
        )
    
    # 获取列表所属的看板
    board = Board.query.get(list_obj.board_id)
    if not board:
        raise NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': list_obj.board_id}
        )
    
    # 验证看板属于该用户
    if board.user_id != user_id:
        raise ForbiddenError("无权访问该资源")


def get_cards_by_list_id(list_id):
    """
    获取列表下的所有卡片
    
    需求：3.1 - THE System SHALL 允许用户在列表中创建无限数量的卡片
    
    Args:
        list_id (int): 列表 ID
        
    Returns:
        list: 卡片对象的列表，按 position 排序
        
    Raises:
        NotFoundError: 当列表不存在时
    """
    # 验证列表是否存在
    list_obj = List.query.get(list_id)
    if not list_obj:
        raise NotFoundError(
            "列表不存在",
            details={'resource': 'list', 'id': list_id}
        )
    
    # 获取列表下的所有卡片，按位置排序
    cards = Card.query.filter_by(list_id=list_id).order_by(Card.position).all()
    return cards


def get_card_by_id(card_id, user_id=None):
    """
    根据 ID 获取指定卡片
    
    需求：3.6 - WHEN 用户单击卡片时，THE System SHALL 显示卡片详情界面
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    
    Args:
        card_id (int): 卡片 ID
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        Card: 卡片对象
        
    Raises:
        NotFoundError: 当卡片不存在时
        ForbiddenError: 当卡片所属看板不属于该用户时（如果提供了 user_id）
    """
    card = Card.query.get(card_id)
    if not card:
        raise NotFoundError(
            "卡片不存在",
            details={'resource': 'card', 'id': card_id}
        )
    
    # 如果提供了 user_id，验证卡片所属看板的所有权
    if user_id is not None:
        verify_card_ownership(card_id, user_id)
    
    return card


def create_card(list_id, data):
    """
    在列表中创建新卡片
    
    需求：3.1 - THE System SHALL 允许用户在列表中创建无限数量的卡片
    需求：3.2 - WHEN 用户点击"添加卡片"按钮时，THE System SHALL 创建新的卡片
    需求：3.3 - WHEN 用户创建卡片时，THE System SHALL 要求提供卡片标题
    需求：5.3 - WHEN 用户创建、修改或删除卡片时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        list_id (int): 列表 ID
        data (dict): 包含卡片信息的字典，必须包含 'title' 字段，可选 'position' 字段
        
    Returns:
        Card: 创建的卡片对象
        
    Raises:
        NotFoundError: 当列表不存在时
        ValidationError: 当输入数据无效时
    """
    # 验证列表是否存在
    list_obj = List.query.get(list_id)
    if not list_obj:
        raise NotFoundError(
            "列表不存在",
            details={'resource': 'list', 'id': list_id}
        )
    
    # 验证必需字段
    validate_required_fields(data, ['title'])
    
    # 验证卡片标题非空
    title = data['title']
    validate_non_empty_string(title, '卡片标题')
    
    # 验证卡片标题长度
    validate_string_length(title, '卡片标题', 255)
    
    # 获取位置（如果未提供，则设置为最后）
    position = data.get('position')
    if position is None:
        # 获取当前列表下的最大位置
        max_position = db.session.query(db.func.max(Card.position)).filter_by(list_id=list_id).scalar()
        position = (max_position + 1) if max_position is not None else 0
    else:
        validate_positive_integer(position, '位置')
    
    # 创建卡片对象
    card = Card(
        list_id=list_id,
        title=title.strip(),
        position=position
    )
    
    # 保存到数据库
    db.session.add(card)
    db.session.commit()
    
    return card


def update_card(card_id, data, user_id=None):
    """
    更新卡片信息
    
    需求：3.4 - THE System SHALL 允许用户编辑卡片标题
    需求：3.7 - THE System SHALL 允许用户在卡片详情中添加描述信息
    需求：3.8 - THE System SHALL 允许用户在卡片详情中添加截止日期
    需求：3.9 - THE System SHALL 允许用户在卡片详情中添加标签
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.3 - WHEN 用户创建、修改或删除卡片时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        card_id (int): 卡片 ID
        data (dict): 包含更新信息的字典，可以包含 'title', 'description', 'due_date', 'tags' 字段
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        Card: 更新后的卡片对象
        
    Raises:
        NotFoundError: 当卡片不存在时
        ForbiddenError: 当卡片所属看板不属于该用户时（如果提供了 user_id）
        ValidationError: 当输入数据无效时
    """
    # 获取卡片（如果提供了 user_id，会验证权限）
    card = get_card_by_id(card_id, user_id)
    
    # 更新标题（如果提供）
    if 'title' in data:
        title = data['title']
        validate_non_empty_string(title, '卡片标题')
        validate_string_length(title, '卡片标题', 255)
        card.title = title.strip()
    
    # 更新描述（如果提供）
    if 'description' in data:
        description = data['description']
        if description is not None:
            validate_type(description, '描述', str)
        card.description = description
    
    # 更新截止日期（如果提供）
    if 'due_date' in data:
        due_date = data['due_date']
        if due_date is not None:
            # 如果是字符串，尝试解析为日期
            if isinstance(due_date, str):
                try:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                except ValueError:
                    raise ValidationError(
                        "截止日期格式无效，应为 YYYY-MM-DD",
                        details={'field': 'due_date', 'constraint': 'date_format'}
                    )
        card.due_date = due_date
    
    # 更新标签（如果提供）
    if 'tags' in data:
        tags = data['tags']
        if tags is not None:
            validate_type(tags, '标签', list)
            # 验证标签列表中的每个元素都是字符串
            for i, tag in enumerate(tags):
                if not isinstance(tag, str):
                    raise ValidationError(
                        f"标签列表中的第 {i+1} 个元素必须是字符串",
                        details={'field': 'tags', 'constraint': 'element_type', 'index': i}
                    )
        card.tags = tags
    
    # 保存到数据库
    db.session.commit()
    
    return card


def delete_card(card_id, user_id=None):
    """
    删除卡片
    
    需求：3.5 - THE System SHALL 允许用户删除卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.3 - WHEN 用户创建、修改或删除卡片时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        card_id (int): 卡片 ID
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Raises:
        NotFoundError: 当卡片不存在时
        ForbiddenError: 当卡片所属看板不属于该用户时（如果提供了 user_id）
    """
    # 获取卡片（如果提供了 user_id，会验证权限）
    card = get_card_by_id(card_id, user_id)
    
    # 删除卡片
    db.session.delete(card)
    db.session.commit()


def move_card(card_id, data, user_id=None):
    """
    移动卡片到其他列表或改变位置
    
    需求：4.1 - THE System SHALL 允许用户在同一列表内拖拽卡片改变顺序
    需求：4.2 - WHEN 用户在列表内拖拽卡片时，THE System SHALL 实时更新卡片位置
    需求：4.3 - THE System SHALL 允许用户将卡片拖拽到不同的列表
    需求：4.4 - WHEN 用户将卡片拖拽到不同列表时，THE System SHALL 更新卡片所属的列表
    需求：4.5 - WHEN 拖拽操作完成时，THE System SHALL 持久化保存新的位置信息
    需求：5.4 - WHEN 用户拖拽列表或卡片时，THE System SHALL 立即将新位置保存到数据库
    
    Args:
        card_id (int): 卡片 ID
        data (dict): 包含移动信息的字典，必须包含 'list_id' 和 'position' 字段
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        Card: 更新后的卡片对象
        
    Raises:
        NotFoundError: 当卡片或目标列表不存在时
        ForbiddenError: 当卡片或目标列表所属看板不属于该用户时（如果提供了 user_id）
        ValidationError: 当输入数据无效时
    """
    # 获取卡片（如果提供了 user_id，会验证权限）
    card = get_card_by_id(card_id, user_id)
    
    # 验证必需字段
    validate_required_fields(data, ['list_id', 'position'])
    
    # 验证目标列表是否存在
    list_id = data['list_id']
    validate_positive_integer(list_id, '列表 ID')
    
    target_list = List.query.get(list_id)
    if not target_list:
        raise NotFoundError(
            "目标列表不存在",
            details={'resource': 'list', 'id': list_id}
        )
    
    # 如果提供了 user_id，验证目标列表所属看板的所有权
    if user_id is not None:
        target_board = Board.query.get(target_list.board_id)
        if not target_board:
            raise NotFoundError(
                "看板不存在",
                details={'resource': 'board', 'id': target_list.board_id}
            )
        if target_board.user_id != user_id:
            raise ForbiddenError("无权访问该资源")
    
    # 验证位置值
    position = data['position']
    validate_positive_integer(position, '位置')
    
    # 更新卡片的列表和位置
    card.list_id = list_id
    card.position = position
    
    # 保存到数据库
    db.session.commit()
    
    return card
