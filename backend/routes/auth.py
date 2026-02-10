"""
认证路由

本模块定义认证相关的 RESTful API 端点：
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/auth/verify - 验证令牌

需求：1.1-1.6, 2.1-2.6, 3.1-3.4
"""

from flask import Blueprint, request, jsonify, current_app, g
from services.auth_service import AuthService
from utils.decorators import require_auth
from models.user import User

auth_bp = Blueprint('auth', __name__)


def get_auth_service():
    """
    获取 AuthService 实例
    
    Returns:
        AuthService: 认证服务实例
    """
    return AuthService(
        secret_key=current_app.config['SECRET_KEY'],
        token_expiration_hours=24
    )


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    需求：1.1 - WHEN 用户提交有效的注册信息 THEN 认证系统 SHALL 创建新用户账户
    需求：1.2 - WHEN 用户提交的用户名已存在 THEN 认证系统 SHALL 拒绝注册
    需求：1.3 - WHEN 用户提交的邮箱已存在 THEN 认证系统 SHALL 拒绝注册
    需求：1.4 - WHEN 用户提交的密码长度少于 8 个字符 THEN 认证系统 SHALL 拒绝注册
    需求：1.5 - WHEN 用户提交的邮箱格式无效 THEN 认证系统 SHALL 拒绝注册
    需求：1.6 - WHEN 创建新用户账户 THEN 认证系统 SHALL 使用 bcrypt 算法加密存储密码
    
    Request Body:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123"
        }
    
    Returns:
        JSON: 注册成功消息和用户信息
        HTTP 状态码: 201 Created
        
    Response Example:
        {
            "message": "注册成功",
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T00:00:00"
            }
        }
        
    Raises:
        ValidationError: 当验证失败时（返回 400）
    """
    data = request.get_json()
    
    # 提取请求数据
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # 调用 AuthService 注册用户
    auth_service = get_auth_service()
    user = auth_service.register_user(username, email, password)
    
    # 返回成功响应
    return jsonify({
        'message': '注册成功',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    需求：2.1 - WHEN 用户使用有效的邮箱和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
    需求：2.2 - WHEN 用户使用有效的用户名和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
    需求：2.3 - WHEN 用户提交的邮箱或用户名不存在 THEN 认证系统 SHALL 返回"用户名或密码错误"
    需求：2.4 - WHEN 用户提交的密码不正确 THEN 认证系统 SHALL 返回"用户名或密码错误"
    需求：2.5 - WHEN 用户成功登录 THEN 认证系统 SHALL 生成包含用户 ID 和过期时间的 JWT 令牌
    需求：2.6 - WHEN 生成 JWT 令牌 THEN 认证系统 SHALL 设置令牌有效期为 24 小时
    
    Request Body:
        {
            "identifier": "john_doe",  // 邮箱或用户名
            "password": "password123"
        }
    
    Returns:
        JSON: JWT 令牌和用户信息
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        
    Raises:
        AuthenticationError: 当认证失败时（返回 401）
    """
    data = request.get_json()
    
    # 提取请求数据
    identifier = data.get('identifier')
    password = data.get('password')
    
    # 调用 AuthService 验证用户
    auth_service = get_auth_service()
    user = auth_service.authenticate_user(identifier, password)
    
    # 生成 JWT 令牌
    token = auth_service.generate_token(user.id)
    
    # 返回成功响应
    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/verify', methods=['GET'])
@require_auth
def verify():
    """
    验证令牌
    
    需求：3.1 - WHEN 用户发送包含有效会话令牌的请求 THEN 认证系统 SHALL 验证令牌并允许访问
    需求：3.2 - WHEN 用户发送包含过期会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
    需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
    需求：3.4 - WHEN 用户发送不包含会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        JSON: 验证结果和用户信息
        HTTP 状态码: 200 OK
        
    Response Example:
        {
            "valid": true,
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        
    Raises:
        UnauthorizedError: 当令牌缺失时（返回 401）
        TokenExpiredError: 当令牌过期时（返回 401）
        InvalidTokenError: 当令牌无效时（返回 401）
    """
    # 从 g 对象获取当前用户 ID（由 @require_auth 装饰器设置）
    user_id = g.current_user_id
    
    # 查询用户信息
    user = User.query.get(user_id)
    
    if not user:
        # 用户不存在（理论上不应该发生，因为令牌已验证）
        from utils.exceptions import NotFoundError
        raise NotFoundError("用户不存在")
    
    # 返回验证成功响应
    return jsonify({
        'valid': True,
        'user': user.to_dict()
    }), 200
