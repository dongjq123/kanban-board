"""
AuthService 单元测试

测试 AuthService 类的基本功能，包括：
- 用户注册
- 用户认证
- JWT 令牌生成和验证

需求：1.1-1.6, 2.1-2.6, 3.1-3.4
"""

import pytest
import jwt
from datetime import datetime, timedelta
from services.auth_service import AuthService
from models.user import User
from utils.exceptions import (
    ValidationError,
    AuthenticationError,
    TokenExpiredError,
    InvalidTokenError
)


class TestAuthService:
    """AuthService 测试类"""
    
    @pytest.fixture
    def auth_service(self, app):
        """创建 AuthService 实例"""
        return AuthService(app.config['SECRET_KEY'])
    
    def test_register_user_success(self, auth_service, db_session):
        """测试成功注册用户"""
        # 注册新用户
        user = auth_service.register_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # 验证用户创建成功
        assert user is not None
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.password_hash != 'password123'  # 密码应该被加密
        assert user.password_hash.startswith('$2b$')  # bcrypt 哈希格式
    
    def test_register_user_duplicate_username(self, auth_service, db_session):
        """测试用户名重复"""
        # 创建第一个用户
        auth_service.register_user('testuser', 'test1@example.com', 'password123')
        
        # 尝试使用相同用户名注册
        with pytest.raises(ValidationError) as exc:
            auth_service.register_user('testuser', 'test2@example.com', 'password456')
        
        assert '用户名已被使用' in str(exc.value)
    
    def test_register_user_duplicate_email(self, auth_service, db_session):
        """测试邮箱重复"""
        # 创建第一个用户
        auth_service.register_user('testuser1', 'test@example.com', 'password123')
        
        # 尝试使用相同邮箱注册
        with pytest.raises(ValidationError) as exc:
            auth_service.register_user('testuser2', 'test@example.com', 'password456')
        
        assert '邮箱已被注册' in str(exc.value)
    
    def test_register_user_short_password(self, auth_service, db_session):
        """测试密码太短"""
        with pytest.raises(ValidationError) as exc:
            auth_service.register_user('testuser', 'test@example.com', 'short')
        
        assert '密码长度至少为 8 个字符' in str(exc.value)
    
    def test_register_user_invalid_email(self, auth_service, db_session):
        """测试邮箱格式无效"""
        with pytest.raises(ValidationError) as exc:
            auth_service.register_user('testuser', 'invalid-email', 'password123')
        
        assert '邮箱格式无效' in str(exc.value)
    
    def test_register_user_short_username(self, auth_service, db_session):
        """测试用户名太短"""
        with pytest.raises(ValidationError) as exc:
            auth_service.register_user('ab', 'test@example.com', 'password123')
        
        assert '用户名长度至少为 3 个字符' in str(exc.value)
    
    def test_authenticate_user_with_username(self, auth_service, db_session):
        """测试使用用户名登录"""
        # 注册用户
        auth_service.register_user('testuser', 'test@example.com', 'password123')
        
        # 使用用户名登录
        user = auth_service.authenticate_user('testuser', 'password123')
        
        assert user is not None
        assert user.username == 'testuser'
    
    def test_authenticate_user_with_email(self, auth_service, db_session):
        """测试使用邮箱登录"""
        # 注册用户
        auth_service.register_user('testuser', 'test@example.com', 'password123')
        
        # 使用邮箱登录
        user = auth_service.authenticate_user('test@example.com', 'password123')
        
        assert user is not None
        assert user.email == 'test@example.com'
    
    def test_authenticate_user_wrong_password(self, auth_service, db_session):
        """测试密码错误"""
        # 注册用户
        auth_service.register_user('testuser', 'test@example.com', 'password123')
        
        # 使用错误密码登录
        with pytest.raises(AuthenticationError) as exc:
            auth_service.authenticate_user('testuser', 'wrongpassword')
        
        assert '用户名或密码错误' in str(exc.value)
    
    def test_authenticate_user_not_exist(self, auth_service, db_session):
        """测试用户不存在"""
        with pytest.raises(AuthenticationError) as exc:
            auth_service.authenticate_user('nonexistent', 'password123')
        
        assert '用户名或密码错误' in str(exc.value)
    
    def test_generate_token(self, auth_service, app):
        """测试生成 JWT 令牌"""
        user_id = 123
        token = auth_service.generate_token(user_id)
        
        # 验证令牌不为空
        assert token is not None
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        assert payload['user_id'] == user_id
        assert 'exp' in payload
        assert 'iat' in payload
        
        # 验证有效期为 24 小时（允许 1 秒误差）
        duration = payload['exp'] - payload['iat']
        assert abs(duration - 86400) <= 1
    
    def test_verify_token_valid(self, auth_service):
        """测试验证有效令牌"""
        user_id = 123
        token = auth_service.generate_token(user_id)
        
        # 验证令牌
        verified_user_id = auth_service.verify_token(token)
        
        assert verified_user_id == user_id
    
    def test_verify_token_expired(self, auth_service, app):
        """测试验证过期令牌"""
        # 创建一个已过期的令牌
        user_id = 123
        expiration = datetime.utcnow() - timedelta(hours=1)  # 1 小时前过期
        payload = {
            'user_id': user_id,
            'exp': expiration,
            'iat': datetime.utcnow() - timedelta(hours=25)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        # 验证令牌应该抛出 TokenExpiredError
        with pytest.raises(TokenExpiredError) as exc:
            auth_service.verify_token(token)
        
        assert '令牌已过期' in str(exc.value)
    
    def test_verify_token_invalid_signature(self, auth_service):
        """测试验证签名错误的令牌"""
        # 使用错误的密钥生成令牌
        user_id = 123
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'wrong-secret-key', algorithm='HS256')
        
        # 验证令牌应该抛出 InvalidTokenError
        with pytest.raises(InvalidTokenError) as exc:
            auth_service.verify_token(token)
        
        assert '令牌无效' in str(exc.value)
    
    def test_verify_token_missing_user_id(self, auth_service, app):
        """测试验证缺少 user_id 的令牌"""
        # 创建缺少 user_id 的令牌
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        # 验证令牌应该抛出 InvalidTokenError
        with pytest.raises(InvalidTokenError) as exc:
            auth_service.verify_token(token)
        
        assert '令牌缺少用户 ID' in str(exc.value)
    
    def test_verify_token_malformed(self, auth_service):
        """测试验证格式错误的令牌"""
        # 使用格式错误的令牌
        token = 'invalid.token.format'
        
        # 验证令牌应该抛出 InvalidTokenError
        with pytest.raises(InvalidTokenError):
            auth_service.verify_token(token)
