"""
卡片路由

本模块定义卡片相关的 RESTful API 端点：
- GET /api/lists/:listId/cards - 获取列表下的所有卡片
- POST /api/lists/:listId/cards - 在列表中创建新卡片
- GET /api/cards/:id - 获取指定卡片
- PUT /api/cards/:id - 更新卡片
- DELETE /api/cards/:id - 删除卡片
- PUT /api/cards/:id/move - 移动卡片到其他列表或改变位置

需求：3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 4.1, 4.3, 4.4, 4.5, 6.1, 6.5, 6.6
"""

from flask import Blueprint, request, jsonify, g
from services import card_service
from utils.decorators import require_auth

cards_bp = Blueprint('cards', __name__)


@cards_bp.route('/<int:card_id>', methods=['GET'])
@require_auth
def get_card(card_id):
    """
    获取指定卡片（通过 list -> board 验证用户权限）
    
    需求：3.6 - WHEN 用户单击卡片时，THE System SHALL 显示卡片详情界面
    需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        card_id (int): 卡片 ID
    
    Returns:
        JSON: 卡片对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "list_id": 1,
            "title": "实现用户登录功能",
            "description": "使用 JWT 实现用户认证",
            "due_date": "2024-01-20",
            "tags": ["后端", "高优先级"],
            "position": 0,
            "created_at": "2024-01-15T10:45:00",
            "updated_at": "2024-01-15T10:50:00"
        }
        
    Raises:
        NotFoundError: 当卡片不存在时（返回 404）
        ForbiddenError: 当卡片所属看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 通过 list -> board 验证用户权限
    card = card_service.get_card_by_id(card_id, user_id=user_id)
    return jsonify(card.to_dict()), 200


@cards_bp.route('/<int:card_id>', methods=['PUT'])
@require_auth
def update_card(card_id):
    """
    更新卡片信息（通过 list -> board 验证用户权限）
    
    需求：3.4 - THE System SHALL 允许用户编辑卡片标题
    需求：3.7 - THE System SHALL 允许用户在卡片详情中添加描述信息
    需求：3.8 - THE System SHALL 允许用户在卡片详情中添加截止日期
    需求：3.9 - THE System SHALL 允许用户在卡片详情中添加标签
    需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        card_id (int): 卡片 ID
    
    Request Body:
        {
            "title": "实现用户登录功能",  // 可选
            "description": "使用 JWT 实现用户认证",  // 可选
            "due_date": "2024-01-20",  // 可选，格式 YYYY-MM-DD
            "tags": ["后端", "高优先级"]  // 可选
        }
    
    Returns:
        JSON: 更新后的卡片对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "list_id": 1,
            "title": "实现用户登录功能",
            "description": "使用 JWT 实现用户认证",
            "due_date": "2024-01-20",
            "tags": ["后端", "高优先级"],
            "position": 0,
            "created_at": "2024-01-15T10:45:00",
            "updated_at": "2024-01-15T10:50:00"
        }
        
    Raises:
        NotFoundError: 当卡片不存在时（返回 404）
        ForbiddenError: 当卡片所属看板不属于当前用户时（返回 403）
        ValidationError: 当输入数据无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 通过 list -> board 验证用户权限并更新
    card = card_service.update_card(card_id, data, user_id=user_id)
    return jsonify(card.to_dict()), 200


@cards_bp.route('/<int:card_id>', methods=['DELETE'])
@require_auth
def delete_card(card_id):
    """
    删除卡片（通过 list -> board 验证用户权限）
    
    需求：3.5 - THE System SHALL 允许用户删除卡片
    需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        card_id (int): 卡片 ID
    
    Returns:
        HTTP 状态码: 204 No Content
        
    Raises:
        NotFoundError: 当卡片不存在时（返回 404）
        ForbiddenError: 当卡片所属看板不属于当前用户时（返回 403）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 通过 list -> board 验证用户权限并删除
    card_service.delete_card(card_id, user_id=user_id)
    return '', 204


@cards_bp.route('/<int:card_id>/move', methods=['PUT'])
@require_auth
def move_card(card_id):
    """
    移动卡片到其他列表或改变位置（验证源和目标看板权限）
    
    需求：4.1 - THE System SHALL 允许用户在同一列表内拖拽卡片改变顺序
    需求：4.2 - WHEN 用户在列表内拖拽卡片时，THE System SHALL 实时更新卡片位置
    需求：4.3 - THE System SHALL 允许用户将卡片拖拽到不同的列表
    需求：4.4 - WHEN 用户将卡片拖拽到不同列表时，THE System SHALL 更新卡片所属的列表
    需求：4.5 - WHEN 拖拽操作完成时，THE System SHALL 持久化保存新的位置信息
    需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    需求：6.2 - THE System SHALL 使用 JSON 格式进行数据交换
    需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
    需求：6.6 - THE API SHALL 返回标准的 HTTP 状态码表示操作结果
    
    Args:
        card_id (int): 卡片 ID
    
    Request Body:
        {
            "list_id": 2,  // 目标列表 ID（可以是同一列表或不同列表）
            "position": 1  // 新位置
        }
    
    Returns:
        JSON: 更新后的卡片对象
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "id": 1,
            "list_id": 2,
            "title": "实现用户登录功能",
            "description": "使用 JWT 实现用户认证",
            "due_date": "2024-01-20",
            "tags": ["后端", "高优先级"],
            "position": 1,
            "created_at": "2024-01-15T10:45:00",
            "updated_at": "2024-01-15T11:00:00"
        }
        
    Raises:
        NotFoundError: 当卡片或目标列表不存在时（返回 404）
        ForbiddenError: 当卡片或目标列表所属看板不属于当前用户时（返回 403）
        ValidationError: 当输入数据无效时（返回 400）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    data = request.get_json()
    
    # 验证源和目标看板权限并移动卡片
    card = card_service.move_card(card_id, data, user_id=user_id)
    return jsonify(card.to_dict()), 200
