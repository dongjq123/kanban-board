"""
认证装饰器模块

本模块提供 Flask 路由装饰器，用于保护需要认证的 API 端点。

需求：3.1-3.4, 6.1-6.4
"""

from functools import wraps
from flask import request, g, current_app
from utils.exceptions import UnauthorizedError


def require_auth(f):
    """
    Flask 路由装饰器，要求请求包含有效的 JWT 令牌
    
    需求：3.1 - WHEN 用户发送包含有效会话令牌的请求 THEN 认证系统 SHALL 验证令牌并允许访问
    需求：3.2 - WHEN 用户发送包含过期会话令牌的请求 THEN 认证系统 SHALL 拒绝访问并返回"令牌已过期"错误
    需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问并返回"令牌无效"错误
    需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
    需求：6.1 - WHEN API 端点被标记为需要认证 THEN API 权限验证器 SHALL 验证请求中的会话令牌
    需求：6.2 - WHEN API 请求包含有效的会话令牌 THEN API 权限验证器 SHALL 提取用户信息并允许访问
    需求：6.3 - WHEN API 请求不包含会话令牌 THEN API 权限验证器 SHALL 返回 401 未授权错误
    需求：6.4 - WHEN API 请求包含无效或过期的会话令牌 THEN API 权限验证器 SHALL 返回 401 未授权错误
    
    使用方式：
        @app.route('/api/boards')
        @require_auth
        def get_boards():
            user_id = g.current_user_id  # 从 g 对象获取当前用户 ID
            ...
    
    行为：
        - 从 Authorization header 提取 Bearer token
        - 验证 token 有效性
        - 将 user_id 存储到 flask.g.current_user_id
        - 如果验证失败，抛出相应的异常（由错误处理器处理）
    
    Args:
        f: 被装饰的路由函数
    
    Returns:
        装饰后的函数
    
    Raises:
        UnauthorizedError: 如果请求不包含 Authorization header 或格式错误
        TokenExpiredError: 如果令牌已过期
        InvalidTokenError: 如果令牌无效
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 延迟导入以避免循环依赖
        from services.auth_service import AuthService
        
        # 从请求头获取 Authorization header
        auth_header = request.headers.get('Authorization')
        
        # 需求：3.4, 6.3 - 检查是否包含 Authorization header
        if not auth_header:
            raise UnauthorizedError("未授权，请先登录")
        
        # 检查 Authorization header 格式是否为 "Bearer <token>"
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise UnauthorizedError("Authorization header 格式错误，应为 'Bearer <token>'")
        
        token = parts[1]
        
        # 创建 AuthService 实例
        auth_service = AuthService(
            secret_key=current_app.config['SECRET_KEY'],
            token_expiration_hours=24
        )
        
        # 验证令牌并提取用户 ID
        # 需求：3.1, 3.2, 3.3, 6.2, 6.4 - 验证令牌有效性
        # 如果令牌过期或无效，verify_token 会抛出相应的异常
        user_id = auth_service.verify_token(token)
        
        # 需求：6.2 - 将用户 ID 存储到 flask.g.current_user_id
        g.current_user_id = user_id
        
        # 调用原始路由函数
        return f(*args, **kwargs)
    
    return decorated_function
