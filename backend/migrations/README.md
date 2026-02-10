# 数据库迁移脚本

本目录包含数据库迁移脚本，用于创建和管理数据库表结构。

## 目录结构

```
migrations/
├── __init__.py                          # 迁移模块，提供 Python API
├── 001_create_tables.sql                # 创建基础表结构
├── 001_create_tables_rollback.sql       # 回滚脚本
├── 002_create_users_table.sql           # 创建用户认证表
├── 002_create_users_table_rollback.sql  # 用户表回滚脚本
├── 003_add_user_id_to_boards.sql        # 为 boards 表添加 user_id 外键
├── 003_add_user_id_to_boards_rollback.sql # boards 外键回滚脚本
└── README.md                            # 本文档
```

## 迁移脚本说明

### 001_create_tables.sql

创建系统的三个核心表：

1. **boards 表**：存储看板信息
   - 字段：id, name, created_at, updated_at
   - 索引：idx_created_at

2. **lists 表**：存储工作列表信息
   - 字段：id, board_id, name, position, created_at, updated_at
   - 外键：board_id → boards(id) ON DELETE CASCADE
   - 索引：idx_board_id, idx_position, idx_board_position

3. **cards 表**：存储任务卡片信息
   - 字段：id, list_id, title, description, due_date, tags, position, created_at, updated_at
   - 外键：list_id → lists(id) ON DELETE CASCADE
   - 索引：idx_list_id, idx_position, idx_due_date, idx_list_position

### 002_create_users_table.sql

创建用户认证表：

1. **users 表**：存储用户认证信息
   - 字段：id, username, email, password_hash, created_at
   - 唯一约束：username, email
   - 检查约束：username 长度 >= 3，email 格式验证
   - 索引：idx_users_username, idx_users_email
   - 需求：9.1, 9.3

### 003_add_user_id_to_boards.sql

为 boards 表添加用户关联：

1. **boards 表更新**：添加用户外键
   - 新增字段：user_id (INT)
   - 外键约束：user_id → users(id) ON DELETE CASCADE
   - 索引：idx_boards_user_id
   - 需求：9.2, 9.4

### 外键约束和级联删除

- 删除看板时，自动删除该看板下的所有列表和卡片
- 删除列表时，自动删除该列表下的所有卡片
- 使用 `ON DELETE CASCADE` 确保数据一致性

### 索引设计

- **单列索引**：用于单字段查询（如按 board_id 查询列表）
- **复合索引**：用于多字段查询和排序（如按 board_id 和 position 查询并排序列表）

## 使用方法

### 方法 1：使用命令行工具（推荐）

```bash
# 初始化数据库（使用 SQLAlchemy）
python migrate.py init

# 初始化数据库（使用 SQL 脚本）
python migrate.py init-sql

# 重置数据库（开发环境）
python migrate.py reset

# 重置数据库（使用 SQL 脚本）
python migrate.py reset-sql

# 删除所有表（危险操作！）
python migrate.py drop

# 指定环境
python migrate.py init --env development
python migrate.py init --env testing
```

### 方法 2：使用 Python API

```python
from flask import Flask
from config import get_config, db
from migrations import init_database, init_database_from_sql, reset_database, create_users_table

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(get_config('development'))
db.init_app(app)

with app.app_context():
    # 使用 SQLAlchemy 初始化数据库
    init_database()
    
    # 或者使用 SQL 脚本初始化数据库
    init_database_from_sql()
    
    # 创建用户认证表
    create_users_table()
    
    # 为 boards 表添加 user_id 外键
    add_user_id_to_boards()
    
    # 重置数据库（仅开发环境）
    reset_database()
```

### 方法 3：直接执行 SQL 脚本

```bash
# 使用 MySQL 客户端执行
mysql -u root -p taskboard < migrations/001_create_tables.sql
mysql -u root -p taskboard < migrations/002_create_users_table.sql

# 回滚
mysql -u root -p taskboard < migrations/002_create_users_table_rollback.sql
mysql -u root -p taskboard < migrations/001_create_tables_rollback.sql
```

## 开发环境快速设置

```bash
# 1. 确保 MySQL 服务正在运行
# 2. 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS taskboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. 配置环境变量（可选）
# 编辑 .env 文件或设置环境变量
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/taskboard"

# 4. 初始化数据库
python migrate.py init
```

## Docker 环境设置

在 Docker 环境中，数据库初始化脚本会自动执行：

```yaml
# docker-compose.yml 中的配置
mysql:
  image: mysql:8.0
  volumes:
    - ./backend/migrations/001_create_tables.sql:/docker-entrypoint-initdb.d/001_create_tables.sql
```

MySQL 容器启动时会自动执行 `/docker-entrypoint-initdb.d/` 目录下的 SQL 脚本。

## 测试环境

测试环境使用 SQLite 内存数据库，不需要执行迁移脚本。测试框架会自动创建和清理数据库：

```python
# tests/conftest.py
@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()  # 自动创建表
        yield app
        db.drop_all()    # 自动清理
```

## 注意事项

1. **生产环境**：
   - 不要使用 `reset` 或 `drop` 命令
   - 建议使用 SQL 脚本进行迁移，以便更好地控制和审计
   - 在执行迁移前备份数据库

2. **字符集**：
   - 所有表使用 `utf8mb4` 字符集和 `utf8mb4_unicode_ci` 排序规则
   - 支持完整的 Unicode 字符，包括 emoji

3. **时间戳**：
   - `created_at` 和 `updated_at` 使用 MySQL 的 `TIMESTAMP` 类型
   - `created_at` 默认为当前时间
   - `updated_at` 在记录更新时自动更新

4. **JSON 字段**：
   - `cards.tags` 使用 MySQL 的 `JSON` 类型
   - 需要 MySQL 5.7.8 或更高版本

## 故障排除

### 错误：表已存在

如果遇到 "Table already exists" 错误，说明表已经创建。可以：

```bash
# 删除现有表并重新创建
python migrate.py reset
```

### 错误：外键约束失败

如果遇到外键约束错误，确保：
1. 父表（boards, lists）在子表之前创建
2. 外键字段的类型与引用字段完全匹配
3. 使用 InnoDB 存储引擎

### 错误：字符集不匹配

确保数据库和表都使用 utf8mb4 字符集：

```sql
-- 修改数据库字符集
ALTER DATABASE taskboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 修改表字符集
ALTER TABLE boards CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 相关文档

- [需求文档](../../.kiro/specs/visual-task-board/requirements.md) - 需求 7.1, 7.2, 7.3, 7.4
- [设计文档](../../.kiro/specs/visual-task-board/design.md) - 数据库设计章节
- [配置文档](../CONFIG_README.md) - 数据库配置说明
