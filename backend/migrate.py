#!/usr/bin/env python3
"""
数据库迁移命令行工具

提供命令行接口用于执行数据库迁移操作：
- init: 初始化数据库（使用 SQLAlchemy）
- init-sql: 从 SQL 脚本初始化数据库
- reset: 重置数据库（删除并重新创建）
- reset-sql: 从 SQL 脚本重置数据库

使用方法：
    python migrate.py init          # 使用 SQLAlchemy 初始化数据库
    python migrate.py init-sql      # 使用 SQL 脚本初始化数据库
    python migrate.py reset         # 重置数据库（开发环境）
    python migrate.py reset-sql     # 使用 SQL 脚本重置数据库

需求：7.1, 7.2, 7.3, 7.4
"""

import sys
import argparse
from flask import Flask
from config import get_config, db
from migrations import (
    init_database,
    init_database_from_sql,
    reset_database,
    reset_database_from_sql,
    drop_all_tables,
    create_users_table,
    add_user_id_to_boards
)


def create_app(env='development'):
    """
    创建 Flask 应用实例
    
    Args:
        env: 环境名称 ('development', 'testing', 'production')
    
    Returns:
        Flask: Flask 应用实例
    """
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)
    return app


def main():
    """主函数：解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(
        description='数据库迁移工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python migrate.py init          # 使用 SQLAlchemy 初始化数据库
  python migrate.py init-sql      # 使用 SQL 脚本初始化数据库
  python migrate.py reset         # 重置数据库（开发环境）
  python migrate.py reset-sql     # 使用 SQL 脚本重置数据库
  python migrate.py drop          # 删除所有表（危险操作！）
        """
    )
    
    parser.add_argument(
        'command',
        choices=['init', 'init-sql', 'reset', 'reset-sql', 'drop'],
        help='要执行的迁移命令'
    )
    
    parser.add_argument(
        '--env',
        choices=['development', 'testing', 'production'],
        default='development',
        help='运行环境（默认：development）'
    )
    
    args = parser.parse_args()
    
    # 创建 Flask 应用上下文
    app = create_app(args.env)
    
    with app.app_context():
        try:
            if args.command == 'init':
                print("正在使用 SQLAlchemy 初始化数据库...")
                init_database()
                print("✓ 数据库初始化成功！")
                
            elif args.command == 'init-sql':
                print("正在从 SQL 脚本初始化数据库...")
                init_database_from_sql()
                print("✓ 数据库初始化成功！")
                
            elif args.command == 'reset':
                if args.env == 'production':
                    print("错误：不能在生产环境执行 reset 操作！", file=sys.stderr)
                    sys.exit(1)
                
                confirm = input("警告：此操作将删除所有数据！确认继续？(yes/no): ")
                if confirm.lower() != 'yes':
                    print("操作已取消。")
                    sys.exit(0)
                
                print("正在重置数据库...")
                reset_database()
                print("✓ 数据库重置成功！")
                
            elif args.command == 'reset-sql':
                if args.env == 'production':
                    print("错误：不能在生产环境执行 reset-sql 操作！", file=sys.stderr)
                    sys.exit(1)
                
                confirm = input("警告：此操作将删除所有数据！确认继续？(yes/no): ")
                if confirm.lower() != 'yes':
                    print("操作已取消。")
                    sys.exit(0)
                
                print("正在从 SQL 脚本重置数据库...")
                reset_database_from_sql()
                print("✓ 数据库重置成功！")
                
            elif args.command == 'drop':
                if args.env == 'production':
                    print("错误：不能在生产环境执行 drop 操作！", file=sys.stderr)
                    sys.exit(1)
                
                confirm = input("警告：此操作将删除所有表和数据！确认继续？(yes/no): ")
                if confirm.lower() != 'yes':
                    print("操作已取消。")
                    sys.exit(0)
                
                print("正在删除所有表...")
                drop_all_tables()
                print("✓ 所有表已删除！")
                
        except Exception as e:
            print(f"✗ 操作失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == '__main__':
    main()
