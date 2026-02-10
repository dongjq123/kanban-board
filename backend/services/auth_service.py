"""
认证服务模块

本模块提供用户认证相关的业务逻辑，包括：
- 用户注册（register_user）
- 用户认证（authenticate_user）
- JWT 令牌生成（generate_token）
- JWT 令牌验证（verify_token）

需求：1.1-1.6, 2.1-2.6, 3.1-3.4
"""

import re
from datetime import datetime, timedelta
import jwt
from config import db
from models.user import User
from utils.exceptions import (
    ValidationError,
    AuthenticationError,
    TokenExpiredError,
    InvalidTokenError
)


class AuthService:
    """
    认证服务类
    
    处理用户认证相关的业务逻辑，包括注册、登录、令牌生成和验证。
    """
    
    def __init__(self, secret_key, token_expiration_hours=24):
        """
        初始化认证服务
        
        Args:
            secret_key (str): JWT 签名密钥
            token_expiration_hours (int): 令牌有效期（小时），默认 24 小时
        """
        self.secret_key = secret_key
        self.token_expiration_hours = token_expiration_hours
    
    def register_user(self, username, email, password):
        """
        注册新用户
        
        需求：1.1 - WHEN 用户提交有效的注册信息 THEN 认证系统 SHALL 创建新用户账户
        需求：1.2 - WHEN 用户提交的用户名已存在 THEN 认证系统 SHALL 拒绝注册
        需求：1.3 - WHEN 用户提交的邮箱已存在 THEN 认证系统 SHALL 拒绝注册
        需求：1.4 - WHEN 用户提交的密码长度少于 8 个字符 THEN 认证系统 SHALL 拒绝注册
        需求：1.5 - WHEN 用户提交的邮箱格式无效 THEN 认证系统 SHALL 拒绝注册
        需求：1.6 - WHEN 创建新用户账户 THEN 认证系统 SHALL 使用 bcrypt 算法加密存储密码
        
        Args:
            username (str): 用户名（3-50 字符）
            email (str): 邮箱地址
            password (str): 密码（至少 8 字符）
        
        Returns:
            User: 创建的用户对象
        
        Raises:
            ValidationError: 如果验证失败
        """
        # 去除首尾空白
        if username:
            username = username.strip()
        if email:
            email = email.strip()
        
        # 验证用户名长度
        if not username or len(username) < 3:
            raise ValidationError("用户名长度至少为 3 个字符")
        
        if len(username) > 50:
            raise ValidationError("用户名长度不能超过 50 个字符")
        
        # 验证邮箱格式
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not email or not re.match(email_pattern, email):
            raise ValidationError("邮箱格式无效")
        
        # 验证密码长度
        if not password or len(password) < 8:
            raise ValidationError("密码长度至少为 8 个字符")
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValidationError("用户名已被使用")
        
        # 检查邮箱是否已存在
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValidationError("邮箱已被注册")
        
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)  # 使用 bcrypt 加密密码
        
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def authenticate_user(self, identifier, password):
        """
        验证用户身份
        
        需求：2.1 - WHEN 用户使用有效的邮箱和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
        需求：2.2 - WHEN 用户使用有效的用户名和密码登录 THEN 认证系统 SHALL 返回会话令牌和用户信息
        需求：2.3 - WHEN 用户提交的邮箱或用户名不存在 THEN 认证系统 SHALL 返回"用户名或密码错误"
        需求：2.4 - WHEN 用户提交的密码不正确 THEN 认证系统 SHALL 返回"用户名或密码错误"
        
        Args:
            identifier (str): 邮箱或用户名
            password (str): 密码
        
        Returns:
            User: 验证成功的用户对象
        
        Raises:
            AuthenticationError: 如果验证失败
        """
        # 尝试通过邮箱或用户名查找用户
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()
        
        # 用户不存在或密码错误，返回相同的错误消息（防止用户枚举攻击）
        if not user or not user.check_password(password):
            raise AuthenticationError("用户名或密码错误")
        
        return user
    
    def generate_token(self, user_id):
        """
        生成 JWT 令牌
        
        需求：2.5 - WHEN 用户成功登录 THEN 认证系统 SHALL 生成包含用户 ID 和过期时间的 JWT 令牌
        需求：2.6 - WHEN 生成 JWT 令牌 THEN 认证系统 SHALL 设置令牌有效期为 24 小时
        
        Args:
            user_id (int): 用户 ID
        
        Returns:
            str: JWT 令牌字符串
        """
        # 计算过期时间（当前时间 + 24 小时）
        expiration = datetime.utcnow() + timedelta(hours=self.token_expiration_hours)
        
        # 创建 JWT payload
        payload = {
            'user_id': user_id,
            'exp': expiration,  # 过期时间
            'iat': datetime.utcnow()  # 签发时间
        }
        
        # 生成 JWT 令牌
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        return token
    
    def verify_token(self, token):
        """
        验证 JWT 令牌
        
        需求：3.1 - WHEN 用户发送包含有效会话令牌的请求 THEN 认证系统 SHALL 验证令牌并允许访问
        需求：3.2 - WHEN 用户发送包含过期会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
        需求：3.3 - WHEN 用户发送包含无效会话令牌的请求 THEN 认证系统 SHALL 拒绝访问
        
        Args:
            token (str): JWT 令牌字符串
        
        Returns:
            int: 用户 ID
        
        Raises:
            TokenExpiredError: 如果令牌过期
            InvalidTokenError: 如果令牌无效
        """
        try:
            # 解码 JWT 令牌
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # 提取用户 ID
            user_id = payload.get('user_id')
            
            if not user_id:
                raise InvalidTokenError("令牌缺少用户 ID")
            
            return user_id
        
        except jwt.ExpiredSignatureError:
            # 令牌过期
            raise TokenExpiredError("令牌已过期，请重新登录")
        
        except jwt.InvalidTokenError:
            # 令牌无效（签名错误、格式错误等）
            raise InvalidTokenError("令牌无效")
        
        except Exception as e:
            # 其他错误
            raise InvalidTokenError(f"令牌验证失败: {str(e)}")

