"""
Pytest 配置和 fixtures

提供测试所需的 fixtures，包括：
- app: Flask 应用实例
- client: Flask 测试客户端
- db: 数据库实例
- db_session: 数据库会话

需求：测试基础设施
"""

import pytest
from app import create_app
from config import db as _db
from migrations import init_database, drop_all_tables


@pytest.fixture(scope='function')
def app():
    """
    创建 Flask 应用实例用于测试
    
    每个测试函数都会创建一个新的应用实例和数据库
    """
    app = create_app('testing')
    
    with app.app_context():
        # 创建所有表
        init_database()
        
        yield app
        
        # 清理：删除所有表
        drop_all_tables()


@pytest.fixture(scope='function')
def client(app):
    """
    创建 Flask 测试客户端
    
    用于测试 API 端点
    """
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """
    提供数据库实例
    
    用于直接操作数据库
    """
    with app.app_context():
        yield _db


@pytest.fixture(scope='function')
def db_session(app, db):
    """
    提供数据库会话
    
    每个测试后自动回滚事务
    """
    with app.app_context():
        yield db.session


@pytest.fixture(scope='function')
def test_user(app, db):
    """
    创建测试用户
    
    用于需要认证的测试
    """
    from models.user import User
    
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        
        yield user


@pytest.fixture(scope='function')
def auth_token(app, test_user):
    """
    生成测试用户的认证令牌
    
    用于需要认证的 API 测试
    """
    from services.auth_service import AuthService
    
    with app.app_context():
        auth_service = AuthService(
            secret_key=app.config['SECRET_KEY'],
            token_expiration_hours=24
        )
        token = auth_service.generate_token(test_user.id)
        
        yield token


@pytest.fixture(scope='function')
def auth_headers(auth_token):
    """
    生成包含认证令牌的请求头
    
    用于需要认证的 API 测试
    """
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

