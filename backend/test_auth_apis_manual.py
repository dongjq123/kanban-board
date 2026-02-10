"""
手动测试认证相关的所有 API 端点

这个脚本测试完整的认证流程和用户隔离功能
用于 Task 7 检查点验证
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(test_name):
    """打印测试名称"""
    print(f"\n>>> {test_name}")


def print_response(response):
    """打印响应信息"""
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except:
        print(f"响应: {response.text}")
        return None


def test_auth_api():
    """测试认证 API"""
    print_section("测试认证 API")
    
    # 1. 注册用户1
    print_test("1. 注册用户1")
    response = requests.post(f"{BASE_URL}/auth/register", json={
        'username': 'testuser1',
        'email': 'test1@example.com',
        'password': 'password123'
    })
    print_response(response)
    assert response.status_code == 201, "注册用户1失败"
    print("✓ 用户1注册成功")
    
    # 2. 注册用户2
    print_test("2. 注册用户2")
    response = requests.post(f"{BASE_URL}/auth/register", json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password456'
    })
    print_response(response)
    assert response.status_code == 201, "注册用户2失败"
    print("✓ 用户2注册成功")
    
    # 3. 测试重复用户名
    print_test("3. 测试重复用户名（应该失败）")
    response = requests.post(f"{BASE_URL}/auth/register", json={
        'username': 'testuser1',
        'email': 'another@example.com',
        'password': 'password789'
    })
    print_response(response)
    assert response.status_code == 400, "应该返回400错误"
    print("✓ 重复用户名验证正确")
    
    # 4. 登录用户1
    print_test("4. 登录用户1")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        'identifier': 'test1@example.com',
        'password': 'password123'
    })
    data = print_response(response)
    assert response.status_code == 200, "登录用户1失败"
    token1 = data['token']
    user1_id = data['user']['id']
    print(f"✓ 用户1登录成功，token: {token1[:20]}...")
    
    # 5. 登录用户2
    print_test("5. 登录用户2")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        'identifier': 'test2@example.com',
        'password': 'password456'
    })
    data = print_response(response)
    assert response.status_code == 200, "登录用户2失败"
    token2 = data['token']
    user2_id = data['user']['id']
    print(f"✓ 用户2登录成功，token: {token2[:20]}...")
    
    # 6. 验证令牌
    print_test("6. 验证用户1的令牌")
    response = requests.get(f"{BASE_URL}/auth/verify", 
                           headers={'Authorization': f'Bearer {token1}'})
    print_response(response)
    assert response.status_code == 200, "令牌验证失败"
    print("✓ 令牌验证成功")
    
    # 7. 测试无效令牌
    print_test("7. 测试无效令牌（应该失败）")
    response = requests.get(f"{BASE_URL}/auth/verify", 
                           headers={'Authorization': 'Bearer invalid_token'})
    print_response(response)
    assert response.status_code == 401, "应该返回401错误"
    print("✓ 无效令牌处理正确")
    
    return token1, token2, user1_id, user2_id


def test_board_api_with_auth(token1, token2):
    """测试带认证的看板 API"""
    print_section("测试看板 API（带认证）")
    
    headers1 = {'Authorization': f'Bearer {token1}', 'Content-Type': 'application/json'}
    headers2 = {'Authorization': f'Bearer {token2}', 'Content-Type': 'application/json'}
    
    # 1. 用户1创建看板
    print_test("1. 用户1创建看板")
    response = requests.post(f"{BASE_URL}/boards", 
                            json={'name': '用户1的看板'},
                            headers=headers1)
    data = print_response(response)
    assert response.status_code == 201, "创建看板失败"
    board1_id = data['id']
    print(f"✓ 用户1创建看板成功，ID={board1_id}")
    
    # 2. 用户2创建看板
    print_test("2. 用户2创建看板")
    response = requests.post(f"{BASE_URL}/boards", 
                            json={'name': '用户2的看板'},
                            headers=headers2)
    data = print_response(response)
    assert response.status_code == 201, "创建看板失败"
    board2_id = data['id']
    print(f"✓ 用户2创建看板成功，ID={board2_id}")
    
    # 3. 用户1获取自己的看板列表
    print_test("3. 用户1获取看板列表（应该只看到自己的）")
    response = requests.get(f"{BASE_URL}/boards", headers=headers1)
    data = print_response(response)
    assert response.status_code == 200, "获取看板列表失败"
    boards = data['boards']
    assert len(boards) == 1, f"用户1应该只看到1个看板，实际看到{len(boards)}个"
    assert boards[0]['id'] == board1_id, "用户1应该只看到自己的看板"
    print("✓ 用户隔离正确：用户1只看到自己的看板")
    
    # 4. 用户2获取自己的看板列表
    print_test("4. 用户2获取看板列表（应该只看到自己的）")
    response = requests.get(f"{BASE_URL}/boards", headers=headers2)
    data = print_response(response)
    assert response.status_code == 200, "获取看板列表失败"
    boards = data['boards']
    assert len(boards) == 1, f"用户2应该只看到1个看板，实际看到{len(boards)}个"
    assert boards[0]['id'] == board2_id, "用户2应该只看到自己的看板"
    print("✓ 用户隔离正确：用户2只看到自己的看板")
    
    # 5. 用户2尝试访问用户1的看板（应该失败）
    print_test("5. 用户2尝试访问用户1的看板（应该返回403）")
    response = requests.get(f"{BASE_URL}/boards/{board1_id}", headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户访问保护正确")
    
    # 6. 用户2尝试修改用户1的看板（应该失败）
    print_test("6. 用户2尝试修改用户1的看板（应该返回403）")
    response = requests.put(f"{BASE_URL}/boards/{board1_id}", 
                           json={'name': '被篡改的看板'},
                           headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户修改保护正确")
    
    # 7. 用户2尝试删除用户1的看板（应该失败）
    print_test("7. 用户2尝试删除用户1的看板（应该返回403）")
    response = requests.delete(f"{BASE_URL}/boards/{board1_id}", headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户删除保护正确")
    
    # 8. 测试未认证访问（应该失败）
    print_test("8. 未认证访问看板列表（应该返回401）")
    response = requests.get(f"{BASE_URL}/boards")
    print_response(response)
    assert response.status_code == 401, "应该返回401未授权"
    print("✓ 未认证访问保护正确")
    
    return board1_id, board2_id


def test_list_api_with_auth(token1, token2, board1_id, board2_id):
    """测试带认证的列表 API"""
    print_section("测试列表 API（带认证）")
    
    headers1 = {'Authorization': f'Bearer {token1}', 'Content-Type': 'application/json'}
    headers2 = {'Authorization': f'Bearer {token2}', 'Content-Type': 'application/json'}
    
    # 1. 用户1在自己的看板创建列表
    print_test("1. 用户1在自己的看板创建列表")
    response = requests.post(f"{BASE_URL}/boards/{board1_id}/lists",
                            json={'name': '待办', 'position': 0},
                            headers=headers1)
    data = print_response(response)
    assert response.status_code == 201, "创建列表失败"
    list1_id = data['id']
    print(f"✓ 用户1创建列表成功，ID={list1_id}")
    
    # 2. 用户2尝试在用户1的看板创建列表（应该失败）
    print_test("2. 用户2尝试在用户1的看板创建列表（应该返回403）")
    response = requests.post(f"{BASE_URL}/boards/{board1_id}/lists",
                            json={'name': '恶意列表', 'position': 1},
                            headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户创建列表保护正确")
    
    # 3. 用户1获取列表
    print_test("3. 用户1获取自己的列表")
    response = requests.get(f"{BASE_URL}/lists/{list1_id}", headers=headers1)
    print_response(response)
    assert response.status_code == 200, "获取列表失败"
    print("✓ 用户1获取列表成功")
    
    # 4. 用户2尝试获取用户1的列表（应该失败）
    print_test("4. 用户2尝试获取用户1的列表（应该返回403）")
    response = requests.get(f"{BASE_URL}/lists/{list1_id}", headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户访问列表保护正确")
    
    # 5. 用户1更新列表
    print_test("5. 用户1更新自己的列表")
    response = requests.put(f"{BASE_URL}/lists/{list1_id}",
                           json={'name': '待处理'},
                           headers=headers1)
    print_response(response)
    assert response.status_code == 200, "更新列表失败"
    print("✓ 用户1更新列表成功")
    
    # 6. 用户2尝试更新用户1的列表（应该失败）
    print_test("6. 用户2尝试更新用户1的列表（应该返回403）")
    response = requests.put(f"{BASE_URL}/lists/{list1_id}",
                           json={'name': '被篡改的列表'},
                           headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户更新列表保护正确")
    
    return list1_id


def test_card_api_with_auth(token1, token2, list1_id):
    """测试带认证的卡片 API"""
    print_section("测试卡片 API（带认证）")
    
    headers1 = {'Authorization': f'Bearer {token1}', 'Content-Type': 'application/json'}
    headers2 = {'Authorization': f'Bearer {token2}', 'Content-Type': 'application/json'}
    
    # 1. 用户1在自己的列表创建卡片
    print_test("1. 用户1在自己的列表创建卡片")
    response = requests.post(f"{BASE_URL}/lists/{list1_id}/cards",
                            json={'title': '实现登录功能', 'position': 0},
                            headers=headers1)
    data = print_response(response)
    assert response.status_code == 201, "创建卡片失败"
    card1_id = data['id']
    print(f"✓ 用户1创建卡片成功，ID={card1_id}")
    
    # 2. 用户2尝试在用户1的列表创建卡片（应该失败）
    print_test("2. 用户2尝试在用户1的列表创建卡片（应该返回403）")
    response = requests.post(f"{BASE_URL}/lists/{list1_id}/cards",
                            json={'title': '恶意卡片', 'position': 1},
                            headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户创建卡片保护正确")
    
    # 3. 用户1获取卡片
    print_test("3. 用户1获取自己的卡片")
    response = requests.get(f"{BASE_URL}/cards/{card1_id}", headers=headers1)
    print_response(response)
    assert response.status_code == 200, "获取卡片失败"
    print("✓ 用户1获取卡片成功")
    
    # 4. 用户2尝试获取用户1的卡片（应该失败）
    print_test("4. 用户2尝试获取用户1的卡片（应该返回403）")
    response = requests.get(f"{BASE_URL}/cards/{card1_id}", headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户访问卡片保护正确")
    
    # 5. 用户1更新卡片
    print_test("5. 用户1更新自己的卡片")
    response = requests.put(f"{BASE_URL}/cards/{card1_id}",
                           json={
                               'title': '实现用户登录和注册',
                               'description': '使用JWT认证',
                               'tags': ['后端', '高优先级']
                           },
                           headers=headers1)
    print_response(response)
    assert response.status_code == 200, "更新卡片失败"
    print("✓ 用户1更新卡片成功")
    
    # 6. 用户2尝试更新用户1的卡片（应该失败）
    print_test("6. 用户2尝试更新用户1的卡片（应该返回403）")
    response = requests.put(f"{BASE_URL}/cards/{card1_id}",
                           json={'title': '被篡改的卡片'},
                           headers=headers2)
    print_response(response)
    assert response.status_code == 403, "应该返回403禁止访问"
    print("✓ 跨用户更新卡片保护正确")
    
    # 7. 用户1删除卡片
    print_test("7. 用户1删除自己的卡片")
    response = requests.delete(f"{BASE_URL}/cards/{card1_id}", headers=headers1)
    print_response(response)
    assert response.status_code == 204, "删除卡片失败"
    print("✓ 用户1删除卡片成功")
    
    # 8. 验证卡片已删除
    print_test("8. 验证卡片已删除")
    response = requests.get(f"{BASE_URL}/cards/{card1_id}", headers=headers1)
    print_response(response)
    assert response.status_code == 404, "卡片应该已被删除"
    print("✓ 卡片已正确删除")


def cleanup(token1, token2, board1_id, board2_id):
    """清理测试数据"""
    print_section("清理测试数据")
    
    headers1 = {'Authorization': f'Bearer {token1}'}
    headers2 = {'Authorization': f'Bearer {token2}'}
    
    print_test("删除用户1的看板")
    response = requests.delete(f"{BASE_URL}/boards/{board1_id}", headers=headers1)
    if response.status_code == 204:
        print(f"✓ 用户1的看板已删除")
    
    print_test("删除用户2的看板")
    response = requests.delete(f"{BASE_URL}/boards/{board2_id}", headers=headers2)
    if response.status_code == 204:
        print(f"✓ 用户2的看板已删除")


def main():
    """主测试流程"""
    print("\n" + "=" * 70)
    print("  用户认证系统 - 后端 API 手动测试")
    print("  Task 7: 检查点 - 后端功能完成")
    print("=" * 70)
    
    try:
        # 测试认证 API
        token1, token2, user1_id, user2_id = test_auth_api()
        
        # 测试看板 API（带认证和用户隔离）
        board1_id, board2_id = test_board_api_with_auth(token1, token2)
        
        # 测试列表 API（带认证和用户隔离）
        list1_id = test_list_api_with_auth(token1, token2, board1_id, board2_id)
        
        # 测试卡片 API（带认证和用户隔离）
        test_card_api_with_auth(token1, token2, list1_id)
        
        # 清理测试数据
        cleanup(token1, token2, board1_id, board2_id)
        
        # 测试总结
        print_section("测试总结")
        print("\n✅ 所有认证和用户隔离测试通过！")
        print("\n测试覆盖的功能：")
        print("  ✓ 用户注册（包括重复验证）")
        print("  ✓ 用户登录（邮箱/用户名）")
        print("  ✓ JWT令牌验证")
        print("  ✓ 无效令牌处理")
        print("  ✓ 看板API用户隔离")
        print("  ✓ 列表API用户隔离")
        print("  ✓ 卡片API用户隔离")
        print("  ✓ 跨用户访问保护（403）")
        print("  ✓ 未认证访问保护（401）")
        print("\n" + "=" * 70)
        print("  ✅ 后端认证功能检查点完成！")
        print("=" * 70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 70)
        print("  ❌ 错误: 无法连接到服务器")
        print("=" * 70)
        print("\n请确保 Flask 应用正在运行:")
        print("  cd backend")
        print("  python app.py")
        print()
        
    except AssertionError as e:
        print("\n" + "=" * 70)
        print(f"  ❌ 测试失败: {e}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"  ❌ 未预期的错误: {e}")
        print("=" * 70 + "\n")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
