"""
运行手动 API 测试的脚本

使用 SQLite 内存数据库进行测试，无需 MySQL
"""

import os
import sys
import threading
import time
from flask import Flask

# 设置测试环境
os.environ['FLASK_ENV'] = 'testing'

# 导入应用
from app import app, db
from test_all_apis_manual import main as run_tests


def run_flask_app():
    """在后台线程运行 Flask 应用"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)


if __name__ == '__main__':
    print("正在启动 Flask 应用（使用 SQLite 内存数据库）...")
    
    # 创建应用上下文
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表已创建")
    
    # 在后台线程启动 Flask 应用
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    print("\n开始运行 API 测试...\n")
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n测试被中断")
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试完成，按 Ctrl+C 退出...")
    try:
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n退出")
        sys.exit(0)
