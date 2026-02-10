"""
看板 API 单元测试

测试看板相关的 API 端点，包括：
- 创建看板
- 获取所有看板
- 获取指定看板
- 更新看板
- 删除看板
- 输入验证
- 错误处理

需求：1.1, 1.2, 1.3, 1.4, 1.5, 1.6
"""

import pytest
import json


class TestBoardAPI:
    """看板 API 测试类"""
    
    def test_get_boards_without_auth_returns_401(self, client):
        """
        测试未认证访问看板列表返回 401 错误
        
        需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
        """
        response = client.get('/api/boards')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
    
    def test_create_board_without_auth_returns_401(self, client):
        """
        测试未认证创建看板返回 401 错误
        
        需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
    
    def test_get_board_without_auth_returns_401(self, client):
        """
        测试未认证获取看板返回 401 错误
        
        需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
        """
        response = client.get('/api/boards/1')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
    
    def test_update_board_without_auth_returns_401(self, client):
        """
        测试未认证更新看板返回 401 错误
        
        需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
        """
        response = client.put(
            '/api/boards/1',
            data=json.dumps({'name': '新名称'}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
    
    def test_delete_board_without_auth_returns_401(self, client):
        """
        测试未认证删除看板返回 401 错误
        
        需求：6.5 - WHEN 所有现有的看板、列表、卡片 API 端点被调用 THEN API 权限验证器 SHALL 验证用户身份
        需求：3.4 - WHEN 用户发送不包含会话令牌的请求到受保护的 API THEN 认证系统 SHALL 拒绝访问并返回"未授权"错误
        """
        response = client.delete('/api/boards/1')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'UNAUTHORIZED'
    
    def test_create_board_success(self, client, auth_headers):
        """
        测试成功创建看板
        
        需求：1.1 - THE System SHALL 允许用户创建新的看板
        需求：1.2 - WHEN 用户创建看板时，THE System SHALL 要求提供看板名称
        需求：4.3 - WHEN 用户创建新看板、列表或卡片 THEN 认证系统 SHALL 自动关联该资源到当前用户
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['name'] == '测试看板'
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_board_with_whitespace_trimmed(self, client, auth_headers):
        """
        测试创建看板时自动去除首尾空白
        
        需求：1.1, 1.2
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': '  测试看板  '}),
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == '测试看板'
    
    def test_create_board_with_empty_name_returns_400(self, client, auth_headers):
        """
        测试空名称创建看板返回 400 错误
        
        需求：1.2 - WHEN 用户创建看板时，THE System SHALL 要求提供看板名称
        需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': ''}),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert '看板名称' in data['error']['message']
    
    def test_create_board_with_whitespace_only_name_returns_400(self, client, auth_headers):
        """
        测试仅包含空白字符的名称创建看板返回 400 错误
        
        需求：1.2, 10.3
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': '   '}),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_create_board_without_name_field_returns_400(self, client, auth_headers):
        """
        测试缺少 name 字段创建看板返回 400 错误
        
        需求：1.2, 10.3
        """
        response = client.post(
            '/api/boards',
            data=json.dumps({}),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert 'name' in data['error']['message']
    
    def test_create_board_with_long_name(self, client, auth_headers):
        """
        测试创建包含长名称的看板
        
        需求：1.1, 1.2
        """
        long_name = 'A' * 255
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': long_name}),
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == long_name
    
    def test_create_board_with_too_long_name_returns_400(self, client, auth_headers):
        """
        测试创建超长名称的看板返回 400 错误
        
        需求：1.2, 10.3
        """
        too_long_name = 'A' * 256
        response = client.post(
            '/api/boards',
            data=json.dumps({'name': too_long_name}),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_get_all_boards_empty(self, client, auth_headers):
        """
        测试获取空看板列表
        
        需求：1.3 - THE System SHALL 允许用户查看所有已创建的看板列表
        需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
        """
        response = client.get('/api/boards', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'boards' in data
        assert data['boards'] == []
    
    def test_get_all_boards_with_multiple_boards(self, client, auth_headers):
        """
        测试获取多个看板
        
        需求：1.3, 4.1
        """
        # 创建多个看板
        board_names = ['看板1', '看板2', '看板3']
        for name in board_names:
            client.post(
                '/api/boards',
                data=json.dumps({'name': name}),
                headers=auth_headers
            )
        
        # 获取所有看板
        response = client.get('/api/boards', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'boards' in data
        assert len(data['boards']) == 3
        
        # 验证所有看板都被返回（不严格要求顺序，因为创建时间可能相同）
        returned_names = [board['name'] for board in data['boards']]
        assert set(returned_names) == set(board_names)
    
    def test_get_board_by_id_success(self, client, auth_headers):
        """
        测试成功获取指定看板
        
        需求：1.3, 4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户
        """
        # 创建看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 获取看板
        response = client.get(f'/api/boards/{board_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == board_id
        assert data['name'] == '测试看板'
    
    def test_get_nonexistent_board_returns_404(self, client, auth_headers):
        """
        测试查询不存在的看板返回 404 错误
        
        需求：10.1 - WHEN 网络请求失败时，THE System SHALL 显示网络错误提示
        """
        response = client.get('/api/boards/99999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'NOT_FOUND'
        assert '看板不存在' in data['error']['message']
    
    def test_update_board_name_success(self, client, auth_headers):
        """
        测试成功更新看板名称
        
        需求：1.4 - THE System SHALL 允许用户编辑看板名称
        需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
        需求：5.1 - WHEN 用户创建、修改或删除看板时，THE System SHALL 立即将变更保存到数据库
        """
        # 创建看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '原始名称'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 更新看板名称
        response = client.put(
            f'/api/boards/{board_id}',
            data=json.dumps({'name': '更新后的名称'}),
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == board_id
        assert data['name'] == '更新后的名称'
        
        # 验证更新已持久化
        get_response = client.get(f'/api/boards/{board_id}', headers=auth_headers)
        assert get_response.get_json()['name'] == '更新后的名称'
    
    def test_update_board_with_empty_name_returns_400(self, client, auth_headers):
        """
        测试用空名称更新看板返回 400 错误
        
        需求：1.4, 10.3
        """
        # 创建看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '原始名称'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 尝试用空名称更新
        response = client.put(
            f'/api/boards/{board_id}',
            data=json.dumps({'name': ''}),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_update_nonexistent_board_returns_404(self, client, auth_headers):
        """
        测试更新不存在的看板返回 404 错误
        
        需求：10.1
        """
        response = client.put(
            '/api/boards/99999',
            data=json.dumps({'name': '新名称'}),
            headers=auth_headers
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_delete_board_success(self, client, auth_headers):
        """
        测试成功删除看板
        
        需求：1.5 - THE System SHALL 允许用户删除看板
        需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
        需求：5.1 - WHEN 用户创建、修改或删除看板时，THE System SHALL 立即将变更保存到数据库
        """
        # 创建看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '待删除看板'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 删除看板
        response = client.delete(f'/api/boards/{board_id}', headers=auth_headers)
        
        assert response.status_code == 204
        assert response.data == b''
        
        # 验证看板已被删除
        get_response = client.get(f'/api/boards/{board_id}', headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_board_returns_404(self, client, auth_headers):
        """
        测试删除不存在的看板返回 404 错误
        
        需求：10.1
        """
        response = client.delete('/api/boards/99999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_delete_board_cascades_to_lists_and_cards(self, client, auth_headers):
        """
        测试删除看板时级联删除列表和卡片
        
        需求：1.6 - WHEN 用户删除看板时，THE System SHALL 同时删除该看板下的所有列表和卡片
        需求：7.5 - WHEN 删除看板时，THE Database SHALL 级联删除相关的列表和卡片
        """
        # 创建看板
        board_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            headers=auth_headers
        )
        board_id = board_response.get_json()['id']
        
        # 创建列表
        list_response = client.post(
            f'/api/boards/{board_id}/lists',
            data=json.dumps({'name': '测试列表', 'position': 0}),
            headers=auth_headers
        )
        list_id = list_response.get_json()['id']
        
        # 创建卡片
        card_response = client.post(
            f'/api/lists/{list_id}/cards',
            data=json.dumps({'title': '测试卡片', 'position': 0}),
            headers=auth_headers
        )
        card_id = card_response.get_json()['id']
        
        # 删除看板
        delete_response = client.delete(f'/api/boards/{board_id}', headers=auth_headers)
        assert delete_response.status_code == 204
        
        # 验证看板已被删除
        board_get_response = client.get(f'/api/boards/{board_id}', headers=auth_headers)
        assert board_get_response.status_code == 404
        
        # 验证列表已被级联删除
        list_get_response = client.get(f'/api/lists/{list_id}', headers=auth_headers)
        assert list_get_response.status_code == 404
        
        # 验证卡片已被级联删除
        card_get_response = client.get(f'/api/cards/{card_id}', headers=auth_headers)
        assert card_get_response.status_code == 404
    
    def test_board_timestamps(self, client, auth_headers):
        """
        测试看板的时间戳字段
        
        需求：7.1 - THE Database SHALL 包含 boards 表存储看板信息
        """
        # 创建看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '测试看板'}),
            headers=auth_headers
        )
        
        data = create_response.get_json()
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['created_at'] is not None
        assert data['updated_at'] is not None
    
    def test_user_can_only_see_own_boards(self, client, app, db, auth_headers):
        """
        测试用户只能看到自己的看板（用户数据隔离）
        
        需求：4.1 - WHEN 用户请求看板列表 THEN 认证系统 SHALL 只返回该用户创建的看板
        """
        from models.user import User
        from services.auth_service import AuthService
        
        # 创建第一个用户的看板
        client.post(
            '/api/boards',
            data=json.dumps({'name': '用户1的看板'}),
            headers=auth_headers
        )
        
        # 创建第二个用户
        with app.app_context():
            user2 = User(username='testuser2', email='test2@example.com')
            user2.set_password('testpassword123')
            db.session.add(user2)
            db.session.commit()
            
            # 生成第二个用户的令牌
            auth_service = AuthService(
                secret_key=app.config['SECRET_KEY'],
                token_expiration_hours=24
            )
            token2 = auth_service.generate_token(user2.id)
        
        auth_headers2 = {
            'Authorization': f'Bearer {token2}',
            'Content-Type': 'application/json'
        }
        
        # 创建第二个用户的看板
        client.post(
            '/api/boards',
            data=json.dumps({'name': '用户2的看板'}),
            headers=auth_headers2
        )
        
        # 验证用户1只能看到自己的看板
        response1 = client.get('/api/boards', headers=auth_headers)
        data1 = response1.get_json()
        assert len(data1['boards']) == 1
        assert data1['boards'][0]['name'] == '用户1的看板'
        
        # 验证用户2只能看到自己的看板
        response2 = client.get('/api/boards', headers=auth_headers2)
        data2 = response2.get_json()
        assert len(data2['boards']) == 1
        assert data2['boards'][0]['name'] == '用户2的看板'
    
    def test_user_cannot_access_other_users_board(self, client, app, db, auth_headers):
        """
        测试用户无法访问其他用户的看板
        
        需求：4.2 - WHEN 用户请求特定看板的详情 THEN 认证系统 SHALL 验证该看板属于该用户，否则返回"无权访问"错误
        """
        from models.user import User
        from services.auth_service import AuthService
        
        # 创建第一个用户的看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '用户1的看板'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 创建第二个用户
        with app.app_context():
            user2 = User(username='testuser2', email='test2@example.com')
            user2.set_password('testpassword123')
            db.session.add(user2)
            db.session.commit()
            
            # 生成第二个用户的令牌
            auth_service = AuthService(
                secret_key=app.config['SECRET_KEY'],
                token_expiration_hours=24
            )
            token2 = auth_service.generate_token(user2.id)
        
        auth_headers2 = {
            'Authorization': f'Bearer {token2}',
            'Content-Type': 'application/json'
        }
        
        # 用户2尝试访问用户1的看板
        response = client.get(f'/api/boards/{board_id}', headers=auth_headers2)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'FORBIDDEN'
    
    def test_user_cannot_update_other_users_board(self, client, app, db, auth_headers):
        """
        测试用户无法修改其他用户的看板
        
        需求：4.4 - WHEN 用户尝试修改不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
        """
        from models.user import User
        from services.auth_service import AuthService
        
        # 创建第一个用户的看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '用户1的看板'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 创建第二个用户
        with app.app_context():
            user2 = User(username='testuser2', email='test2@example.com')
            user2.set_password('testpassword123')
            db.session.add(user2)
            db.session.commit()
            
            # 生成第二个用户的令牌
            auth_service = AuthService(
                secret_key=app.config['SECRET_KEY'],
                token_expiration_hours=24
            )
            token2 = auth_service.generate_token(user2.id)
        
        auth_headers2 = {
            'Authorization': f'Bearer {token2}',
            'Content-Type': 'application/json'
        }
        
        # 用户2尝试修改用户1的看板
        response = client.put(
            f'/api/boards/{board_id}',
            data=json.dumps({'name': '被修改的名称'}),
            headers=auth_headers2
        )
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'FORBIDDEN'
    
    def test_user_cannot_delete_other_users_board(self, client, app, db, auth_headers):
        """
        测试用户无法删除其他用户的看板
        
        需求：4.5 - WHEN 用户尝试删除不属于自己的资源 THEN 认证系统 SHALL 拒绝操作并返回"无权访问"错误
        """
        from models.user import User
        from services.auth_service import AuthService
        
        # 创建第一个用户的看板
        create_response = client.post(
            '/api/boards',
            data=json.dumps({'name': '用户1的看板'}),
            headers=auth_headers
        )
        board_id = create_response.get_json()['id']
        
        # 创建第二个用户
        with app.app_context():
            user2 = User(username='testuser2', email='test2@example.com')
            user2.set_password('testpassword123')
            db.session.add(user2)
            db.session.commit()
            
            # 生成第二个用户的令牌
            auth_service = AuthService(
                secret_key=app.config['SECRET_KEY'],
                token_expiration_hours=24
            )
            token2 = auth_service.generate_token(user2.id)
        
        auth_headers2 = {
            'Authorization': f'Bearer {token2}',
            'Content-Type': 'application/json'
        }
        
        # 用户2尝试删除用户1的看板
        response = client.delete(f'/api/boards/{board_id}', headers=auth_headers2)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert data['error']['code'] == 'FORBIDDEN'
