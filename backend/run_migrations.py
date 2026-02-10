"""
运行所有数据库迁移
"""

from flask import Flask
from config import get_config, db
from migrations import create_users_table, add_user_id_to_boards

def create_app(env='development'):
    """创建 Flask 应用实例"""
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)
    return app

def main():
    """运行所有迁移"""
    app = create_app('development')
    
    with app.app_context():
        try:
            print("正在创建 users 表...")
            create_users_table()
            print("✓ users 表创建成功！")
            
            print("正在为 boards 表添加 user_id 列...")
            add_user_id_to_boards()
            print("✓ user_id 列添加成功！")
            
            print("\n✓ 所有迁移执行成功！")
        except Exception as e:
            print(f"✗ 迁移失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
