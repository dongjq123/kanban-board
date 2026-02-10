"""
Card 模型

本模块定义任务卡片（Card）数据模型，包括：
- Card 类和字段（id、list_id、title、description、due_date、tags、position、created_at、updated_at）
- to_dict() 方法用于 JSON 序列化
- 与 List 的外键关系

需求：3.1, 3.7, 3.8, 3.9, 7.3, 7.4, 7.7
"""

from datetime import datetime
from config import db


class Card(db.Model):
    """
    任务卡片模型
    
    任务卡片是最基础的任务单元，包含具体的任务信息。
    卡片属于一个工作列表，可以包含标题、描述、截止日期和标签等信息。
    """
    
    __tablename__ = 'cards'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, comment='卡片唯一标识符')
    list_id = db.Column(
        db.Integer, 
        db.ForeignKey('lists.id'), 
        nullable=False,
        comment='所属列表 ID'
    )
    title = db.Column(db.String(255), nullable=False, comment='卡片标题')
    description = db.Column(db.Text, comment='卡片描述（可选）')
    due_date = db.Column(db.Date, comment='截止日期（可选）')
    tags = db.Column(db.JSON, comment='标签数组，存储为 JSON 格式（可选）')
    position = db.Column(
        db.Integer, 
        nullable=False, 
        default=0,
        comment='卡片在列表中的位置顺序'
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
    # 与 List 的关系通过 backref 在 List 模型中定义
    # 这里不需要额外定义关系，因为 List 模型已经定义了 cards 关系
    
    def to_dict(self):
        """
        将 Card 对象转换为字典，用于 JSON 序列化
        
        Returns:
            dict: 包含卡片所有字段的字典
        """
        return {
            'id': self.id,
            'list_id': self.list_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags or [],
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """字符串表示，用于调试"""
        return f'<Card {self.id}: {self.title}>'
