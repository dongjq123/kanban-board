"""
看板服务层

本模块提供看板相关的业务逻辑，包括：
- 获取所有看板
- 创建新看板
- 获取指定看板
- 更新看板
- 删除看板

需求：1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1
"""

from config import db
from models.board import Board
from utils.exceptions import NotFoundError, ValidationError, ForbiddenError
from utils.validators import validate_required_fields, validate_non_empty_string, validate_string_length


def get_all_boards(user_id=None):
    """
    获取所有看板（如果提供 user_id，则只返回该用户的看板）
    
    需求：1.3 - THE System SHALL 允许用户查看所有已创建的看板列表
    需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
    
    Args:
        user_id (int, optional): 用户 ID，如果提供则只返回该用户的看板
    
    Returns:
        list: 看板对象的列表
    """
    query = Board.query
    
    # 如果提供了 user_id，则只返回该用户的看板
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    
    boards = query.order_by(Board.created_at.desc()).all()
    return boards


def get_board_by_id(board_id, user_id=None):
    """
    根据 ID 获取指定看板（如果提供 user_id，则验证看板属于该用户）
    
    需求：1.3 - THE System SHALL 允许用户查看所有已创建的看板列表
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户，否则返回"无权访问"错误
    
    Args:
        board_id (int): 看板 ID
        user_id (int, optional): 用户 ID，如果提供则验证看板属于该用户
        
    Returns:
        Board: 看板对象
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于指定用户时
    """
    board = Board.query.get(board_id)
    if not board:
        raise NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': board_id}
        )
    
    # 如果提供了 user_id，验证看板属于该用户
    if user_id is not None and board.user_id != user_id:
        raise ForbiddenError("无权访问该看板")
    
    return board


def create_board(data, user_id=None):
    """
    创建新看板
    
    需求：1.1 - THE System SHALL 允许用户创建新的看板
    需求：1.2 - WHEN 用户创建看板时，THE System SHALL 要求提供看板名称
    需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
    需求：5.1 - WHEN 用户创建、修改或删除看板时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        data (dict): 包含看板信息的字典，必须包含 'name' 字段
        user_id (int, optional): 用户 ID，如果提供则自动关联到该用户
        
    Returns:
        Board: 创建的看板对象
        
    Raises:
        ValidationError: 当输入数据无效时
    """
    # 验证必需字段
    validate_required_fields(data, ['name'])
    
    # 验证看板名称非空
    name = data['name']
    validate_non_empty_string(name, '看板名称')
    
    # 验证看板名称长度
    validate_string_length(name, '看板名称', 255)
    
    # 创建看板对象
    board = Board(name=name.strip())
    
    # 如果提供了 user_id，自动关联到该用户
    if user_id is not None:
        board.user_id = user_id
    
    # 保存到数据库
    db.session.add(board)
    db.session.commit()
    
    return board


def update_board(board_id, data, user_id=None):
    """
    更新看板信息
    
    需求：1.4 - THE System SHALL 允许用户编辑看板名称
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.1 - WHEN 用户创建、修改或删除看板时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        board_id (int): 看板 ID
        data (dict): 包含更新信息的字典，可以包含 'name' 字段
        user_id (int, optional): 用户 ID，如果提供则验证看板属于该用户
        
    Returns:
        Board: 更新后的看板对象
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于指定用户时
        ValidationError: 当输入数据无效时
    """
    # 获取看板（如果提供了 user_id，会验证权限）
    board = get_board_by_id(board_id, user_id)
    
    # 更新名称（如果提供）
    if 'name' in data:
        name = data['name']
        validate_non_empty_string(name, '看板名称')
        validate_string_length(name, '看板名称', 255)
        board.name = name.strip()
    
    # 保存到数据库
    db.session.commit()
    
    return board


def delete_board(board_id, user_id=None):
    """
    删除看板
    
    需求：1.5 - THE System SHALL 允许用户删除看板
    需求：1.6 - WHEN 用户删除看板时，THE System SHALL 同时删除该看板下的所有列表和卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.1 - WHEN 用户创建、修改或删除看板时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        board_id (int): 看板 ID
        user_id (int, optional): 用户 ID，如果提供则验证看板属于该用户
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于指定用户时
        
    Note:
        由于 Board 模型配置了 cascade='all, delete-orphan'，
        删除看板时会自动级联删除其下的所有列表和卡片
    """
    # 获取看板（如果提供了 user_id，会验证权限）
    board = get_board_by_id(board_id, user_id)
    
    # 删除看板（级联删除列表和卡片）
    db.session.delete(board)
    db.session.commit()
