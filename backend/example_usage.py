"""
数据库配置使用示例

演示如何在 Flask 应用中使用数据库配置
"""

from flask import Flask
from config import db, get_config


def create_app(config_name='development'):
    """
    创建并配置 Flask 应用
    
    Args:
        config_name: 配置环境名称 ('development', 'testing', 'production')
    
    Returns:
        Flask: 配置好的 Flask 应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(get_config(config_name))
    
    # 初始化数据库
    db.init_app(app)
    
    return app


if __name__ == '__main__':
    # 创建开发环境应用
    app = create_app('development')
    
    with app.app_context():
        print("数据库配置信息：")
        print(f"数据库 URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"连接池大小: {app.config['SQLALCHEMY_POOL_SIZE']}")
        print(f"连接池回收时间: {app.config['SQLALCHEMY_POOL_RECYCLE']} 秒")
        print(f"连接池超时时间: {app.config['SQLALCHEMY_POOL_TIMEOUT']} 秒")
        print(f"最大溢出连接数: {app.config['SQLALCHEMY_MAX_OVERFLOW']}")
        print(f"字符集: {app.config['SQLALCHEMY_ENGINE_OPTIONS']['connect_args']['charset']}")
        print(f"调试模式: {app.config['DEBUG']}")
        
        # 注意：实际创建表需要先定义模型（将在任务 2.2-2.4 中实现）
        # db.create_all()
