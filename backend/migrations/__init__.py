"""
数据库迁移模块

本模块提供数据库初始化和迁移功能，包括：
- 创建所有表结构
- 执行 SQL 迁移脚本
- 数据库初始化函数

需求：7.1, 7.2, 7.3, 7.4
"""

import os
from pathlib import Path
from sqlalchemy import text
from config import db


def get_migration_path():
    """
    获取迁移脚本目录路径
    
    Returns:
        Path: 迁移脚本目录的绝对路径
    """
    return Path(__file__).parent


def execute_sql_file(sql_file_path):
    """
    执行 SQL 文件中的所有语句
    
    Args:
        sql_file_path: SQL 文件路径
        
    Raises:
        FileNotFoundError: 如果 SQL 文件不存在
        Exception: 如果执行 SQL 语句失败
    """
    if not os.path.exists(sql_file_path):
        raise FileNotFoundError(f"SQL 文件不存在: {sql_file_path}")
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 分割 SQL 语句（按分号分割，忽略注释）
    statements = []
    current_statement = []
    
    for line in sql_content.split('\n'):
        # 跳过空行和注释行
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('--'):
            continue
        
        current_statement.append(line)
        
        # 如果行以分号结尾，表示一个完整的语句
        if stripped_line.endswith(';'):
            statement = '\n'.join(current_statement)
            statements.append(statement)
            current_statement = []
    
    # 执行所有语句
    for statement in statements:
        if statement.strip():
            db.session.execute(text(statement))
    
    db.session.commit()


def init_database():
    """
    初始化数据库
    
    使用 SQLAlchemy 的 create_all() 方法创建所有表。
    这个方法会根据模型定义自动创建表结构。
    
    注意：这个方法适用于开发和测试环境。
    生产环境建议使用 SQL 迁移脚本以便更好地控制数据库变更。
    """
    # 导入所有模型以确保它们被注册到 SQLAlchemy
    from models.board import Board
    from models.list import List
    from models.card import Card
    from models.user import User
    
    # 创建所有表
    db.create_all()
    db.session.commit()


def init_database_from_sql():
    """
    从 SQL 迁移脚本初始化数据库
    
    执行 001_create_tables.sql 脚本创建所有表结构。
    这个方法适用于生产环境，提供更精确的数据库控制。
    """
    migration_path = get_migration_path()
    sql_file = migration_path / '001_create_tables.sql'
    execute_sql_file(sql_file)


def create_users_table():
    """
    创建 users 表
    
    执行 002_create_users_table.sql 脚本创建用户认证表。
    需求：9.1, 9.3
    """
    migration_path = get_migration_path()
    sql_file = migration_path / '002_create_users_table.sql'
    execute_sql_file(sql_file)


def add_user_id_to_boards():
    """
    在 boards 表添加 user_id 外键
    
    执行 003_add_user_id_to_boards.sql 脚本为 boards 表添加 user_id 列。
    需求：9.2, 9.4
    """
    migration_path = get_migration_path()
    sql_file = migration_path / '003_add_user_id_to_boards.sql'
    execute_sql_file(sql_file)


def drop_all_tables():
    """
    删除所有表
    
    警告：这个操作会删除所有数据！仅用于开发和测试环境。
    """
    db.drop_all()
    db.session.commit()


def reset_database():
    """
    重置数据库
    
    删除所有表并重新创建。
    警告：这个操作会删除所有数据！仅用于开发和测试环境。
    """
    drop_all_tables()
    init_database()


def reset_database_from_sql():
    """
    从 SQL 脚本重置数据库
    
    执行回滚脚本删除所有表，然后执行创建脚本重新创建表。
    警告：这个操作会删除所有数据！仅用于开发和测试环境。
    """
    migration_path = get_migration_path()
    
    # 执行回滚脚本
    rollback_file = migration_path / '001_create_tables_rollback.sql'
    try:
        execute_sql_file(rollback_file)
    except Exception as e:
        print(f"回滚脚本执行失败（可能表不存在）: {e}")
    
    # 执行创建脚本
    init_database_from_sql()
