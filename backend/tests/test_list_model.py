"""
临时测试文件：验证 List 模型实现

这个测试文件用于验证任务 2.3 的 List 模型实现是否正确。
"""

import pytest
from datetime import datetime
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


def test_list_model_fields(app_context):
    """测试 List 模型字段定义"""
    # 创建一个看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建一个列表
    list_obj = List(
        board_id=board.id,
        name='待办事项',
        position=0
    )
    db.session.add(list_obj)
    db.session.commit()
    
    # 验证字段
    assert list_obj.id is not None
    assert list_obj.board_id == board.id
    assert list_obj.name == '待办事项'
    assert list_obj.position == 0
    assert list_obj.created_at is not None
    assert list_obj.updated_at is not None
    assert isinstance(list_obj.created_at, datetime)
    assert isinstance(list_obj.updated_at, datetime)


def test_list_to_dict(app_context):
    """测试 List 模型的 to_dict() 方法"""
    # 创建一个看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建一个列表
    list_obj = List(
        board_id=board.id,
        name='进行中',
        position=1
    )
    db.session.add(list_obj)
    db.session.commit()
    
    # 转换为字典
    list_dict = list_obj.to_dict()
    
    # 验证字典内容
    assert list_dict['id'] == list_obj.id
    assert list_dict['board_id'] == board.id
    assert list_dict['name'] == '进行中'
    assert list_dict['position'] == 1
    assert 'created_at' in list_dict
    assert 'updated_at' in list_dict
    # 验证时间格式为 ISO 格式
    assert 'T' in list_dict['created_at']
    assert 'T' in list_dict['updated_at']


def test_list_board_relationship(app_context):
    """测试 List 与 Board 的关系"""
    # 创建一个看板
    board = Board(name='项目看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建多个列表
    list1 = List(board_id=board.id, name='待办', position=0)
    list2 = List(board_id=board.id, name='进行中', position=1)
    list3 = List(board_id=board.id, name='完成', position=2)
    
    db.session.add_all([list1, list2, list3])
    db.session.commit()
    
    # 通过 Board 访问 Lists
    assert len(board.lists) == 3
    assert list1 in board.lists
    assert list2 in board.lists
    assert list3 in board.lists
    
    # 通过 List 访问 Board
    assert list1.board == board
    assert list2.board == board
    assert list3.board == board


def test_list_card_relationship(app_context):
    """测试 List 与 Card 的关系"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 创建多个卡片
    card1 = Card(list_id=list_obj.id, title='任务1', position=0)
    card2 = Card(list_id=list_obj.id, title='任务2', position=1)
    
    db.session.add_all([card1, card2])
    db.session.commit()
    
    # 通过 List 访问 Cards
    assert len(list_obj.cards) == 2
    assert card1 in list_obj.cards
    assert card2 in list_obj.cards
    
    # 通过 Card 访问 List
    assert card1.list == list_obj
    assert card2.list == list_obj


def test_list_cascade_delete(app_context):
    """测试删除列表时级联删除卡片"""
    # 创建看板、列表和卡片
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    card1 = Card(list_id=list_obj.id, title='任务1', position=0)
    card2 = Card(list_id=list_obj.id, title='任务2', position=1)
    db.session.add_all([card1, card2])
    db.session.commit()
    
    card1_id = card1.id
    card2_id = card2.id
    
    # 删除列表
    db.session.delete(list_obj)
    db.session.commit()
    
    # 验证卡片也被删除
    assert Card.query.get(card1_id) is None
    assert Card.query.get(card2_id) is None


def test_board_cascade_delete_to_lists_and_cards(app_context):
    """测试删除看板时级联删除列表和卡片"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建列表
    list1 = List(board_id=board.id, name='待办', position=0)
    list2 = List(board_id=board.id, name='进行中', position=1)
    db.session.add_all([list1, list2])
    db.session.commit()
    
    # 创建卡片
    card1 = Card(list_id=list1.id, title='任务1', position=0)
    card2 = Card(list_id=list2.id, title='任务2', position=0)
    db.session.add_all([card1, card2])
    db.session.commit()
    
    list1_id = list1.id
    list2_id = list2.id
    card1_id = card1.id
    card2_id = card2.id
    
    # 删除看板
    db.session.delete(board)
    db.session.commit()
    
    # 验证列表和卡片都被删除
    assert List.query.get(list1_id) is None
    assert List.query.get(list2_id) is None
    assert Card.query.get(card1_id) is None
    assert Card.query.get(card2_id) is None


def test_list_repr(app_context):
    """测试 List 模型的字符串表示"""
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    repr_str = repr(list_obj)
    assert 'List' in repr_str
    assert str(list_obj.id) in repr_str
    assert '待办事项' in repr_str


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
