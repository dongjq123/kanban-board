"""
手动测试看板 API 的脚本

用于验证看板 API 端点是否正常工作
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api/boards'


def test_board_api():
    """测试看板 API 的完整流程"""
    
    print("=" * 60)
    print("测试看板 API")
    print("=" * 60)
    
    # 1. 获取所有看板（应该为空）
    print("\n1. 获取所有看板（初始状态）")
    response = requests.get(BASE_URL)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 2. 创建新看板
    print("\n2. 创建新看板")
    board_data = {'name': '项目开发看板'}
    response = requests.post(BASE_URL, json=board_data)
    print(f"状态码: {response.status_code}")
    board = response.json()
    print(f"响应: {json.dumps(board, indent=2, ensure_ascii=False)}")
    board_id = board['id']
    
    # 3. 获取指定看板
    print(f"\n3. 获取看板 ID={board_id}")
    response = requests.get(f"{BASE_URL}/{board_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 4. 更新看板名称
    print(f"\n4. 更新看板 ID={board_id} 的名称")
    update_data = {'name': '更新后的看板名称'}
    response = requests.put(f"{BASE_URL}/{board_id}", json=update_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 5. 创建多个看板
    print("\n5. 创建多个看板")
    for i in range(2, 4):
        board_data = {'name': f'看板 {i}'}
        response = requests.post(BASE_URL, json=board_data)
        print(f"创建看板 {i}: 状态码 {response.status_code}")
    
    # 6. 获取所有看板
    print("\n6. 获取所有看板")
    response = requests.get(BASE_URL)
    print(f"状态码: {response.status_code}")
    boards = response.json()['boards']
    print(f"看板数量: {len(boards)}")
    for board in boards:
        print(f"  - ID={board['id']}, 名称={board['name']}")
    
    # 7. 测试验证错误（空名称）
    print("\n7. 测试验证错误（空名称）")
    response = requests.post(BASE_URL, json={'name': ''})
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 8. 测试 404 错误（不存在的看板）
    print("\n8. 测试 404 错误（不存在的看板）")
    response = requests.get(f"{BASE_URL}/99999")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 9. 删除看板
    print(f"\n9. 删除看板 ID={board_id}")
    response = requests.delete(f"{BASE_URL}/{board_id}")
    print(f"状态码: {response.status_code}")
    
    # 10. 验证看板已删除
    print(f"\n10. 验证看板 ID={board_id} 已删除")
    response = requests.get(f"{BASE_URL}/{board_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_board_api()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器")
        print("请确保 Flask 应用正在运行: python app.py")
    except Exception as e:
        print(f"错误: {e}")
