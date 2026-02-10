"""
配置模块测试

测试数据库配置的正确性
"""

import os
import pytest
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, get_config, db


class TestConfigClasses:
    """测试配置类"""
    
    def test_config_has_database_uri(self):
        """测试配置类包含数据库 URI"""
        assert hasattr(Config, 'SQLALCHEMY_DATABASE_URI')
        assert Config.SQLALCHEMY_DATABASE_URI is not None
    
    def test_config_disables_track_modifications(self):
        """测试配置禁用了修改跟踪"""
        assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_config_has_pool_settings(self):
        """测试配置包含连接池设置"""
        assert hasattr(Config, 'SQLALCHEMY_POOL_SIZE')
        assert hasattr(Config, 'SQLALCHEMY_POOL_RECYCLE')
        assert hasattr(Config, 'SQLALCHEMY_POOL_TIMEOUT')
        assert hasattr(Config, 'SQLALCHEMY_MAX_OVERFLOW')
        
        # 验证连接池配置值合理
        assert Config.SQLALCHEMY_POOL_SIZE > 0
        assert Config.SQLALCHEMY_POOL_RECYCLE > 0
        assert Config.SQLALCHEMY_POOL_TIMEOUT > 0
        assert Config.SQLALCHEMY_MAX_OVERFLOW > 0
    
    def test_config_has_engine_options(self):
        """测试配置包含引擎选项"""
        assert hasattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS')
        assert 'pool_pre_ping' in Config.SQLALCHEMY_ENGINE_OPTIONS
        assert 'connect_args' in Config.SQLALCHEMY_ENGINE_OPTIONS
        assert 'charset' in Config.SQLALCHEMY_ENGINE_OPTIONS['connect_args']
        assert Config.SQLALCHEMY_ENGINE_OPTIONS['connect_args']['charset'] == 'utf8mb4'
    
    def test_development_config_debug_enabled(self):
        """测试开发配置启用了调试模式"""
        assert DevelopmentConfig.DEBUG is True
        assert DevelopmentConfig.TESTING is False
    
    def test_testing_config_uses_sqlite(self):
        """测试配置使用 SQLite 内存数据库"""
        assert TestingConfig.TESTING is True
        assert 'sqlite' in TestingConfig.SQLALCHEMY_DATABASE_URI
        assert ':memory:' in TestingConfig.SQLALCHEMY_DATABASE_URI
    
    def test_production_config_debug_disabled(self):
        """测试生产配置禁用了调试模式"""
        assert ProductionConfig.DEBUG is False
        assert ProductionConfig.TESTING is False


class TestGetConfig:
    """测试 get_config 函数"""
    
    def test_get_config_development(self):
        """测试获取开发环境配置"""
        config = get_config('development')
        assert config == DevelopmentConfig
    
    def test_get_config_testing(self):
        """测试获取测试环境配置"""
        config = get_config('testing')
        assert config == TestingConfig
    
    def test_get_config_production(self):
        """测试获取生产环境配置"""
        config = get_config('production')
        assert config == ProductionConfig
    
    def test_get_config_default(self):
        """测试获取默认配置"""
        config = get_config('invalid')
        assert config == DevelopmentConfig
    
    def test_get_config_from_env(self, monkeypatch):
        """测试从环境变量获取配置"""
        monkeypatch.setenv('FLASK_ENV', 'testing')
        config = get_config()
        assert config == TestingConfig


class TestDatabaseInstance:
    """测试数据库实例"""
    
    def test_db_instance_exists(self):
        """测试 db 实例存在"""
        assert db is not None
    
    def test_db_is_sqlalchemy_instance(self):
        """测试 db 是 SQLAlchemy 实例"""
        from flask_sqlalchemy import SQLAlchemy
        assert isinstance(db, SQLAlchemy)


class TestDatabaseURI:
    """测试数据库 URI 配置"""
    
    def test_database_uri_format(self):
        """测试数据库 URI 格式正确"""
        uri = Config.SQLALCHEMY_DATABASE_URI
        # MySQL URI 应该包含 mysql+pymysql://
        assert uri.startswith('mysql+pymysql://') or uri.startswith('sqlite://')
    
    def test_database_uri_from_env(self, monkeypatch):
        """测试从环境变量读取数据库 URI"""
        test_uri = 'mysql+pymysql://testuser:testpass@testhost:3306/testdb'
        monkeypatch.setenv('DATABASE_URL', test_uri)
        
        # 重新导入以获取新的环境变量
        import importlib
        import config as config_module
        importlib.reload(config_module)
        
        assert config_module.Config.SQLALCHEMY_DATABASE_URI == test_uri
