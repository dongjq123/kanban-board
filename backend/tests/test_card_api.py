"""
卡片 API 单元测试

测试卡片相关的 API 端点，包括：
- 创建卡片
- 获取列表的所有卡片
- 获取指定卡片
- 更新卡片（标题、描述、截止日期、标签）
- 删除卡片
- 移动卡片（同列表内或跨列表）
- 输入验证
- 错误处理

需求：3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 4.1, 4.3
"""

import pytest
import json


class TestCardAPI:
    """卡片 API 测试类"""
    
    @pytest.fixture
    def board_and_list(self, client):
        """创建测试用的看板和列表"""
        # 创建看板
        board_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            content_type='application/json'
        )
        board_id = board_response.get_json()['id']
        
        # 创建列表
        list_response = client.post(
            f'/api/boards/{board_id}/lists',
            data=json.dumps({'name': '测试列表', 'position': 0}),
            content_type='application/json'
        )
        list_id = list_response.get_json()['id']
        
        return {'board_id': board_id, 'list_id': list_id}
    
    def test_create_card_success(self, client, board_and_list):
        """测试成功创建卡片 - 需求：3.1, 3.2, 3.3"""
        list_id = board_and_list['list_id']
        
        response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['title'] == '测试卡片'
        assert data['list_id'] == list_id
        assert data['description'] is None
        assert data['due_date'] is None
        assert data['tags'] == []
        assert data['position'] == 0
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_card_with_empty_title_returns_400(self, client, board_and_list):
        """测试空标题创建卡片返回 400 错误 - 需求：3.3, 10.3"""
        list_id = board_and_list['list_id']
        
        response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': ''}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '卡片标题' in data['error']['message']
    
    def test_get_cards_by_list_id_with_multiple_cards(self, client, board_and_list):
        """测试获取多个卡片 - 需求：3.1"""
        list_id = board_and_list['list_id']
        
        # 创建多个卡片
        card_titles = ['卡片1', '卡片2', '卡片3']
        for title in card_titles:
            client.post(
                f'/api/lists/{list_id}/cards',
                data=json.dumps({'title': title}),
                content_type='application/json'
            )
        
        # 获取所有卡片
        response = client.get(f'/api/lists/{list_id}/cards')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'cards' in data
        assert len(data['cards']) == 3
        
        # 验证卡片按位置排序
        returned_titles = [card['title'] for card in data['cards']]
        assert returned_titles == card_titles
    
    def test_get_card_by_id_success(self, client, board_and_list):
        """测试成功获取指定卡片 - 需求：3.6"""
        list_id = board_and_list['list_id']
        
        # 创建卡片
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        # 获取卡片
        response = client.get(f'/api/cards/{card_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == card_id
        assert data['title'] == '测试卡片'
    
    def test_get_nonexistent_card_returns_404(self, client):
        """测试查询不存在的卡片返回 404 错误 - 需求：10.1"""
        response = client.get('/api/cards/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_update_card_title_success(self, client, board_and_list):
        """测试成功更新卡片标题 - 需求：3.4, 5.3"""
        list_id = board_and_list['list_id']
        
        # 创建卡片
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '原始标题'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        # 更新卡片标题
        response = client.put(
            f'/api/cards/{card_id}',
            data=json.dumps({'title': '更新后的标题'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == '更新后的标题'
    
    def test_update_card_description_success(self, client, board_and_list):
        """测试成功更新卡片描述 - 需求：3.7, 5.3"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.put(
            f'/api/cards/{card_id}',
            data=json.dumps({'description': '这是卡片的详细描述'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['description'] == '这是卡片的详细描述'
    
    def test_update_card_due_date_success(self, client, board_and_list):
        """测试成功更新卡片截止日期 - 需求：3.8, 5.3"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.put(
            f'/api/cards/{card_id}',
            data=json.dumps({'due_date': '2024-01-20'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['due_date'] == '2024-01-20'
    
    def test_update_card_tags_success(self, client, board_and_list):
        """测试成功更新卡片标签 - 需求：3.9, 5.3"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.put(
            f'/api/cards/{card_id}',
            data=json.dumps({'tags': ['后端', '高优先级', '紧急']}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['tags'] == ['后端', '高优先级', '紧急']
    
    def test_update_card_all_fields_success(self, client, board_and_list):
        """测试同时更新卡片的所有字段 - 需求：3.4, 3.7, 3.8, 3.9, 5.3"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.put(
            f'/api/cards/{card_id}',
            data=json.dumps({
                'title': '更新后的标题',
                'description': '详细描述',
                'due_date': '2024-01-20',
                'tags': ['后端', '高优先级']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == '更新后的标题'
        assert data['description'] == '详细描述'
        assert data['due_date'] == '2024-01-20'
        assert data['tags'] == ['后端', '高优先级']
    
    def test_delete_card_success(self, client, board_and_list):
        """测试成功删除卡片 - 需求：3.5, 5.3"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '待删除卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.delete(f'/api/cards/{card_id}')
        
        assert response.status_code == 204
        assert response.data == b''
        
        # 验证卡片已被删除
        get_response = client.get(f'/api/cards/{card_id}')
        assert get_response.status_code == 404
    
    def test_move_card_within_same_list_success(self, client, board_and_list):
        """测试在同一列表内移动卡片 - 需求：4.1, 4.2, 4.5"""
        list_id = board_and_list['list_id']
        
        create_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        response = client.put(
            f'/api/cards/{card_id}/move',
            data=json.dumps({'list_id': list_id, 'position': 5}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['list_id'] == list_id
        assert data['position'] == 5
    
    def test_move_card_to_different_list_success(self, client, board_and_list):
        """测试将卡片移动到不同的列表 - 需求：4.3, 4.4, 4.5"""
        board_id = board_and_list['board_id']
        list1_id = board_and_list['list_id']
        
        # 创建第二个列表
        list2_response = client.post(
            f'/api/boards/{board_id}/lists',
            data=json.dumps({'name': '第二个列表', 'position': 1}),
            content_type='application/json'
        )
        list2_id = list2_response.get_json()['id']
        
        # 在第一个列表创建卡片
        create_response = client.post(
            f'/api/lists/{list1_id}/cards',
            data=json.dumps({'title': '测试卡片'}),
            content_type='application/json'
        )
        card_id = create_response.get_json()['id']
        
        # 移动卡片到第二个列表
        response = client.put(
            f'/api/cards/{card_id}/move',
            data=json.dumps({'list_id': list2_id, 'position': 0}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['list_id'] == list2_id
        assert data['position'] == 0
