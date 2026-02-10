"""
User 模型

本模块定义用户（User）数据模型，包括：
- User 类和字段（id、username、email、password_hash、created_at）
- set_password() 方法用于密码加密（使用 bcrypt，12 轮）
- check_password() 方法用于密码验证
- to_dict() 方法用于 JSON 序列化（排除 password_hash）

需求：1.6, 7.1, 7.3, 7.4
"""

from datetime import datetime
import bcrypt
from config import db


class User(db.Model):
    """
    用户模型
    
    用户是系统的基本实体，拥有自己的看板、列表和卡片。
    密码使用 bcrypt 算法加密存储，确保安全性。
    """
    
    __tablename__ = 'users'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, comment='用户唯一标识符')
    username = db.Column(
        db.String(50), 
        unique=True, 
        nullable=False, 
        comment='用户名（唯一）'
    )
    email = db.Column(
        db.String(255), 
        unique=True, 
        nullable=False, 
        comment='邮箱（唯一）'
    )
    password_hash = db.Column(
        db.String(255), 
        nullable=False, 
        comment='bcrypt 加密的密码哈希'
    )
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        comment='创建时间'
    )
    
    # 关系定义
    # 一个用户可以拥有多个看板
    # cascade='all, delete-orphan' 确保删除用户时级联删除所有看板
    # backref='user' 在 Board 模型中创建反向引用
    # lazy=True 表示延迟加载，只在访问时才查询看板
    boards = db.relationship(
        'Board', 
        backref='user', 
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password):
        """
        使用 bcrypt 加密并设置密码
        
        需求：1.6 - WHEN 创建新用户账户 THEN 认证系统 SHALL 使用 bcrypt 算法加密存储密码
        需求：7.1 - WHEN 用户注册或修改密码 THEN 认证系统 SHALL 使用 bcrypt 算法和至少 12 轮加密
        
        Args:
            password (str): 明文密码
        """
        # 使用 bcrypt 加密密码，12 轮加密
        # bcrypt.gensalt(rounds=12) 生成盐值，rounds=12 表示 2^12 次迭代
        salt = bcrypt.gensalt(rounds=12)
        # bcrypt.hashpw() 使用盐值加密密码
        # password.encode('utf-8') 将字符串转换为字节
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        # 将字节转换为字符串存储到数据库
        self.password_hash = password_hash.decode('utf-8')
    
    def check_password(self, password):
        """
        验证密码是否正确
        
        需求：7.2 - WHEN 用户登录 THEN 认证系统 SHALL 使用 bcrypt 验证密码而不是明文比较
        
        Args:
            password (str): 待验证的明文密码
        
        Returns:
            bool: 密码正确返回 True，否则返回 False
        """
        # bcrypt.checkpw() 验证密码
        # 将存储的哈希值和明文密码都转换为字节进行比较
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        """
        将 User 对象转换为字典，用于 JSON 序列化
        
        需求：7.4 - WHEN API 返回用户信息 THEN 认证系统 SHALL 排除密码哈希字段
        
        Returns:
            dict: 包含用户字段的字典（排除 password_hash）
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """字符串表示，用于调试"""
        return f'<User {self.id}: {self.username}>'
