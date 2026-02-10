"""
数据库配置模块

本模块提供 SQLAlchemy 数据库配置，包括：
- 数据库连接字符串配置
- SQLAlchemy 实例初始化
- 数据库连接池配置
- 字符集配置

需求：7.1, 7.2, 7.3
"""

import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()


class Config:
    """应用配置类"""
    
    # 数据库配置
    # 从环境变量读取数据库连接字符串，如果未设置则使用默认值
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost:3306/taskboard'
    )
    
    # 禁用 SQLAlchemy 事件系统的修改跟踪，节省内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 数据库连接池配置
    # 连接池大小：保持的数据库连接数
    SQLALCHEMY_POOL_SIZE = 10
    
    # 连接池回收时间（秒）：超过此时间的连接将被回收
    # MySQL 默认 wait_timeout 为 28800 秒（8小时），设置为 7200 秒（2小时）以避免连接超时
    SQLALCHEMY_POOL_RECYCLE = 7200
    
    # 连接池超时时间（秒）：获取连接的最大等待时间
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # 最大溢出连接数：超过 pool_size 后可以创建的额外连接数
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # 连接前执行的 SQL 命令，确保使用 UTF-8 字符集
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # 连接前测试连接是否有效
        'connect_args': {
            'charset': 'utf8mb4',  # 使用 utf8mb4 字符集支持完整的 Unicode（包括 emoji）
        }
    }
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    # 使用内存数据库进行测试
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # 测试时禁用 CSRF 保护
    WTF_CSRF_ENABLED = False
    # SQLite 不需要连接池配置和字符集配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    # 生产环境必须设置 SECRET_KEY 环境变量
    SECRET_KEY = os.getenv('SECRET_KEY')


# 配置字典，根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    获取配置对象
    
    Args:
        env: 环境名称 ('development', 'testing', 'production')
             如果为 None，则从 FLASK_ENV 环境变量读取
    
    Returns:
        Config: 配置类对象
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
