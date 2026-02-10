"""
列表服务层

本模块提供列表相关的业务逻辑，包括：
- 获取看板下的所有列表
- 创建新列表
- 获取指定列表
- 更新列表
- 删除列表
- 更新列表位置

需求：2.1, 2.2, 2.3, 2.4, 2.6, 5.2
"""

from config import db
from models.list import List
from models.board import Board
from utils.exceptions import NotFoundError, ValidationError, ForbiddenError
from utils.validators import validate_required_fields, validate_non_empty_string, validate_string_length, validate_positive_integer


def verify_board_ownership(board_id, user_id):
    """
    验证看板是否属于指定用户
    
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    
    Args:
        board_id (int): 看板 ID
        user_id (int): 用户 ID
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于该用户时
    """
    board = Board.query.get(board_id)
    if not board:
        raise NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': board_id}
        )
    
    if board.user_id != user_id:
        raise ForbiddenError("无权访问该资源")


def get_lists_by_board_id(board_id, user_id=None):
    """
    获取看板下的所有列表
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
    
    Args:
        board_id (int): 看板 ID
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        list: 列表对象的列表，按 position 排序
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于该用户时（如果提供了 user_id）
    """
    # 验证看板是否存在
    board = Board.query.get(board_id)
    if not board:
        raise NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': board_id}
        )
    
    # 如果提供了 user_id，验证看板所有权
    if user_id is not None:
        verify_board_ownership(board_id, user_id)
    
    # 获取看板下的所有列表，按位置排序
    lists = List.query.filter_by(board_id=board_id).order_by(List.position).all()
    return lists


def get_list_by_id(list_id, user_id=None):
    """
    根据 ID 获取指定列表
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    
    Args:
        list_id (int): 列表 ID
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        List: 列表对象
        
    Raises:
        NotFoundError: 当列表不存在时
        ForbiddenError: 当列表所属看板不属于该用户时（如果提供了 user_id）
    """
    list_obj = List.query.get(list_id)
    if not list_obj:
        raise NotFoundError(
            "列表不存在",
            details={'resource': 'list', 'id': list_id}
        )
    
    # 如果提供了 user_id，验证看板所有权
    if user_id is not None:
        verify_board_ownership(list_obj.board_id, user_id)
    
    return list_obj


def create_list(board_id, data, user_id=None):
    """
    在看板中创建新列表
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：2.2 - WHEN 用户创建列表时，THE System SHALL 要求提供列表名称
    需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
    需求：5.2 - WHEN 用户创建、修改或删除列表时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        board_id (int): 看板 ID
        data (dict): 包含列表信息的字典，必须包含 'name' 字段，可选 'position' 字段
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        List: 创建的列表对象
        
    Raises:
        NotFoundError: 当看板不存在时
        ForbiddenError: 当看板不属于该用户时（如果提供了 user_id）
        ValidationError: 当输入数据无效时
    """
    # 验证看板是否存在
    board = Board.query.get(board_id)
    if not board:
        raise NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': board_id}
        )
    
    # 如果提供了 user_id，验证看板所有权
    if user_id is not None:
        verify_board_ownership(board_id, user_id)
    
    # 验证必需字段
    validate_required_fields(data, ['name'])
    
    # 验证列表名称非空
    name = data['name']
    validate_non_empty_string(name, '列表名称')
    
    # 验证列表名称长度
    validate_string_length(name, '列表名称', 255)
    
    # 获取位置（如果未提供，则设置为最后）
    position = data.get('position')
    if position is None:
        # 获取当前看板下的最大位置
        max_position = db.session.query(db.func.max(List.position)).filter_by(board_id=board_id).scalar()
        position = (max_position + 1) if max_position is not None else 0
    else:
        validate_positive_integer(position, '位置')
    
    # 创建列表对象
    list_obj = List(
        board_id=board_id,
        name=name.strip(),
        position=position
    )
    
    # 保存到数据库
    db.session.add(list_obj)
    db.session.commit()
    
    return list_obj


def update_list(list_id, data, user_id=None):
    """
    更新列表信息
    
    需求：2.3 - THE System SHALL 允许用户自定义列表的名称
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.2 - WHEN 用户创建、修改或删除列表时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        list_id (int): 列表 ID
        data (dict): 包含更新信息的字典，可以包含 'name' 字段
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        List: 更新后的列表对象
        
    Raises:
        NotFoundError: 当列表不存在时
        ForbiddenError: 当列表所属看板不属于该用户时（如果提供了 user_id）
        ValidationError: 当输入数据无效时
    """
    # 获取列表
    list_obj = get_list_by_id(list_id, user_id)
    
    # 更新名称（如果提供）
    if 'name' in data:
        name = data['name']
        validate_non_empty_string(name, '列表名称')
        validate_string_length(name, '列表名称', 255)
        list_obj.name = name.strip()
    
    # 保存到数据库
    db.session.commit()
    
    return list_obj


def delete_list(list_id, user_id=None):
    """
    删除列表
    
    需求：2.4 - THE System SHALL 允许用户删除列表
    需求：2.5 - WHEN 用户删除列表时，THE System SHALL 同时删除该列表下的所有卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.2 - WHEN 用户创建、修改或删除列表时，THE System SHALL 立即将变更保存到数据库
    
    Args:
        list_id (int): 列表 ID
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Raises:
        NotFoundError: 当列表不存在时
        ForbiddenError: 当列表所属看板不属于该用户时（如果提供了 user_id）
        
    Note:
        由于 List 模型配置了 cascade='all, delete-orphan'，
        删除列表时会自动级联删除其下的所有卡片
    """
    # 获取列表
    list_obj = get_list_by_id(list_id, user_id)
    
    # 删除列表（级联删除卡片）
    db.session.delete(list_obj)
    db.session.commit()


def update_list_position(list_id, data, user_id=None):
    """
    更新列表位置
    
    需求：2.6 - THE System SHALL 允许用户通过拖拽重新排列列表的顺序
    需求：2.7 - WHEN 用户拖拽列表时，THE System SHALL 实时更新列表的位置
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：5.4 - WHEN 用户拖拽列表或卡片时，THE System SHALL 立即将新位置保存到数据库
    
    Args:
        list_id (int): 列表 ID
        data (dict): 包含位置信息的字典，必须包含 'position' 字段
        user_id (int, optional): 用户 ID，如果提供则验证权限
        
    Returns:
        List: 更新后的列表对象
        
    Raises:
        NotFoundError: 当列表不存在时
        ForbiddenError: 当列表所属看板不属于该用户时（如果提供了 user_id）
        ValidationError: 当输入数据无效时
    """
    # 获取列表
    list_obj = get_list_by_id(list_id, user_id)
    
    # 验证必需字段
    validate_required_fields(data, ['position'])
    
    # 验证位置值
    position = data['position']
    validate_positive_integer(position, '位置')
    
    # 更新位置
    list_obj.position = position
    
    # 保存到数据库
    db.session.commit()
    
    return list_obj
