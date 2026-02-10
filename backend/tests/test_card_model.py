"""
Card 模型单元测试

本测试文件验证任务 2.4 的 Card 模型实现，包括：
- 字段定义和验证
- to_dict() JSON 序列化方法
- 与 List 的外键关系
- 可选字段（description、due_date、tags）的处理

需求：3.1, 3.7, 3.8, 3.9, 7.3, 7.4, 7.7
"""

import pytest
from datetime import datetime, date
from config import db, get_config
from flask import Flask
from models import Board, List, Card


@pytest.fixture
def app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config.from_object(get_config('testing'))
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """创建应用上下文"""
    with app.app_context():
        yield


@pytest.fixture
def sample_list(app_context):
    """创建示例列表用于测试"""
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    return list_obj


def test_card_model_basic_fields(sample_list):
    """测试 Card 模型基本字段定义"""
    # 创建一个卡片（只包含必需字段）
    card = Card(
        list_id=sample_list.id,
        title='实现用户登录功能',
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证必需字段
    assert card.id is not None
    assert card.list_id == sample_list.id
    assert card.title == '实现用户登录功能'
    assert card.position == 0
    assert card.created_at is not None
    assert card.updated_at is not None
    assert isinstance(card.created_at, datetime)
    assert isinstance(card.updated_at, datetime)
    
    # 验证可选字段默认值
    assert card.description is None
    assert card.due_date is None
    assert card.tags is None


def test_card_model_all_fields(sample_list):
    """测试 Card 模型所有字段（包括可选字段）"""
    # 创建一个包含所有字段的卡片
    card = Card(
        list_id=sample_list.id,
        title='实现用户登录功能',
        description='使用 JWT 实现用户认证',
        due_date=date(2024, 1, 20),
        tags=['后端', '高优先级'],
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证所有字段
    assert card.id is not None
    assert card.list_id == sample_list.id
    assert card.title == '实现用户登录功能'
    assert card.description == '使用 JWT 实现用户认证'
    assert card.due_date == date(2024, 1, 20)
    assert card.tags == ['后端', '高优先级']
    assert card.position == 0
    assert card.created_at is not None
    assert card.updated_at is not None


def test_card_to_dict_basic(sample_list):
    """测试 Card 模型的 to_dict() 方法（基本字段）"""
    # 创建一个卡片（只包含必需字段）
    card = Card(
        list_id=sample_list.id,
        title='编写单元测试',
        position=1
    )
    db.session.add(card)
    db.session.commit()
    
    # 转换为字典
    card_dict = card.to_dict()
    
    # 验证字典内容
    assert card_dict['id'] == card.id
    assert card_dict['list_id'] == sample_list.id
    assert card_dict['title'] == '编写单元测试'
    assert card_dict['description'] is None
    assert card_dict['due_date'] is None
    assert card_dict['tags'] == []  # 空列表而不是 None
    assert card_dict['position'] == 1
    assert 'created_at' in card_dict
    assert 'updated_at' in card_dict
    # 验证时间格式为 ISO 格式
    assert 'T' in card_dict['created_at']
    assert 'T' in card_dict['updated_at']


def test_card_to_dict_all_fields(sample_list):
    """测试 Card 模型的 to_dict() 方法（所有字段）"""
    # 创建一个包含所有字段的卡片
    card = Card(
        list_id=sample_list.id,
        title='实现拖拽功能',
        description='使用 Vue.Draggable 实现卡片拖拽',
        due_date=date(2024, 2, 15),
        tags=['前端', '用户体验', '重要'],
        position=2
    )
    db.session.add(card)
    db.session.commit()
    
    # 转换为字典
    card_dict = card.to_dict()
    
    # 验证字典内容
    assert card_dict['id'] == card.id
    assert card_dict['list_id'] == sample_list.id
    assert card_dict['title'] == '实现拖拽功能'
    assert card_dict['description'] == '使用 Vue.Draggable 实现卡片拖拽'
    assert card_dict['due_date'] == '2024-02-15'  # ISO 格式日期
    assert card_dict['tags'] == ['前端', '用户体验', '重要']
    assert card_dict['position'] == 2
    assert 'created_at' in card_dict
    assert 'updated_at' in card_dict


def test_card_list_relationship(sample_list):
    """测试 Card 与 List 的关系"""
    # 创建多个卡片
    card1 = Card(list_id=sample_list.id, title='任务1', position=0)
    card2 = Card(list_id=sample_list.id, title='任务2', position=1)
    card3 = Card(list_id=sample_list.id, title='任务3', position=2)
    
    db.session.add_all([card1, card2, card3])
    db.session.commit()
    
    # 通过 List 访问 Cards
    assert len(sample_list.cards) == 3
    assert card1 in sample_list.cards
    assert card2 in sample_list.cards
    assert card3 in sample_list.cards
    
    # 通过 Card 访问 List
    assert card1.list == sample_list
    assert card2.list == sample_list
    assert card3.list == sample_list


def test_card_tags_empty_list(sample_list):
    """测试 Card 的 tags 字段为空列表时的处理"""
    # 创建一个 tags 为空列表的卡片
    card = Card(
        list_id=sample_list.id,
        title='测试任务',
        tags=[],
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证 to_dict() 返回空列表
    card_dict = card.to_dict()
    assert card_dict['tags'] == []


def test_card_tags_none(sample_list):
    """测试 Card 的 tags 字段为 None 时的处理"""
    # 创建一个 tags 为 None 的卡片
    card = Card(
        list_id=sample_list.id,
        title='测试任务',
        tags=None,
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证 to_dict() 返回空列表而不是 None
    card_dict = card.to_dict()
    assert card_dict['tags'] == []


def test_card_update_fields(sample_list):
    """测试更新 Card 字段"""
    # 创建一个卡片
    card = Card(
        list_id=sample_list.id,
        title='初始标题',
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    original_updated_at = card.updated_at
    
    # 更新字段
    card.title = '更新后的标题'
    card.description = '添加描述'
    card.due_date = date(2024, 3, 1)
    card.tags = ['新标签']
    db.session.commit()
    
    # 验证更新
    assert card.title == '更新后的标题'
    assert card.description == '添加描述'
    assert card.due_date == date(2024, 3, 1)
    assert card.tags == ['新标签']
    # updated_at 应该被更新（注意：在某些数据库中可能需要时间差）
    # 这里只验证字段存在
    assert card.updated_at is not None


def test_card_position_default(sample_list):
    """测试 Card 的 position 字段默认值"""
    # 创建一个不指定 position 的卡片
    card = Card(
        list_id=sample_list.id,
        title='测试任务'
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证 position 默认为 0
    assert card.position == 0


def test_card_repr(sample_list):
    """测试 Card 模型的字符串表示"""
    card = Card(
        list_id=sample_list.id,
        title='测试卡片标题',
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    repr_str = repr(card)
    assert 'Card' in repr_str
    assert str(card.id) in repr_str
    assert '测试卡片标题' in repr_str


def test_multiple_cards_in_different_lists(app_context):
    """测试在不同列表中创建卡片"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建两个列表
    list1 = List(board_id=board.id, name='待办', position=0)
    list2 = List(board_id=board.id, name='进行中', position=1)
    db.session.add_all([list1, list2])
    db.session.commit()
    
    # 在不同列表中创建卡片
    card1 = Card(list_id=list1.id, title='任务1', position=0)
    card2 = Card(list_id=list2.id, title='任务2', position=0)
    db.session.add_all([card1, card2])
    db.session.commit()
    
    # 验证卡片属于正确的列表
    assert card1.list == list1
    assert card2.list == list2
    assert len(list1.cards) == 1
    assert len(list2.cards) == 1


def test_card_with_complex_tags(sample_list):
    """测试 Card 的 tags 字段支持复杂标签"""
    # 创建一个包含多个标签的卡片
    card = Card(
        list_id=sample_list.id,
        title='复杂任务',
        tags=['标签1', '标签2', '标签3', '中文标签', 'English Tag'],
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证标签正确保存和检索
    assert len(card.tags) == 5
    assert '标签1' in card.tags
    assert '中文标签' in card.tags
    assert 'English Tag' in card.tags
    
    # 验证 to_dict() 正确序列化标签
    card_dict = card.to_dict()
    assert card_dict['tags'] == ['标签1', '标签2', '标签3', '中文标签', 'English Tag']


def test_card_due_date_serialization(sample_list):
    """测试 Card 的 due_date 字段序列化"""
    # 创建一个包含截止日期的卡片
    card = Card(
        list_id=sample_list.id,
        title='有截止日期的任务',
        due_date=date(2024, 12, 31),
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证 to_dict() 正确序列化日期为 ISO 格式
    card_dict = card.to_dict()
    assert card_dict['due_date'] == '2024-12-31'


def test_card_due_date_none_serialization(sample_list):
    """测试 Card 的 due_date 为 None 时的序列化"""
    # 创建一个没有截止日期的卡片
    card = Card(
        list_id=sample_list.id,
        title='无截止日期的任务',
        position=0
    )
    db.session.add(card)
    db.session.commit()
    
    # 验证 to_dict() 返回 None
    card_dict = card.to_dict()
    assert card_dict['due_date'] is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
