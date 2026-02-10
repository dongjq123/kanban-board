"""
认证 API 单元测试

测试认证相关的 API 端点，包括：
- 用户注册 (POST /api/auth/register)
- 用户登录 (POST /api/auth/login)
- 令牌验证 (GET /api/auth/verify)
- 输入验证
- 错误处理

需求：1.1-1.6, 2.1-2.6, 3.1-3.4
"""

import pytest
import json
import jwt
from datetime import datetime, timedelta


class TestAuthRegisterAPI:
    """用户注册 API 测试类"""
    
    def test_register_success(self, client):
        """
        测试成功注册用户
        
        需求：1.1 - WHEN 用户提交有效的注册信息 THEN 认证系统 SHALL 创建新用户账户
        """
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == '注册成功'
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        assert data['user']['email'] == 'test@example.com'
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
        assert 'id' in data['user']
        assert 'created_at' in data['user']
    
    def test_register_with_duplicate_username_returns_400(self, client):
        """
        测试重复用户名注册返回 400 错误
        
        需求：1.2 - WHEN 用户提交的用户名已存在 THEN 认证系统 SHALL 拒绝注册
        """
        # 第一次注册
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test1@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 第二次注册相同用户名
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test2@example.com',
                'password': 'password456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '用户名已被使用' in data['error']['message']
    
    def test_register_with_duplicate_email_returns_400(self, client):
        """
        测试重复邮箱注册返回 400 错误
        
        需求：1.3 - WHEN 用户提交的邮箱已存在 THEN 认证系统 SHALL 拒绝注册
        """
        # 第一次注册
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser1',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 第二次注册相同邮箱
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser2',
                'email': 'test@example.com',
                'password': 'password456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '邮箱已被注册' in data['error']['message']
    
    def test_register_with_short_password_returns_400(self, client):
        """
        测试密码过短注册返回 400 错误
        
        需求：1.4 - WHEN 用户提交的密码长度少于 8 个字符 THEN 认证系统 SHALL 拒绝注册
        """
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'pass123'  # 只有 7 个字符
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '密码长度至少为 8 个字符' in data['error']['message']
    
    def test_register_with_invalid_email_returns_400(self, client):
        """
        测试无效邮箱格式注册返回 400 错误
        
        需求：1.5 - WHEN 用户提交的邮箱格式无效 THEN 认证系统 SHALL 拒绝注册
        """
        invalid_emails = [
            'notanemail',
            'missing@domain',
            '@nodomain.com',
            'no@domain',
            'spaces in@email.com'
        ]
        
        for invalid_email in invalid_emails:
            response = client.post(
                '/api/auth/register',
                data=json.dumps({
                    'username': 'testuser',
                    'email': invalid_email,
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
            assert data['error']['code'] == 'VALIDATION_ERROR'
            assert '邮箱格式无效' in data['error']['message']
    
    def test_register_with_short_username_returns_400(self, client):
        """
        测试用户名过短注册返回 400 错误
        """
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'ab',  # 只有 2 个字符
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '用户名长度至少为 3 个字符' in data['error']['message']


class TestAuthLoginAPI:
    """用户登录 API 测试类"""
    
    def test_login_with_email_success(self, client):
        """
        测试使用邮箱成功登录
        
        需求：2.1 - WHEN 用户使用有效的邮箱和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
        需求：2.5 - WHEN 用户成功登录 THEN 认证系统 SHALL 生成包含用户 ID 和过期时间的 JWT 令牌
        """
        # 先注册用户
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 使用邮箱登录
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        assert data['user']['email'] == 'test@example.com'
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_login_with_username_success(self, client):
        """
        测试使用用户名成功登录
        
        需求：2.2 - WHEN 用户使用有效的用户名和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
        """
        # 先注册用户
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 使用用户名登录
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'testuser',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_login_with_nonexistent_user_returns_401(self, client):
        """
        测试不存在的用户登录返回 401 错误
        
        需求：2.3 - WHEN 用户提交的邮箱或用户名不存在 THEN 认证系统 SHALL 返回"用户名或密码错误"
        """
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'nonexistent@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'AUTHENTICATION_ERROR'
        assert '用户名或密码错误' in data['error']['message']
    
    def test_login_with_wrong_password_returns_401(self, client):
        """
        测试错误密码登录返回 401 错误
        
        需求：2.4 - WHEN 用户提交的密码不正确 THEN 认证系统 SHALL 返回"用户名或密码错误"
        """
        # 先注册用户
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # 使用错误密码登录
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'test@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'AUTHENTICATION_ERROR'
        assert '用户名或密码错误' in data['error']['message']
    
    def test_login_token_structure(self, client, app):
        """
        测试登录返回的 JWT 令牌结构
        
        需求：2.5 - WHEN 用户成功登录 THEN 认证系统 SHALL 生成包含用户 ID 和过期时间的 JWT 令牌
        需求：2.6 - WHEN 生成 JWT 令牌 THEN 认证系统 SHALL 设置令牌有效期为 24 小时
        """
        # 先注册用户
        register_response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = register_response.get_json()['user']['id']
        
        # 登录
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = login_response.get_json()['token']
        
        # 解码令牌验证结构
        with app.app_context():
            payload = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        
        # 验证字段存在
        assert 'user_id' in payload
        assert 'exp' in payload
        assert 'iat' in payload
        
        # 验证用户 ID 正确
        assert payload['user_id'] == user_id
        
        # 验证有效期为 24 小时（允许 2 秒误差）
        duration = payload['exp'] - payload['iat']
        assert abs(duration - 86400) <= 2


class TestAuthVerifyAPI:
    """令牌验证 API 测试类"""
    
    def test_verify_with_valid_token_success(self, client):
        """
        测试使用有效令牌验证成功
        
        需求：3.1 - WHEN 用户发送包含有效会话令牌的请求 THEN 认证系统 SHALL 验证令牌并允许访问
        """
        # 先注册并登录
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'identifier': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        token = login_response.get_json()['token']
        
        # 验证令牌
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        assert data['user']['email'] == 'test@example.com'
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_verify_without_token_returns_401(self, client):
        """
        测试不带令牌验证返回 401 错误
        
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问
        """
        response = client.get('/api/auth/verify')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
        assert '未授权' in data['error']['message']
    
    def test_verify_with_invalid_token_returns_401(self, client):
        """
        测试使用无效令牌验证返回 401 错误
        
        需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
        """
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': 'Bearer invalid_token_here'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'INVALID_TOKEN'
    
    def test_verify_with_expired_token_returns_401(self, client, app):
        """
        测试使用过期令牌验证返回 401 错误
        
        需求：3.2 - WHEN 用户发送包含过期会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
        """
        # 先注册用户
        register_response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = register_response.get_json()['user']['id']
        
        # 手动创建一个过期的令牌
        with app.app_context():
            expired_payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() - timedelta(hours=1),  # 1 小时前过期
                'iat': datetime.utcnow() - timedelta(hours=25)  # 25 小时前签发
            }
            expired_token = jwt.encode(
                expired_payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        
        # 使用过期令牌验证
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': f'Bearer {expired_token}'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'TOKEN_EXPIRED'
        assert '令牌已过期' in data['error']['message']
    
    def test_verify_with_malformed_authorization_header_returns_401(self, client):
        """
        测试使用格式错误的 Authorization header 返回 401 错误
        """
        # 测试缺少 Bearer 前缀
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': 'some_token'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
        
        # 测试错误的前缀
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': 'Basic some_token'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
