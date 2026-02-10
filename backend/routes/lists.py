"""
列表路由

本模块定义列表相关的 RESTful API 端点：
- GET /api/boards/:boardId/lists - 获取看板下的所有列表
- POST /api/boards/:boardId/lists - 在看板中创建新列表
- GET /api/lists/:id - 获取指定列表
- PUT /api/lists/:id - 更新列表
- DELETE /api/lists/:id - 删除列表
- PUT /api/lists/:id/position - 更新列表位置
- GET /api/lists/:id/cards - 获取列表下的所有卡片
- POST /api/lists/:id/cards - 在列表中创建新卡片

需求：2.1, 2.2, 2.3, 2.4, 2.6, 3.1, 3.2, 4.1-4.5, 6.1, 6.5, 6.6
"""

from flask import Blueprint, request, jsonify, g
from services import list_service, card_service
from utils.decorators import require_auth

lists_bp = Blueprint('lists', __name__)


@lists_bp.route('/<int:list_id>', methods=['GET'])
@require_auth
def get_list(list_id):
    """
    获取指定列表（通过 board_id 验证用户权限）
    
    需求：2.1 - THE System SHALL 允许用户在看板中添加无限数量的工作列表
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Returns:
        JSON: 列表对象
        HTTP 状态码: 200 OK
        
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
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 通过 board_id 验证用户权限
    list_obj = list_service.get_list_by_id(list_id, user_id=user_id)
    return jsonify(list_obj.to_dict()), 200


@lists_bp.route('/<int:list_id>', methods=['PUT'])
@require_auth
def update_list(list_id):
    """
    更新列表信息（通过 board_id 验证用户权限）
    
    需求：2.3 - THE System SHALL 允许用户自定义列表的名称
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Request Body:
        {
            "name": "更新后的列表名称"
        }
    
    Returns:
        JSON: 更新后的列表对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "board_id": 1,
            "name": "更新后的列表名称",
            "position": 0,
            "created_at": "2024-01-15T10:35:00",
            "updated_at": "2024-01-15T11:00:00"
        }
        
    Raises:
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
        ValidationError: 当列表名称为空或无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 通过 board_id 验证用户权限并更新
    list_obj = list_service.update_list(list_id, data, user_id=user_id)
    return jsonify(list_obj.to_dict()), 200


@lists_bp.route('/<int:list_id>', methods=['DELETE'])
@require_auth
def delete_list(list_id):
    """
    删除列表（通过 board_id 验证用户权限）
    
    需求：2.4 - THE System SHALL 允许用户删除列表
    需求：2.5 - WHEN 用户删除列表时，THE System SHALL 同时删除该列表下的所有卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Returns:
        HTTP 状态码: 204 No Content
        
    Raises:
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
        
    Note:
        删除列表时会自动级联删除其下的所有卡片
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 通过 board_id 验证用户权限并删除
    list_service.delete_list(list_id, user_id=user_id)
    return '', 204


@lists_bp.route('/<int:list_id>/position', methods=['PUT'])
@require_auth
def update_list_position(list_id):
    """
    更新列表位置（通过 board_id 验证用户权限）
    
    需求：2.6 - THE System SHALL 允许用户通过拖拽重新排列列表的顺序
    需求：2.7 - WHEN 用户拖拽列表时，THE System SHALL 实时更新列表的位置
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Request Body:
        {
            "position": 2
        }
    
    Returns:
        JSON: 更新后的列表对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "board_id": 1,
            "name": "待办事项",
            "position": 2,
            "created_at": "2024-01-15T10:35:00",
            "updated_at": "2024-01-15T10:40:00"
        }
        
    Raises:
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
        ValidationError: 当位置值无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 通过 board_id 验证用户权限并更新位置
    list_obj = list_service.update_list_position(list_id, data, user_id=user_id)
    return jsonify(list_obj.to_dict()), 200


@lists_bp.route('/<int:list_id>/cards', methods=['GET'])
@require_auth
def get_list_cards(list_id):
    """
    获取列表下的所有卡片（通过 board_id 验证用户权限）
    
    需求：3.1 - THE System SHALL 允许用户在列表中创建无限数量的卡片
    需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Returns:
        JSON: 包含所有卡片的列表，按 position 排序
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "cards": [
                {
                    "id": 1,
                    "list_id": 1,
                    "title": "实现用户登录功能",
                    "description": null,
                    "due_date": null,
                    "tags": [],
                    "position": 0,
                    "created_at": "2024-01-15T10:45:00",
                    "updated_at": "2024-01-15T10:45:00"
                },
                {
                    "id": 2,
                    "list_id": 1,
                    "title": "编写单元测试",
                    "description": "测试登录功能",
                    "due_date": "2024-01-22",
                    "tags": ["测试"],
                    "position": 1,
                    "created_at": "2024-01-15T10:46:00",
                    "updated_at": "2024-01-15T10:46:00"
                }
            ]
        }
        
    Raises:
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 首先验证列表所属看板的权限
    list_service.get_list_by_id(list_id, user_id=user_id)
    
    # 获取列表下的所有卡片
    cards = card_service.get_cards_by_list_id(list_id)
    return jsonify({
        'cards': [card.to_dict() for card in cards]
    }), 200


@lists_bp.route('/<int:list_id>/cards', methods=['POST'])
@require_auth
def create_list_card(list_id):
    """
    在列表中创建新卡片（通过 board_id 验证用户权限）
    
    需求：3.1 - THE System SHALL 允许用户在列表中创建无限数量的卡片
    需求：3.2 - WHEN 用户点击"添加卡片"按钮时，THE System SHALL 创建新的卡片
    需求：3.3 - WHEN 用户创建卡片时，THE System SHALL 要求提供卡片标题
    需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        list_id (int): 列表 ID
    
    Request Body:
        {
            "title": "实现用户登录功能",
            "position": 0  // 可选，如果不提供则自动设置为最后
        }
    
    Returns:
        JSON: 创建的卡片对象
        HTTP 状态码: 201 Created
        
    Response Example:
        {
            "id": 1,
            "list_id": 1,
            "title": "实现用户登录功能",
            "description": null,
            "due_date": null,
            "tags": [],
            "position": 0,
            "created_at": "2024-01-15T10:45:00",
            "updated_at": "2024-01-15T10:45:00"
        }
        
    Raises:
        NotFoundError: 当列表不存在时（返回 404）
        ForbiddenError: 当列表所属看板不属于当前用户时（返回 403）
        ValidationError: 当卡片标题为空或无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 首先验证列表所属看板的权限
    list_service.get_list_by_id(list_id, user_id=user_id)
    
    data = request.get_json()
    
    # 创建卡片
    card = card_service.create_card(list_id, data)
    return jsonify(card.to_dict()), 201
