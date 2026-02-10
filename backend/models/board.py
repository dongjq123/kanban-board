"""
Board 模型

本模块定义看板（Board）数据模型，包括：
- Board 类和字段（id、name、created_at、updated_at）
- to_dict() 方法用于 JSON 序列化
- 与 List 的一对多关系和级联删除配置

需求：1.1, 1.6, 7.1, 7.4
"""

from datetime import datetime
from config import db


class Board(db.Model):
    """
    看板模型
    
    看板是最顶层的工作空间，包含多个工作列表。
    当看板被删除时，其下的所有列表和卡片都会被级联删除。
    """
    
    __tablename__ = 'boards'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, comment='看板唯一标识符')
    name = db.Column(db.String(255), nullable=False, comment='看板名称')
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,  # 暂时允许为空，以支持现有数据
        comment='所属用户 ID'
    )
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        comment='创建时间'
    )
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False,
        comment='最后更新时间'
    )
    
    # 关系定义
    # 一个看板可以包含多个列表
    # cascade='all, delete-orphan' 确保删除看板时级联删除所有列表
    # backref='board' 在 List 模型中创建反向引用
    # lazy=True 表示延迟加载，只在访问时才查询列表
    lists = db.relationship(
        'List', 
        backref='board', 
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        """
        将 Board 对象转换为字典，用于 JSON 序列化
        
        Returns:
            dict: 包含看板所有字段的字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """字符串表示，用于调试"""
        return f'<Board {self.id}: {self.name}>'
