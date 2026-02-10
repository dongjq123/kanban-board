# 数据库配置文档

## 概述

本文档说明如何配置和使用 SQLAlchemy 数据库连接。

## 配置文件

配置在 `config.py` 中定义，包含以下主要组件：

### 1. SQLAlchemy 实例

```python
from config import db
```

`db` 是全局的 SQLAlchemy 实例，用于定义模型和执行数据库操作。

### 2. 配置类

系统提供三种环境配置：

- **DevelopmentConfig**: 开发环境配置（默认）
- **TestingConfig**: 测试环境配置（使用 SQLite 内存数据库）
- **ProductionConfig**: 生产环境配置

### 3. 配置参数

#### 数据库连接

- `SQLALCHEMY_DATABASE_URI`: 数据库连接字符串
  - 默认: `mysql+pymysql://root:password@localhost:3306/taskboard`
  - 可通过环境变量 `DATABASE_URL` 覆盖

#### 连接池配置

- `SQLALCHEMY_POOL_SIZE`: 连接池大小（默认: 10）
- `SQLALCHEMY_POOL_RECYCLE`: 连接回收时间（默认: 7200 秒）
- `SQLALCHEMY_POOL_TIMEOUT`: 连接超时时间（默认: 30 秒）
- `SQLALCHEMY_MAX_OVERFLOW`: 最大溢出连接数（默认: 20）

#### 字符集配置

- 使用 `utf8mb4` 字符集，支持完整的 Unicode（包括 emoji）
- 启用 `pool_pre_ping` 确保连接有效性

## 环境变量

在项目根目录创建 `.env` 文件（参考 `.env.example`）：

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskboard
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

## 使用方法

### 1. 在 Flask 应用中初始化

```python
from flask import Flask
from config import db, get_config

app = Flask(__name__)
app.config.from_object(get_config('development'))
db.init_app(app)
```

### 2. 定义模型

```python
from config import db

class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
```

### 3. 创建数据库表

```python
with app.app_context():
    db.create_all()
```

### 4. 执行数据库操作

```python
# 创建记录
board = Board(name='新看板')
db.session.add(board)
db.session.commit()

# 查询记录
boards = Board.query.all()

# 更新记录
board.name = '更新后的名称'
db.session.commit()

# 删除记录
db.session.delete(board)
db.session.commit()
```

## 测试配置

运行配置测试：

```bash
pytest tests/test_config.py -v
```

## 连接池说明

### 为什么需要连接池？

1. **性能优化**: 避免频繁创建和销毁数据库连接
2. **资源管理**: 限制同时打开的连接数
3. **连接复用**: 重用已有连接，减少开销

### 连接池参数调优

- **POOL_SIZE**: 根据应用并发量调整，一般 5-20 之间
- **MAX_OVERFLOW**: 处理突发流量，建议设置为 POOL_SIZE 的 1-2 倍
- **POOL_RECYCLE**: 避免 MySQL 连接超时，设置为小于 MySQL `wait_timeout` 的值
- **POOL_TIMEOUT**: 获取连接的最大等待时间，避免长时间阻塞

### 连接池监控

在生产环境中，建议监控以下指标：

- 连接池使用率
- 连接等待时间
- 连接超时次数
- 连接错误率

## 字符集说明

### 为什么使用 utf8mb4？

- **完整 Unicode 支持**: 支持所有 Unicode 字符，包括 emoji
- **兼容性**: 向后兼容 utf8
- **推荐标准**: MySQL 5.5.3+ 推荐使用 utf8mb4

### 数据库字符集配置

确保 MySQL 数据库也使用 utf8mb4：

```sql
CREATE DATABASE taskboard 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

## 故障排查

### 连接失败

1. 检查数据库服务是否运行
2. 验证连接字符串是否正确
3. 确认数据库用户权限
4. 检查防火墙设置

### 连接超时

1. 增加 `POOL_TIMEOUT` 值
2. 检查数据库负载
3. 优化慢查询
4. 增加连接池大小

### 字符编码问题

1. 确认数据库使用 utf8mb4
2. 检查表和列的字符集
3. 验证连接字符串包含 charset 参数

## 安全建议

1. **不要在代码中硬编码密码**: 使用环境变量
2. **使用强密码**: 数据库密码应足够复杂
3. **限制数据库访问**: 仅允许必要的 IP 访问
4. **定期更新密钥**: 定期更换 SECRET_KEY
5. **生产环境配置**: 确保生产环境禁用 DEBUG 模式

## 相关需求

- 需求 7.1: 数据库包含 boards 表
- 需求 7.2: 数据库包含 lists 表
- 需求 7.3: 数据库包含 cards 表

## 下一步

配置完成后，继续实现：

- 任务 2.2: 实现 Board 模型
- 任务 2.3: 实现 List 模型
- 任务 2.4: 实现 Card 模型
