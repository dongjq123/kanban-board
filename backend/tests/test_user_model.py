"""
User 模型单元测试

测试 User 模型的基本功能：
- 密码加密和验证
- to_dict() 方法
- 数据库字段约束

需求：1.6, 7.1, 7.2, 7.3, 7.4
"""

import pytest
from models.user import User
from config import db


class TestUserModel:
    """User 模型测试类"""
    
    def test_set_password_encrypts_password(self, app):
        """
        测试 set_password() 方法正确加密密码
        
        需求：1.6, 7.1 - 密码应该使用 bcrypt 加密
        """
        with app.app_context():
            user = User()
            user.username = 'testuser'
            user.email = 'test@example.com'
            user.set_password('mypassword123')
            
            # 验证密码哈希不等于明文密码
            assert user.password_hash != 'mypassword123'
            
            # 验证密码哈希以 $2b$ 开头（bcrypt 标识）
            assert user.password_hash.startswith('$2b$')
            
            # 验证密码哈希包含轮数信息（$2b$12$）
            assert user.password_hash.startswith('$2b$12$')
    
    def test_check_password_with_correct_password(self, app):
        """
        测试 check_password() 方法验证正确密码
        
        需求：7.2 - 应该使用 bcrypt 验证密码
        """
        with app.app_context():
            user = User()
            user.username = 'testuser'
            user.email = 'test@example.com'
            user.set_password('mypassword123')
            
            # 验证正确的密码返回 True
            assert user.check_password('mypassword123') is True
    
    def test_check_password_with_incorrect_password(self, app):
        """
        测试 check_password() 方法拒绝错误密码
        
        需求：7.2 - 应该使用 bcrypt 验证密码
        """
        with app.app_context():
            user = User()
            user.username = 'testuser'
            user.email = 'test@example.com'
            user.set_password('mypassword123')
            
            # 验证错误的密码返回 False
            assert user.check_password('wrongpassword') is False
    
    def test_to_dict_excludes_password_hash(self, app):
        """
        测试 to_dict() 方法不包含密码哈希
        
        需求：7.4 - API 返回用户信息时应该排除密码哈希
        """
        with app.app_context():
            user = User()
            user.id = 1
            user.username = 'testuser'
            user.email = 'test@example.com'
            user.set_password('mypassword123')
            
            user_dict = user.to_dict()
            
            # 验证字典包含必要字段
            assert 'id' in user_dict
            assert 'username' in user_dict
            assert 'email' in user_dict
            assert 'created_at' in user_dict
            
            # 验证字典不包含密码相关字段
            assert 'password' not in user_dict
            assert 'password_hash' not in user_dict
            
            # 验证字段值正确
            assert user_dict['id'] == 1
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'
    
    def test_user_creation_and_persistence(self, app):
        """
        测试用户创建和数据库持久化
        
        需求：1.1 - 应该能够创建新用户账户
        """
        with app.app_context():
            # 创建用户
            user = User()
            user.username = 'newuser'
            user.email = 'newuser@example.com'
            user.set_password('password123')
            
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            
            # 从数据库查询用户
            saved_user = User.query.filter_by(username='newuser').first()
            
            # 验证用户存在
            assert saved_user is not None
            assert saved_user.username == 'newuser'
            assert saved_user.email == 'newuser@example.com'
            
            # 验证密码验证功能
            assert saved_user.check_password('password123') is True
            assert saved_user.check_password('wrongpassword') is False
    
    def test_username_uniqueness(self, app):
        """
        测试用户名唯一性约束
        
        需求：1.2 - 用户名应该是唯一的
        """
        with app.app_context():
            # 创建第一个用户
            user1 = User()
            user1.username = 'uniqueuser'
            user1.email = 'user1@example.com'
            user1.set_password('password123')
            db.session.add(user1)
            db.session.commit()
            
            # 尝试创建相同用户名的用户
            user2 = User()
            user2.username = 'uniqueuser'
            user2.email = 'user2@example.com'
            user2.set_password('password456')
            db.session.add(user2)
            
            # 验证会抛出异常
            with pytest.raises(Exception):  # SQLAlchemy 会抛出 IntegrityError
                db.session.commit()
            
            # 回滚事务
            db.session.rollback()
    
    def test_email_uniqueness(self, app):
        """
        测试邮箱唯一性约束
        
        需求：1.3 - 邮箱应该是唯一的
        """
        with app.app_context():
            # 创建第一个用户
            user1 = User()
            user1.username = 'user1'
            user1.email = 'unique@example.com'
            user1.set_password('password123')
            db.session.add(user1)
            db.session.commit()
            
            # 尝试创建相同邮箱的用户
            user2 = User()
            user2.username = 'user2'
            user2.email = 'unique@example.com'
            user2.set_password('password456')
            db.session.add(user2)
            
            # 验证会抛出异常
            with pytest.raises(Exception):  # SQLAlchemy 会抛出 IntegrityError
                db.session.commit()
            
            # 回滚事务
            db.session.rollback()
    
    def test_password_with_special_characters(self, app):
        """
        测试包含特殊字符的密码
        
        需求：7.1 - bcrypt 应该能够处理各种字符
        """
        with app.app_context():
            user = User()
            user.username = 'testuser'
            user.email = 'test@example.com'
            
            # 测试包含特殊字符的密码
            special_password = 'P@ssw0rd!#$%^&*()'
            user.set_password(special_password)
            
            # 验证密码正确加密和验证
            assert user.check_password(special_password) is True
            assert user.check_password('wrongpassword') is False
    
    def test_password_with_unicode_characters(self, app):
        """
        测试包含 Unicode 字符的密码
        
        需求：7.1 - bcrypt 应该能够处理 Unicode 字符
        """
        with app.app_context():
            user = User()
            user.username = 'testuser'
            user.email = 'test@example.com'
            
            # 测试包含中文字符的密码
            unicode_password = '密码123'
            user.set_password(unicode_password)
            
            # 验证密码正确加密和验证
            assert user.check_password(unicode_password) is True
            assert user.check_password('wrongpassword') is False
