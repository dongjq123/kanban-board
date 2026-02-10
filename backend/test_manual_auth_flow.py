"""
手动测试完整认证流程

测试步骤：
1. 注册新用户
2. 登录
3. 创建看板、列表、卡片
4. 登出
5. 重新登录验证数据存在
6. 尝试访问他人数据（应该被拒绝）

需求：所有需求
"""

import requests
import json
import time
from datetime import datetime

# 配置
BASE_URL = 'http://localhost:5000/api'
HEADERS = {'Content-Type': 'application/json'}

# 测试数据
timestamp = int(time.time())
USER1 = {
    'username': f'testuser1_{timestamp}',
    'email': f'testuser1_{timestamp}@example.com',
    'password': 'password123'
}

USER2 = {
    'username': f'testuser2_{timestamp}',
    'email': f'testuser2_{timestamp}@example.com',
    'password': 'password456'
}

def print_section(title):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_result(test_name, success, details=""):
    """打印测试结果"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"    {details}")

def test_register_user(user_data):
    """测试用户注册"""
    print_section(f"步骤 1: 注册用户 {user_data['username']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            headers=HEADERS,
            json=user_data
        )
        
        if response.status_code == 201:
            data = response.json()
            print_result("用户注册成功", True, f"用户ID: {data['user']['id']}")
            print(f"    用户名: {data['user']['username']}")
            print(f"    邮箱: {data['user']['email']}")
            return True, data['user']
        else:
            print_result("用户注册失败", False, f"状态码: {response.status_code}, 响应: {response.text}")
            return False, None
    except Exception as e:
        print_result("用户注册异常", False, str(e))
        return False, None

def test_login(identifier, password):
    """测试用户登录"""
    print_section(f"步骤 2: 登录用户 {identifier}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            headers=HEADERS,
            json={'identifier': identifier, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result("用户登录成功", True, f"获得令牌")
            print(f"    用户ID: {data['user']['id']}")
            print(f"    用户名: {data['user']['username']}")
            print(f"    令牌前缀: {data['token'][:20]}...")
            return True, data['token'], data['user']
        else:
            print_result("用户登录失败", False, f"状态码: {response.status_code}, 响应: {response.text}")
            return False, None, None
    except Exception as e:
        print_result("用户登录异常", False, str(e))
        return False, None, None

def test_create_board(token, board_name):
    """测试创建看板"""
    print_section(f"步骤 3: 创建看板 '{board_name}'")
    
    try:
        headers = HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'
        
        response = requests.post(
            f"{BASE_URL}/boards",
            headers=headers,
            json={'name': board_name}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_result("创建看板成功", True, f"看板ID: {data['id']}")
            print(f"    看板名称: {data['name']}")
            print(f"    用户ID: {data.get('user_id', 'N/A')}")
            return True, data
        else:
            print_result("创建看板失败", False, f"状态码: {response.status_code}, 响应: {response.text}")
            return False, None
    except Exception as e:
        print_result("创建看板异常", False, str(e))
        return False, None

def test_create_list(token, board_id, list_name):
    """测试创建列表"""
    print(f"\n创建列表 '{list_name}'")
    
    try:
        headers = HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'
        
        response = requests.post(
            f"{BASE_URL}/boards/{board_id}/lists",
            headers=headers,
            json={'name': list_name}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_result("创建列表成功", True, f"列表ID: {data['id']}")
            return True, data
        else:
            print_result("创建列表失败", False, f"状态码: {response.status_code}")
            return False, None
    except Exception as e:
        print_result("创建列表异常", False, str(e))
        return False, None

def test_create_card(token, list_id, card_title):
    """测试创建卡片"""
    print(f"\n创建卡片 '{card_title}'")
    
    try:
        headers = HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'
        
        response = requests.post(
            f"{BASE_URL}/lists/{list_id}/cards",
            headers=headers,
            json={'title': card_title, 'description': '测试卡片描述'}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_result("创建卡片成功", True, f"卡片ID: {data['id']}")
            return True, data
        else:
            print_result("创建卡片失败", False, f"状态码: {response.status_code}")
            return False, None
    except Exception as e:
        print_result("创建卡片异常", False, str(e))
        return False, None

def test_get_boards(token):
    """测试获取看板列表"""
    print_section("步骤 5: 重新登录后获取看板列表")
    
    try:
        headers = HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'
        
        response = requests.get(
            f"{BASE_URL}/boards",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            boards = data.get('boards', data)  # 处理可能的 {'boards': [...]} 格式
            print_result("获取看板列表成功", True, f"看板数量: {len(boards)}")
            for board in boards:
                print(f"    - 看板ID: {board['id']}, 名称: {board['name']}")
            return True, boards
        else:
            print_result("获取看板列表失败", False, f"状态码: {response.status_code}")
            return False, None
    except Exception as e:
        print_result("获取看板列表异常", False, str(e))
        return False, None

def test_access_other_user_board(token, board_id):
    """测试访问他人看板（应该被拒绝）"""
    print_section(f"步骤 6: 尝试访问他人看板 (ID: {board_id})")
    
    try:
        headers = HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'
        
        response = requests.get(
            f"{BASE_URL}/boards/{board_id}",
            headers=headers
        )
        
        if response.status_code == 403:
            print_result("正确拒绝访问他人看板", True, "返回 403 Forbidden")
            return True
        elif response.status_code == 404:
            print_result("正确拒绝访问他人看板", True, "返回 404 Not Found (也是有效的隔离方式)")
            return True
        else:
            print_result("未能正确拒绝访问", False, f"状态码: {response.status_code}, 应该返回 403 或 404")
            return False
    except Exception as e:
        print_result("访问他人看板异常", False, str(e))
        return False

def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("  用户认证系统 - 完整流程手动测试")
    print("  测试时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    # 测试结果统计
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }
    
    # ========== 用户 1 的测试流程 ==========
    
    # 1. 注册用户 1
    success, user1 = test_register_user(USER1)
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ 用户 1 注册失败，无法继续测试")
        return
    
    # 2. 登录用户 1
    success, token1, user1_info = test_login(USER1['email'], USER1['password'])
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ 用户 1 登录失败，无法继续测试")
        return
    
    # 3. 创建看板、列表、卡片
    success, board1 = test_create_board(token1, "用户1的测试看板")
    results['total'] += 1
    if success:
        results['passed'] += 1
        board1_id = board1['id']
        
        # 创建列表
        success, list1 = test_create_list(token1, board1_id, "待办事项")
        results['total'] += 1
        if success:
            results['passed'] += 1
            list1_id = list1['id']
            
            # 创建卡片
            success, card1 = test_create_card(token1, list1_id, "测试任务1")
            results['total'] += 1
            if success:
                results['passed'] += 1
            else:
                results['failed'] += 1
        else:
            results['failed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ 创建看板失败，无法继续测试")
        return
    
    # 4. 登出（前端操作，这里模拟）
    print_section("步骤 4: 登出用户 1")
    print("    (前端清除 localStorage 中的 token)")
    print_result("登出成功", True)
    
    # 5. 重新登录并验证数据存在
    success, token1_new, _ = test_login(USER1['username'], USER1['password'])
    results['total'] += 1
    if success:
        results['passed'] += 1
        
        # 获取看板列表验证数据存在
        success, boards = test_get_boards(token1_new)
        results['total'] += 1
        if success and len(boards) > 0:
            results['passed'] += 1
            # 验证之前创建的看板是否存在
            board_found = any(b['id'] == board1_id for b in boards)
            if board_found:
                print_result("验证数据持久化", True, "之前创建的看板仍然存在")
            else:
                print_result("验证数据持久化", False, "之前创建的看板未找到")
        else:
            results['failed'] += 1
    else:
        results['failed'] += 1
    
    # ========== 用户 2 的测试流程 ==========
    
    # 注册用户 2
    success, user2 = test_register_user(USER2)
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ 用户 2 注册失败，无法继续测试")
        return
    
    # 登录用户 2
    success, token2, user2_info = test_login(USER2['email'], USER2['password'])
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ 用户 2 登录失败，无法继续测试")
        return
    
    # 6. 用户 2 尝试访问用户 1 的看板（应该被拒绝）
    success = test_access_other_user_board(token2, board1_id)
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # 验证用户 2 看不到用户 1 的看板
    print_section("验证用户数据隔离")
    success, user2_boards = test_get_boards(token2)
    results['total'] += 1
    if success:
        # 用户 2 应该看不到用户 1 的看板
        user1_board_visible = any(b['id'] == board1_id for b in user2_boards)
        if not user1_board_visible:
            print_result("用户数据隔离正确", True, "用户 2 看不到用户 1 的看板")
            results['passed'] += 1
        else:
            print_result("用户数据隔离失败", False, "用户 2 可以看到用户 1 的看板")
            results['failed'] += 1
    else:
        results['failed'] += 1
    
    # ========== 测试总结 ==========
    
    print_section("测试总结")
    print(f"总测试数: {results['total']}")
    print(f"通过: {results['passed']} ✓")
    print(f"失败: {results['failed']} ✗")
    print(f"成功率: {results['passed']/results['total']*100:.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 所有测试通过！用户认证系统工作正常。")
    else:
        print(f"\n⚠️  有 {results['failed']} 个测试失败，请检查。")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
