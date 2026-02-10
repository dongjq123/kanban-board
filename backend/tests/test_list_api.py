"""
列表 API 单元测试

本模块测试列表相关的 API 端点，包括：
- 获取看板下的所有列表
- 创建新列表
- 获取指定列表
- 更新列表
- 删除列表
- 更新列表位置

需求：2.1, 2.2, 2.3, 2.4, 2.6
"""

import pytest
from models.board import Board
from models.list import List


def test_get_board_lists_empty(client, db):
    """测试获取空看板的列表"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 获取列表
    response = client.get(f'/api/boards/{board.id}/lists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'lists' in data
    assert len(data['lists']) == 0


def test_get_board_lists_with_data(client, db):
    """测试获取包含列表的看板"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建列表
    list1 = List(board_id=board.id, name='待办', position=0)
    list2 = List(board_id=board.id, name='进行中', position=1)
    list3 = List(board_id=board.id, name='完成', position=2)
    db.session.add_all([list1, list2, list3])
    db.session.commit()
    
    # 获取列表
    response = client.get(f'/api/boards/{board.id}/lists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'lists' in data
    assert len(data['lists']) == 3
    # 验证按 position 排序
    assert data['lists'][0]['name'] == '待办'
    assert data['lists'][1]['name'] == '进行中'
    assert data['lists'][2]['name'] == '完成'


def test_get_board_lists_nonexistent_board(client):
    """测试获取不存在的看板的列表"""
    response = client.get('/api/boards/99999/lists')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_create_list_success(client, db):
    """测试成功创建列表"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建列表
    response = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '待办事项'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == '待办事项'
    assert data['board_id'] == board.id
    assert data['position'] == 0
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_list_with_position(client, db):
    """测试创建列表时指定位置"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建列表并指定位置
    response = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '待办事项',
        'position': 5
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['position'] == 5


def test_create_list_auto_position(client, db):
    """测试创建列表时自动分配位置"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 创建第一个列表
    response1 = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '列表1'
    })
    assert response1.status_code == 201
    assert response1.get_json()['position'] == 0
    
    # 创建第二个列表
    response2 = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '列表2'
    })
    assert response2.status_code == 201
    assert response2.get_json()['position'] == 1
    
    # 创建第三个列表
    response3 = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '列表3'
    })
    assert response3.status_code == 201
    assert response3.get_json()['position'] == 2


def test_create_list_empty_name(client, db):
    """测试创建列表时名称为空"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 尝试创建空名称的列表
    response = client.post(f'/api/boards/{board.id}/lists', json={
        'name': ''
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_create_list_whitespace_name(client, db):
    """测试创建列表时名称仅包含空白字符"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 尝试创建仅包含空白字符的列表
    response = client.post(f'/api/boards/{board.id}/lists', json={
        'name': '   '
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_create_list_missing_name(client, db):
    """测试创建列表时缺少名称字段"""
    # 创建看板
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    # 尝试创建缺少名称的列表
    response = client.post(f'/api/boards/{board.id}/lists', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_create_list_nonexistent_board(client):
    """测试在不存在的看板中创建列表"""
    response = client.post('/api/boards/99999/lists', json={
        'name': '待办事项'
    })
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_get_list_success(client, db):
    """测试成功获取列表"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 获取列表
    response = client.get(f'/api/lists/{list_obj.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == list_obj.id
    assert data['name'] == '待办事项'
    assert data['board_id'] == board.id
    assert data['position'] == 0


def test_get_list_nonexistent(client):
    """测试获取不存在的列表"""
    response = client.get('/api/lists/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_list_name(client, db):
    """测试更新列表名称"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 更新列表名称
    response = client.put(f'/api/lists/{list_obj.id}', json={
        'name': '新的名称'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == '新的名称'
    assert data['id'] == list_obj.id


def test_update_list_empty_name(client, db):
    """测试更新列表时名称为空"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 尝试更新为空名称
    response = client.put(f'/api/lists/{list_obj.id}', json={
        'name': ''
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_update_list_nonexistent(client):
    """测试更新不存在的列表"""
    response = client.put('/api/lists/99999', json={
        'name': '新名称'
    })
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_delete_list_success(client, db):
    """测试成功删除列表"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    list_id = list_obj.id
    
    # 删除列表
    response = client.delete(f'/api/lists/{list_id}')
    assert response.status_code == 204
    
    # 验证列表已删除
    response = client.get(f'/api/lists/{list_id}')
    assert response.status_code == 404


def test_delete_list_nonexistent(client):
    """测试删除不存在的列表"""
    response = client.delete('/api/lists/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_list_position_success(client, db):
    """测试成功更新列表位置"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 更新位置
    response = client.put(f'/api/lists/{list_obj.id}/position', json={
        'position': 5
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['position'] == 5
    assert data['id'] == list_obj.id


def test_update_list_position_missing_field(client, db):
    """测试更新列表位置时缺少 position 字段"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 尝试更新位置但缺少字段
    response = client.put(f'/api/lists/{list_obj.id}/position', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_update_list_position_negative(client, db):
    """测试更新列表位置为负数"""
    # 创建看板和列表
    board = Board(name='测试看板')
    db.session.add(board)
    db.session.commit()
    
    list_obj = List(board_id=board.id, name='待办事项', position=0)
    db.session.add(list_obj)
    db.session.commit()
    
    # 尝试更新为负数位置
    response = client.put(f'/api/lists/{list_obj.id}/position', json={
        'position': -1
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_update_list_position_nonexistent(client):
    """测试更新不存在的列表的位置"""
    response = client.put('/api/lists/99999/position', json={
        'position': 5
    })
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'
