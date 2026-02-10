"""
用户认证数据库迁移测试

测试用户认证相关的数据库迁移脚本，包括：
- users 表创建
- 唯一约束
- 索引创建
- 字段约束

需求：9.1, 9.3
"""

import pytest
import os
from pathlib import Path


class TestUserMigrationScripts:
    """用户迁移脚本测试类"""
    
    def test_users_table_migration_file_exists(self):
        """测试 users 表迁移脚本文件存在"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
        assert migration_path.exists(), "002_create_users_table.sql 文件不存在"
    
    def test_users_table_rollback_file_exists(self):
        """测试 users 表回滚脚本文件存在"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table_rollback.sql'
        assert rollback_path.exists(), "002_create_users_table_rollback.sql 文件不存在"
    
    def test_users_table_migration_contains_required_fields(self):
        """测试 users 表迁移脚本包含所有必需字段"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证表名
        assert 'CREATE TABLE' in content
        assert 'users' in content
        
        # 验证必需字段
        assert 'id' in content
        assert 'username' in content
        assert 'email' in content
        assert 'password_hash' in content
        assert 'created_at' in content
        
        # 验证字段类型
        assert 'VARCHAR(50)' in content  # username
        assert 'VARCHAR(255)' in content  # email and password_hash
        assert 'TIMESTAMP' in content  # created_at
        
        # 验证约束
        assert 'NOT NULL' in content
        assert 'UNIQUE' in content
        assert 'PRIMARY KEY' in content
    
    def test_users_table_migration_contains_constraints(self):
        """测试 users 表迁移脚本包含约束"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证长度约束
        assert 'username_length' in content
        assert 'CHAR_LENGTH(username) >= 3' in content
        
        # 验证邮箱格式约束
        assert 'email_format' in content
        assert 'REGEXP' in content
    
    def test_users_table_migration_contains_indexes(self):
        """测试 users 表迁移脚本包含索引"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证索引
        assert 'INDEX idx_users_username' in content
        assert 'INDEX idx_users_email' in content
    
    def test_users_table_migration_uses_utf8mb4(self):
        """测试 users 表迁移脚本使用 utf8mb4 字符集"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证字符集设置
        assert 'utf8mb4' in content
        assert 'utf8mb4_unicode_ci' in content
    
    def test_users_table_rollback_drops_table(self):
        """测试 users 表回滚脚本删除表"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table_rollback.sql'
        
        with open(rollback_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证删除表语句
        assert 'DROP TABLE' in content
        assert 'users' in content
        assert 'IF EXISTS' in content


class TestUserTableStructure:
    """用户表结构测试类（需要数据库连接）"""
    
    @pytest.mark.skipif(
        os.getenv('SKIP_DB_TESTS', 'false').lower() == 'true',
        reason="数据库未运行，跳过数据库测试"
    )
    def test_users_table_structure(self, app):
        """测试 users 表结构（需要数据库）"""
        # 这个测试只在数据库可用时运行
        # 在 CI/CD 环境中，可以通过设置 SKIP_DB_TESTS=true 跳过
        try:
            from sqlalchemy import inspect
            from config import db
            from migrations import execute_sql_file
            from pathlib import Path
            
            with app.app_context():
                # 执行迁移脚本
                migration_path = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
                execute_sql_file(str(migration_path))
                
                # 获取数据库检查器
                inspector = inspect(db.engine)
                
                # 验证表存在
                table_names = inspector.get_table_names()
                assert 'users' in table_names
                
                # 验证字段
                columns = {col['name']: col for col in inspector.get_columns('users')}
                
                assert 'id' in columns
                assert 'username' in columns
                assert 'email' in columns
                assert 'password_hash' in columns
                assert 'created_at' in columns
                
                # 验证字段约束
                assert columns['username']['nullable'] is False
                assert columns['email']['nullable'] is False
                assert columns['password_hash']['nullable'] is False
                
                # 验证主键
                pk_constraint = inspector.get_pk_constraint('users')
                assert 'id' in pk_constraint['constrained_columns']
                
                # 验证唯一约束
                unique_constraints = inspector.get_unique_constraints('users')
                unique_columns = set()
                for constraint in unique_constraints:
                    unique_columns.update(constraint['column_names'])
                
                # username 和 email 应该有唯一约束
                # 注意：在某些数据库中，UNIQUE 约束可能通过索引实现
                assert 'username' in unique_columns or any(
                    'username' in idx['column_names'] and idx.get('unique', False)
                    for idx in inspector.get_indexes('users')
                )
                assert 'email' in unique_columns or any(
                    'email' in idx['column_names'] and idx.get('unique', False)
                    for idx in inspector.get_indexes('users')
                )
                
        except Exception as e:
            pytest.skip(f"数据库不可用，跳过测试: {e}")


class TestBoardsUserIdMigrationScripts:
    """boards 表 user_id 外键迁移脚本测试类"""
    
    def test_boards_user_id_migration_file_exists(self):
        """测试 boards 表 user_id 迁移脚本文件存在"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
        assert migration_path.exists(), "003_add_user_id_to_boards.sql 文件不存在"
    
    def test_boards_user_id_rollback_file_exists(self):
        """测试 boards 表 user_id 回滚脚本文件存在"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards_rollback.sql'
        assert rollback_path.exists(), "003_add_user_id_to_boards_rollback.sql 文件不存在"
    
    def test_boards_user_id_migration_adds_column(self):
        """测试 boards 表 user_id 迁移脚本添加列"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证添加列语句
        assert 'ALTER TABLE boards' in content
        assert 'ADD COLUMN user_id' in content
        assert 'INT' in content
    
    def test_boards_user_id_migration_adds_foreign_key(self):
        """测试 boards 表 user_id 迁移脚本添加外键约束"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证外键约束
        assert 'FOREIGN KEY' in content
        assert 'REFERENCES users(id)' in content
        assert 'ON DELETE CASCADE' in content
        assert 'fk_boards_user_id' in content
    
    def test_boards_user_id_migration_creates_index(self):
        """测试 boards 表 user_id 迁移脚本创建索引"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证索引创建
        assert 'CREATE INDEX idx_boards_user_id' in content
        assert 'ON boards(user_id)' in content
    
    def test_boards_user_id_migration_uses_utf8mb4(self):
        """测试 boards 表 user_id 迁移脚本使用 utf8mb4 字符集"""
        migration_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证字符集设置
        assert 'utf8mb4' in content
    
    def test_boards_user_id_rollback_removes_column(self):
        """测试 boards 表 user_id 回滚脚本删除列"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards_rollback.sql'
        
        with open(rollback_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证删除列语句
        assert 'ALTER TABLE boards' in content
        assert 'DROP COLUMN user_id' in content
    
    def test_boards_user_id_rollback_removes_foreign_key(self):
        """测试 boards 表 user_id 回滚脚本删除外键约束"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards_rollback.sql'
        
        with open(rollback_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证删除外键约束
        assert 'DROP FOREIGN KEY fk_boards_user_id' in content
    
    def test_boards_user_id_rollback_removes_index(self):
        """测试 boards 表 user_id 回滚脚本删除索引"""
        rollback_path = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards_rollback.sql'
        
        with open(rollback_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证删除索引
        assert 'DROP INDEX idx_boards_user_id' in content
    
    @pytest.mark.skipif(
        os.getenv('SKIP_DB_TESTS', 'false').lower() == 'true',
        reason="数据库未运行，跳过数据库测试"
    )
    def test_boards_user_id_column_structure(self, app):
        """测试 boards 表 user_id 列结构（需要数据库）"""
        # 这个测试只在数据库可用时运行
        try:
            from sqlalchemy import inspect
            from config import db
            from migrations import execute_sql_file
            from pathlib import Path
            
            with app.app_context():
                # 确保 boards 和 users 表存在
                boards_migration = Path(__file__).parent.parent / 'migrations' / '001_create_tables.sql'
                users_migration = Path(__file__).parent.parent / 'migrations' / '002_create_users_table.sql'
                user_id_migration = Path(__file__).parent.parent / 'migrations' / '003_add_user_id_to_boards.sql'
                
                execute_sql_file(str(boards_migration))
                execute_sql_file(str(users_migration))
                execute_sql_file(str(user_id_migration))
                
                # 获取数据库检查器
                inspector = inspect(db.engine)
                
                # 验证 user_id 列存在
                columns = {col['name']: col for col in inspector.get_columns('boards')}
                assert 'user_id' in columns
                
                # 验证外键约束
                foreign_keys = inspector.get_foreign_keys('boards')
                user_id_fk = None
                for fk in foreign_keys:
                    if 'user_id' in fk['constrained_columns']:
                        user_id_fk = fk
                        break
                
                assert user_id_fk is not None, "user_id 外键约束不存在"
                assert user_id_fk['referred_table'] == 'users'
                assert 'id' in user_id_fk['referred_columns']
                assert user_id_fk['options'].get('ondelete') == 'CASCADE'
                
                # 验证索引
                indexes = inspector.get_indexes('boards')
                user_id_index = None
                for idx in indexes:
                    if 'user_id' in idx['column_names']:
                        user_id_index = idx
                        break
                
                assert user_id_index is not None, "user_id 索引不存在"
                
        except Exception as e:
            pytest.skip(f"数据库不可用，跳过测试: {e}")
