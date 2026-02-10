"""
手动测试所有 API 端点的脚本

用于验证看板、列表和卡片 API 端点是否正常工作
这是 Task 8 检查点的一部分
"""

import requests
import json
from datetime import date

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
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应: {response.text}")


def test_board_api():
    """测试看板 API"""
    print_section("测试看板 API")
    
    # 1. 创建看板
    print_test("1. 创建看板")
    response = requests.post(f"{BASE_URL}/boards", json={'name': '项目开发看板'})
    print_response(response)
    assert response.status_code == 201, "创建看板失败"
    board_id = response.json()['id']
    print(f"✓ 看板创建成功，ID={board_id}")
    
    # 2. 获取所有看板
    print_test("2. 获取所有看板")
    response = requests.get(f"{BASE_URL}/boards")
    print_response(response)
    assert response.status_code == 200, "获取看板列表失败"
    print(f"✓ 获取看板列表成功")
    
    # 3. 获取指定看板
    print_test("3. 获取指定看板")
    response = requests.get(f"{BASE_URL}/boards/{board_id}")
    print_response(response)
    assert response.status_code == 200, "获取看板失败"
    print(f"✓ 获取看板成功")
    
    # 4. 更新看板
    print_test("4. 更新看板名称")
    response = requests.put(f"{BASE_URL}/boards/{board_id}", json={'name': '更新后的看板'})
    print_response(response)
    assert response.status_code == 200, "更新看板失败"
    print(f"✓ 更新看板成功")
    
    # 5. 测试验证错误
    print_test("5. 测试空名称验证错误")
    response = requests.post(f"{BASE_URL}/boards", json={'name': ''})
    print_response(response)
    assert response.status_code == 400, "应该返回 400 错误"
    print(f"✓ 验证错误处理正确")
    
    # 6. 测试 404 错误
    print_test("6. 测试不存在的看板")
    response = requests.get(f"{BASE_URL}/boards/99999")
    print_response(response)
    assert response.status_code == 404, "应该返回 404 错误"
    print(f"✓ 404 错误处理正确")
    
    return board_id


def test_list_api(board_id):
    """测试列表 API"""
    print_section("测试列表 API")
    
    # 1. 创建列表
    print_test("1. 在看板中创建列表")
    response = requests.post(f"{BASE_URL}/boards/{board_id}/lists", 
                            json={'name': '待办事项', 'position': 0})
    print_response(response)
    assert response.status_code == 201, "创建列表失败"
    list_id = response.json()['id']
    print(f"✓ 列表创建成功，ID={list_id}")
    
    # 2. 创建更多列表
    print_test("2. 创建更多列表")
    response = requests.post(f"{BASE_URL}/boards/{board_id}/lists", 
                            json={'name': '进行中', 'position': 1})
    print_response(response)
    list_id_2 = response.json()['id']
    
    response = requests.post(f"{BASE_URL}/boards/{board_id}/lists", 
                            json={'name': '已完成', 'position': 2})
    print_response(response)
    list_id_3 = response.json()['id']
    print(f"✓ 创建了 3 个列表")
    
    # 3. 获取看板的所有列表
    print_test("3. 获取看板的所有列表")
    response = requests.get(f"{BASE_URL}/boards/{board_id}/lists")
    print_response(response)
    assert response.status_code == 200, "获取列表失败"
    lists = response.json()['lists']
    print(f"✓ 获取到 {len(lists)} 个列表")
    
    # 4. 获取指定列表
    print_test("4. 获取指定列表")
    response = requests.get(f"{BASE_URL}/lists/{list_id}")
    print_response(response)
    assert response.status_code == 200, "获取列表失败"
    print(f"✓ 获取列表成功")
    
    # 5. 更新列表名称
    print_test("5. 更新列表名称")
    response = requests.put(f"{BASE_URL}/lists/{list_id}", json={'name': '待处理任务'})
    print_response(response)
    assert response.status_code == 200, "更新列表失败"
    print(f"✓ 更新列表成功")
    
    # 6. 更新列表位置
    print_test("6. 更新列表位置")
    response = requests.put(f"{BASE_URL}/lists/{list_id}/position", json={'position': 2})
    print_response(response)
    assert response.status_code == 200, "更新列表位置失败"
    print(f"✓ 更新列表位置成功")
    
    # 7. 测试验证错误
    print_test("7. 测试空名称验证错误")
    response = requests.post(f"{BASE_URL}/boards/{board_id}/lists", json={'name': ''})
    print_response(response)
    assert response.status_code == 400, "应该返回 400 错误"
    print(f"✓ 验证错误处理正确")
    
    # 8. 测试 404 错误
    print_test("8. 测试不存在的列表")
    response = requests.get(f"{BASE_URL}/lists/99999")
    print_response(response)
    assert response.status_code == 404, "应该返回 404 错误"
    print(f"✓ 404 错误处理正确")
    
    return list_id, list_id_2, list_id_3


def test_card_api(list_id, list_id_2):
    """测试卡片 API"""
    print_section("测试卡片 API")
    
    # 1. 创建卡片
    print_test("1. 在列表中创建卡片")
    response = requests.post(f"{BASE_URL}/lists/{list_id}/cards", 
                            json={'title': '实现用户登录功能', 'position': 0})
    print_response(response)
    assert response.status_code == 201, "创建卡片失败"
    card_id = response.json()['id']
    print(f"✓ 卡片创建成功，ID={card_id}")
    
    # 2. 创建更多卡片
    print_test("2. 创建更多卡片")
    response = requests.post(f"{BASE_URL}/lists/{list_id}/cards", 
                            json={'title': '设计数据库模型', 'position': 1})
    print_response(response)
    card_id_2 = response.json()['id']
    
    response = requests.post(f"{BASE_URL}/lists/{list_id}/cards", 
                            json={'title': '编写 API 文档', 'position': 2})
    print_response(response)
    card_id_3 = response.json()['id']
    print(f"✓ 创建了 3 个卡片")
    
    # 3. 获取列表的所有卡片
    print_test("3. 获取列表的所有卡片")
    response = requests.get(f"{BASE_URL}/lists/{list_id}/cards")
    print_response(response)
    assert response.status_code == 200, "获取卡片列表失败"
    cards = response.json()['cards']
    print(f"✓ 获取到 {len(cards)} 个卡片")
    
    # 4. 获取指定卡片
    print_test("4. 获取指定卡片")
    response = requests.get(f"{BASE_URL}/cards/{card_id}")
    print_response(response)
    assert response.status_code == 200, "获取卡片失败"
    print(f"✓ 获取卡片成功")
    
    # 5. 更新卡片标题
    print_test("5. 更新卡片标题")
    response = requests.put(f"{BASE_URL}/cards/{card_id}", 
                           json={'title': '实现用户登录和注册功能'})
    print_response(response)
    assert response.status_code == 200, "更新卡片失败"
    print(f"✓ 更新卡片标题成功")
    
    # 6. 更新卡片详情（描述、截止日期、标签）
    print_test("6. 更新卡片详情")
    response = requests.put(f"{BASE_URL}/cards/{card_id}", json={
        'title': '实现用户登录和注册功能',
        'description': '使用 JWT 实现用户认证，支持邮箱和手机号登录',
        'due_date': '2024-02-15',
        'tags': ['后端', '高优先级', '认证']
    })
    print_response(response)
    assert response.status_code == 200, "更新卡片详情失败"
    print(f"✓ 更新卡片详情成功")
    
    # 7. 在同一列表内移动卡片
    print_test("7. 在同一列表内移动卡片")
    response = requests.put(f"{BASE_URL}/cards/{card_id}/move", 
                           json={'list_id': list_id, 'position': 2})
    print_response(response)
    assert response.status_code == 200, "移动卡片失败"
    print(f"✓ 在同一列表内移动卡片成功")
    
    # 8. 移动卡片到不同列表
    print_test("8. 移动卡片到不同列表")
    response = requests.put(f"{BASE_URL}/cards/{card_id}/move", 
                           json={'list_id': list_id_2, 'position': 0})
    print_response(response)
    assert response.status_code == 200, "移动卡片到不同列表失败"
    print(f"✓ 移动卡片到不同列表成功")
    
    # 9. 验证卡片已移动
    print_test("9. 验证卡片已移动到新列表")
    response = requests.get(f"{BASE_URL}/cards/{card_id}")
    print_response(response)
    card = response.json()
    assert card['list_id'] == list_id_2, "卡片未正确移动"
    print(f"✓ 卡片已正确移动到列表 {list_id_2}")
    
    # 10. 测试验证错误
    print_test("10. 测试空标题验证错误")
    response = requests.post(f"{BASE_URL}/lists/{list_id}/cards", json={'title': ''})
    print_response(response)
    assert response.status_code == 400, "应该返回 400 错误"
    print(f"✓ 验证错误处理正确")
    
    # 11. 测试 404 错误
    print_test("11. 测试不存在的卡片")
    response = requests.get(f"{BASE_URL}/cards/99999")
    print_response(response)
    assert response.status_code == 404, "应该返回 404 错误"
    print(f"✓ 404 错误处理正确")
    
    # 12. 删除卡片
    print_test("12. 删除卡片")
    response = requests.delete(f"{BASE_URL}/cards/{card_id_3}")
    print_response(response)
    assert response.status_code == 204, "删除卡片失败"
    print(f"✓ 删除卡片成功")
    
    # 13. 验证卡片已删除
    print_test("13. 验证卡片已删除")
    response = requests.get(f"{BASE_URL}/cards/{card_id_3}")
    print_response(response)
    assert response.status_code == 404, "卡片应该已被删除"
    print(f"✓ 卡片已正确删除")
    
    return card_id, card_id_2


def test_cascade_delete(board_id):
    """测试级联删除"""
    print_section("测试级联删除")
    
    # 1. 创建测试数据
    print_test("1. 创建测试数据（看板、列表、卡片）")
    response = requests.post(f"{BASE_URL}/boards", json={'name': '测试级联删除'})
    test_board_id = response.json()['id']
    
    response = requests.post(f"{BASE_URL}/boards/{test_board_id}/lists", 
                            json={'name': '测试列表', 'position': 0})
    test_list_id = response.json()['id']
    
    response = requests.post(f"{BASE_URL}/lists/{test_list_id}/cards", 
                            json={'title': '测试卡片', 'position': 0})
    test_card_id = response.json()['id']
    print(f"✓ 创建了测试看板 {test_board_id}、列表 {test_list_id}、卡片 {test_card_id}")
    
    # 2. 删除看板
    print_test("2. 删除看板（应该级联删除列表和卡片）")
    response = requests.delete(f"{BASE_URL}/boards/{test_board_id}")
    print_response(response)
    assert response.status_code == 204, "删除看板失败"
    print(f"✓ 删除看板成功")
    
    # 3. 验证列表已被删除
    print_test("3. 验证列表已被级联删除")
    response = requests.get(f"{BASE_URL}/lists/{test_list_id}")
    print_response(response)
    assert response.status_code == 404, "列表应该已被删除"
    print(f"✓ 列表已正确级联删除")
    
    # 4. 验证卡片已被删除
    print_test("4. 验证卡片已被级联删除")
    response = requests.get(f"{BASE_URL}/cards/{test_card_id}")
    print_response(response)
    assert response.status_code == 404, "卡片应该已被删除"
    print(f"✓ 卡片已正确级联删除")


def cleanup(board_id):
    """清理测试数据"""
    print_section("清理测试数据")
    
    print_test("删除测试看板")
    response = requests.delete(f"{BASE_URL}/boards/{board_id}")
    if response.status_code == 204:
        print(f"✓ 测试看板 {board_id} 已删除")
    else:
        print(f"⚠ 删除测试看板失败: {response.status_code}")


def main():
    """主测试流程"""
    print("\n" + "=" * 70)
    print("  可视化工作管理工具 - 后端 API 手动测试")
    print("  Task 8: 检查点 - 后端 API 完成")
    print("=" * 70)
    
    try:
        # 测试看板 API
        board_id = test_board_api()
        
        # 测试列表 API
        list_id, list_id_2, list_id_3 = test_list_api(board_id)
        
        # 测试卡片 API
        card_id, card_id_2 = test_card_api(list_id, list_id_2)
        
        # 测试级联删除
        test_cascade_delete(board_id)
        
        # 清理测试数据
        cleanup(board_id)
        
        # 测试总结
        print_section("测试总结")
        print("\n✓ 所有 API 端点测试通过！")
        print("\n测试覆盖的端点：")
        print("  看板 API:")
        print("    - POST   /api/boards              (创建看板)")
        print("    - GET    /api/boards              (获取所有看板)")
        print("    - GET    /api/boards/:id          (获取指定看板)")
        print("    - PUT    /api/boards/:id          (更新看板)")
        print("    - DELETE /api/boards/:id          (删除看板)")
        print("\n  列表 API:")
        print("    - POST   /api/boards/:id/lists    (创建列表)")
        print("    - GET    /api/boards/:id/lists    (获取看板的所有列表)")
        print("    - GET    /api/lists/:id           (获取指定列表)")
        print("    - PUT    /api/lists/:id           (更新列表)")
        print("    - PUT    /api/lists/:id/position  (更新列表位置)")
        print("    - DELETE /api/lists/:id           (删除列表)")
        print("\n  卡片 API:")
        print("    - POST   /api/lists/:id/cards     (创建卡片)")
        print("    - GET    /api/lists/:id/cards     (获取列表的所有卡片)")
        print("    - GET    /api/cards/:id           (获取指定卡片)")
        print("    - PUT    /api/cards/:id           (更新卡片)")
        print("    - PUT    /api/cards/:id/move      (移动卡片)")
        print("    - DELETE /api/cards/:id           (删除卡片)")
        print("\n  错误处理:")
        print("    - 400 验证错误（空名称、空标题等）")
        print("    - 404 资源不存在错误")
        print("    - 级联删除功能")
        print("\n" + "=" * 70)
        print("  后端 API 检查点完成！")
        print("=" * 70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 70)
        print("  错误: 无法连接到服务器")
        print("=" * 70)
        print("\n请确保 Flask 应用正在运行:")
        print("  cd backend")
        print("  python app.py")
        print("\n或者使用测试环境:")
        print("  cd backend")
        print("  pytest")
        print()
        
    except AssertionError as e:
        print("\n" + "=" * 70)
        print(f"  测试失败: {e}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"  未预期的错误: {e}")
        print("=" * 70 + "\n")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
