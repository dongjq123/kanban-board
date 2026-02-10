"""
List 模型

本模块定义工作列表（List）数据模型，包括：
- List 类和字段（id、board_id、name、position、created_at、updated_at）
- to_dict() 方法用于 JSON 序列化
- 与 Board 的外键关系和与 Card 的一对多关系
- 级联删除配置

需求：2.1, 2.5, 7.2, 7.4, 7.7
"""

from datetime import datetime
from config import db


class List(db.Model):
    """
    工作列表模型
    
    工作列表是看板中的一列，包含多个任务卡片，代表工作流的某个阶段。
    列表属于一个看板，当列表被删除时，其下的所有卡片都会被级联删除。
    """
    
    __tablename__ = 'lists'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, comment='列表唯一标识符')
    board_id = db.Column(
        db.Integer, 
        db.ForeignKey('boards.id'), 
        nullable=False,
        comment='所属看板 ID'
    )
    name = db.Column(db.String(255), nullable=False, comment='列表名称')
    position = db.Column(
        db.Integer, 
        nullable=False, 
        default=0,
        comment='列表在看板中的位置顺序'
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
    # 与 Board 的关系通过 backref 在 Board 模型中定义
    # 这里定义与 Card 的一对多关系
    # cascade='all, delete-orphan' 确保删除列表时级联删除所有卡片
    # backref='list' 在 Card 模型中创建反向引用
    # lazy=True 表示延迟加载，只在访问时才查询卡片
    cards = db.relationship(
        'Card', 
        backref='list', 
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        """
        将 List 对象转换为字典，用于 JSON 序列化
        
        Returns:
            dict: 包含列表所有字段的字典
        """
        return {
            'id': self.id,
            'board_id': self.board_id,
            'name': self.name,
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """字符串表示，用于调试"""
        return f'<List {self.id}: {self.name}>'

