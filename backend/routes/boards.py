"""
看板路由

本模块定义看板相关的 RESTful API 端点：
- GET /api/boards - 获取所有看板
- POST /api/boards - 创建新看板
- GET /api/boards/:id - 获取指定看板
- PUT /api/boards/:id - 更新看板
- DELETE /api/boards/:id - 删除看板
- GET /api/boards/:id/lists - 获取看板下的所有列表
- POST /api/boards/:id/lists - 在看板中创建新列表

需求：1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 4.5, 6.1, 6.5, 6.6
"""

from flask import Blueprint, request, jsonify, g
from services import board_service, list_service
from utils.decorators import require_auth

boards_bp = Blueprint('boards', __name__)


@boards_bp.route('', methods=['GET'])
@require_auth
def get_boards():
    """
    获取当前用户的所有看板
    
    需求：1.3 - THE System SHALL 允许用户查看所有已创建的看板列表
    需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Returns:
        JSON: 包含当前用户所有看板的列表
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "boards": [
                {
                    "id": 1,
                    "name": "项目开发看板",
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T10:30:00"
                }
            ]
        }
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 只获取当前用户的看板
    boards = board_service.get_all_boards(user_id=user_id)
    return jsonify({
        'boards': [board.to_dict() for board in boards]
    }), 200


@boards_bp.route('', methods=['POST'])
@require_auth
def create_board():
    """
    创建新看板（自动关联到当前用户）
    
    需求：1.1 - THE System SHALL 允许用户创建新的看板
    需求：1.2 - WHEN 用户创建看板时，THE System SHALL 要求提供看板名称
    需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Request Body:
        {
            "name": "项目开发看板"
        }
    
    Returns:
        JSON: 创建的看板对象
        HTTP 状态码: 201 Created
        
    Response Example:
        {
            "id": 1,
            "name": "项目开发看板",
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }
        
    Raises:
        ValidationError: 当看板名称为空或无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 创建看板并自动关联到当前用户
    board = board_service.create_board(data, user_id=user_id)
    return jsonify(board.to_dict()), 201


@boards_bp.route('/<int:board_id>', methods=['GET'])
@require_auth
def get_board(board_id):
    """
    获取指定看板（验证看板属于当前用户）
    
    需求：1.3 - THE System SHALL 允许用户查看所有已创建的看板列表
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户，否则返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        board_id (int): 看板 ID
    
    Returns:
        JSON: 看板对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "name": "项目开发看板",
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }
        
    Raises:
        NotFoundError: 当看板不存在时（返回 404）
        ForbiddenError: 当看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 验证看板属于当前用户
    board = board_service.get_board_by_id(board_id, user_id=user_id)
    return jsonify(board.to_dict()), 200


@boards_bp.route('/<int:board_id>', methods=['PUT'])
@require_auth
def update_board(board_id):
    """
    更新看板信息（验证看板属于当前用户）
    
    需求：1.4 - THE System SHALL 允许用户编辑看板名称
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        board_id (int): 看板 ID
    
    Request Body:
        {
            "name": "更新后的看板名称"
        }
    
    Returns:
        JSON: 更新后的看板对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "name": "更新后的看板名称",
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T11:00:00"
        }
        
    Raises:
        NotFoundError: 当看板不存在时（返回 404）
        ForbiddenError: 当看板不属于当前用户时（返回 403）
        ValidationError: 当看板名称为空或无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 验证看板属于当前用户并更新
    board = board_service.update_board(board_id, data, user_id=user_id)
    return jsonify(board.to_dict()), 200


@boards_bp.route('/<int:board_id>', methods=['DELETE'])
@require_auth
def delete_board(board_id):
    """
    删除看板（验证看板属于当前用户）
    
    需求：1.5 - THE System SHALL 允许用户删除看板
    需求：1.6 - WHEN 用户删除看板时，THE System SHALL 同时删除该看板下的所有列表和卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        board_id (int): 看板 ID
    
    Returns:
        HTTP 状态码: 204 No Content
        
    Raises:
        NotFoundError: 当看板不存在时（返回 404）
        ForbiddenError: 当看板不属于当前用户时（返回 403）
        
    Note:
        删除看板时会自动级联删除其下的所有列表和卡片
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 验证看板属于当前用户并删除
    board_service.delete_board(board_id, user_id=user_id)
    return '', 204


@boards_bp.route('/<int:board_id>/lists', methods=['GET'])
@require_auth
def get_board_lists(board_id):
    """
    获取看板下的所有列表（验证看板属于当前用户）
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        board_id (int): 看板 ID
    
    Returns:
        JSON: 包含所有列表的列表，按 position 排序
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "lists": [
                {
                    "id": 1,
                    "board_id": 1,
                    "name": "待办事项",
                    "position": 0,
                    "created_at": "2024-01-15T10:35:00",
                    "updated_at": "2024-01-15T10:35:00"
                },
                {
                    "id": 2,
                    "board_id": 1,
                    "name": "进行中",
                    "position": 1,
                    "created_at": "2024-01-15T10:36:00",
                    "updated_at": "2024-01-15T10:36:00"
                }
            ]
        }
        
    Raises:
        NotFoundError: 当看板不存在时（返回 404）
        ForbiddenError: 当看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 验证看板属于当前用户并获取列表
    lists = list_service.get_lists_by_board_id(board_id, user_id=user_id)
    return jsonify({
        'lists': [list_obj.to_dict() for list_obj in lists]
    }), 200


@boards_bp.route('/<int:board_id>/lists', methods=['POST'])
@require_auth
def create_board_list(board_id):
    """
    在看板中创建新列表（验证看板属于当前用户）
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：2.2 - WHEN 用户创建列表时，THE System SHALL 要求提供列表名称
    需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        board_id (int): 看板 ID
    
    Request Body:
        {
            "name": "待办事项",
            "position": 0  // 可选，如果不提供则自动设置为最后
        }
    
    Returns:
        JSON: 创建的列表对象
        HTTP 状态码: 201 Created
        
    Response Example:
        {
            "id": 1,
            "board_id": 1,
            "name": "待办事项",
            "position": 0,
            "created_at": "2024-01-15T10:35:00",
            "updated_at": "2024-01-15T10:35:00"
        }
        
    Raises:
        NotFoundError: 当看板不存在时（返回 404）
        ForbiddenError: 当看板不属于当前用户时（返回 403）
        ValidationError: 当列表名称为空或无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 验证看板属于当前用户并创建列表
    list_obj = list_service.create_list(board_id, data, user_id=user_id)
    return jsonify(list_obj.to_dict()), 201
