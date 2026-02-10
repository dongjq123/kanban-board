"""
认证装饰器测试

本模块测试 require_auth 装饰器的功能，包括：
- 有效令牌允许访问
- 无效令牌拒绝访问
- 缺失令牌拒绝访问
- 过期令牌拒绝访问
- 用户 ID 正确存储到 g.current_user_id

需求：3.1-3.4, 6.1-6.4
"""

import pytest
from flask import Flask, g, jsonify
from utils.decorators import require_auth
from utils.exceptions import UnauthorizedError, InvalidTokenError, TokenExpiredError
from services.auth_service import AuthService
from models.user import User
from config import db
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def test_app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_client(test_app):
    """创建测试客户端"""
    return test_app.test_client()


@pytest.fixture
def auth_service(test_app):
    """创建认证服务实例"""
    with test_app.app_context():
        return AuthService(
            secret_key=test_app.config['SECRET_KEY'],
            token_expiration_hours=24
        )


@pytest.fixture
def test_user(test_app):
    """创建测试用户"""
    with test_app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        # 刷新以获取 ID
        db.session.refresh(user)
        user_id = user.id
        return user_id


@pytest.fixture
def valid_token(auth_service, test_user):
    """生成有效的 JWT 令牌"""
    return auth_service.generate_token(test_user)


@pytest.fixture
def expired_token(test_app, test_user):
    """生成过期的 JWT 令牌"""
    with test_app.app_context():
        # 创建一个已经过期的令牌（过期时间设置为 1 小时前）
        expiration = datetime.utcnow() - timedelta(hours=1)
        payload = {
            'user_id': test_user,
            'exp': expiration,
            'iat': datetime.utcnow() - timedelta(hours=2)
        }
        token = jwt.encode(payload, test_app.config['SECRET_KEY'], algorithm='HS256')
        return token


@pytest.fixture
def invalid_token():
    """生成无效的 JWT 令牌"""
    return 'invalid.token.string'


def test_require_auth_with_valid_token(test_app, test_client, valid_token, test_user):
    """
    测试：有效令牌允许访问
    
    需求：3.1 - WHEN 用户发送包含有效会话令牌的请求 THEN 认证系统 SHALL 验证令牌并允许访问
    需求：6.2 - WHEN API 请求包含有效的会话令牌 THEN API 权限验证器 SHALL 提取用户信息并允许访问
    """
    with test_app.app_context():
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected')
        @require_auth
        def protected_route():
            # 验证 g.current_user_id 被正确设置
            return jsonify({'user_id': g.current_user_id})
        
        # 发送带有有效令牌的请求
        response = test_client.get(
            '/test/protected',
            headers={'Authorization': f'Bearer {valid_token}'}
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == test_user


def test_require_auth_without_token(test_app, test_client):
    """
    测试：缺失令牌拒绝访问
    
    需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
    需求：6.3 - WHEN API 请求不包含会话令牌 THEN API 权限验证器 SHALL 返回 401 未授权错误
    """
    with test_app.app_context():
        # 注册错误处理器
        @test_app.errorhandler(UnauthorizedError)
        def handle_unauthorized(error):
            return jsonify({'error': error.message}), 401
        
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected2')
        @require_auth
        def protected_route():
            return jsonify({'message': 'success'})
        
        # 发送不带令牌的请求
        response = test_client.get('/test/protected2')
        
        # 验证响应
        assert response.status_code == 401
        data = response.get_json()
        assert '未授权' in data['error']


def test_require_auth_with_invalid_token_format(test_app, test_client):
    """
    测试：错误的 Authorization header 格式拒绝访问
    
    需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
    """
    with test_app.app_context():
        # 注册错误处理器
        @test_app.errorhandler(UnauthorizedError)
        def handle_unauthorized(error):
            return jsonify({'error': error.message}), 401
        
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected3')
        @require_auth
        def protected_route():
            return jsonify({'message': 'success'})
        
        # 测试各种错误格式
        invalid_headers = [
            'InvalidFormat',  # 缺少 Bearer 前缀
            'Bearer',  # 只有 Bearer 没有令牌
            'Bearer token1 token2',  # 多个令牌
        ]
        
        for header in invalid_headers:
            response = test_client.get(
                '/test/protected3',
                headers={'Authorization': header}
            )
            assert response.status_code == 401


def test_require_auth_with_invalid_token(test_app, test_client, invalid_token):
    """
    测试：无效令牌拒绝访问
    
    需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问并返回"令牌无效"错误
    需求：6.4 - WHEN API 请求包含无效或过期的会话令牌 THEN API 权限验证器 SHALL 返回 401 未授权错误
    """
    with test_app.app_context():
        # 注册错误处理器
        @test_app.errorhandler(InvalidTokenError)
        def handle_invalid_token(error):
            return jsonify({'error': error.message}), 401
        
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected4')
        @require_auth
        def protected_route():
            return jsonify({'message': 'success'})
        
        # 发送带有无效令牌的请求
        response = test_client.get(
            '/test/protected4',
            headers={'Authorization': f'Bearer {invalid_token}'}
        )
        
        # 验证响应
        assert response.status_code == 401
        data = response.get_json()
        assert '令牌无效' in data['error']


def test_require_auth_with_expired_token(test_app, test_client, expired_token):
    """
    测试：过期令牌拒绝访问
    
    需求：3.2 - WHEN 用户发送包含过期会话令牌的请求 THEN 认证系统 SHALL 拒绝访问并返回"令牌已过期"错误
    需求：6.4 - WHEN API 请求包含无效或过期的会话令牌 THEN API 权限验证器 SHALL 返回 401 未授权错误
    """
    with test_app.app_context():
        # 注册错误处理器
        @test_app.errorhandler(TokenExpiredError)
        def handle_expired_token(error):
            return jsonify({'error': error.message}), 401
        
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected5')
        @require_auth
        def protected_route():
            return jsonify({'message': 'success'})
        
        # 发送带有过期令牌的请求
        response = test_client.get(
            '/test/protected5',
            headers={'Authorization': f'Bearer {expired_token}'}
        )
        
        # 验证响应
        assert response.status_code == 401
        data = response.get_json()
        assert '令牌已过期' in data['error']


def test_require_auth_with_wrong_secret_key(test_app, test_client, test_user):
    """
    测试：使用错误密钥签名的令牌拒绝访问
    
    需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问并返回"令牌无效"错误
    """
    with test_app.app_context():
        # 注册错误处理器
        @test_app.errorhandler(InvalidTokenError)
        def handle_invalid_token(error):
            return jsonify({'error': error.message}), 401
        
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected6')
        @require_auth
        def protected_route():
            return jsonify({'message': 'success'})
        
        # 使用错误的密钥生成令牌
        wrong_secret = 'wrong-secret-key'
        payload = {
            'user_id': test_user,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        wrong_token = jwt.encode(payload, wrong_secret, algorithm='HS256')
        
        # 发送带有错误签名令牌的请求
        response = test_client.get(
            '/test/protected6',
            headers={'Authorization': f'Bearer {wrong_token}'}
        )
        
        # 验证响应
        assert response.status_code == 401
        data = response.get_json()
        assert '令牌无效' in data['error']


def test_require_auth_stores_user_id_in_g(test_app, test_client, valid_token, test_user):
    """
    测试：用户 ID 正确存储到 g.current_user_id
    
    需求：6.2 - WHEN API 请求包含有效的会话令牌 THEN API 权限验证器 SHALL 提取用户信息并允许访问
    """
    with test_app.app_context():
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected7')
        @require_auth
        def protected_route():
            # 验证 g.current_user_id 存在且正确
            assert hasattr(g, 'current_user_id')
            assert g.current_user_id == test_user
            return jsonify({'user_id': g.current_user_id})
        
        # 发送带有有效令牌的请求
        response = test_client.get(
            '/test/protected7',
            headers={'Authorization': f'Bearer {valid_token}'}
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == test_user


def test_require_auth_case_insensitive_bearer(test_app, test_client, valid_token, test_user):
    """
    测试：Bearer 关键字不区分大小写
    
    需求：6.1 - WHEN API 端点被标记为需要认证 THEN API 权限验证器 SHALL 验证请求中的会话令牌
    """
    with test_app.app_context():
        # 创建一个受保护的测试路由
        @test_app.route('/test/protected8')
        @require_auth
        def protected_route():
            return jsonify({'user_id': g.current_user_id})
        
        # 测试不同大小写的 Bearer
        for bearer_keyword in ['Bearer', 'bearer', 'BEARER', 'BeArEr']:
            response = test_client.get(
                '/test/protected8',
                headers={'Authorization': f'{bearer_keyword} {valid_token}'}
            )
            
            # 验证响应
            assert response.status_code == 200
            data = response.get_json()
            assert data['user_id'] == test_user


def test_require_auth_multiple_decorators(test_app, test_client, valid_token, test_user):
    """
    测试：装饰器可以与其他装饰器一起使用
    
    需求：6.1 - WHEN API 端点被标记为需要认证 THEN API 权限验证器 SHALL 验证请求中的会话令牌
    """
    with test_app.app_context():
        # 创建一个带有多个装饰器的测试路由
        def custom_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                # 自定义装饰器逻辑
                return f(*args, **kwargs)
            return decorated
        
        from functools import wraps
        
        @test_app.route('/test/protected9')
        @custom_decorator
        @require_auth
        def protected_route():
            return jsonify({'user_id': g.current_user_id})
        
        # 发送带有有效令牌的请求
        response = test_client.get(
            '/test/protected9',
            headers={'Authorization': f'Bearer {valid_token}'}
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == test_user
