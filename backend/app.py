"""
Flask 应用入口

本模块初始化 Flask 应用，配置数据库连接，注册路由蓝图和错误处理器。

需求：6.1, 6.4, 6.5, 10.1, 10.2, 10.4
"""

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
import logging
from logging.handlers import RotatingFileHandler
import os

from config import get_config, db
from utils.exceptions import (
    ValidationError,
    NotFoundError,
    DatabaseError,
    AuthenticationError,
    TokenExpiredError,
    InvalidTokenError,
    UnauthorizedError,
    ForbiddenError
)
from routes.boards import boards_bp
from routes.lists import lists_bp
from routes.cards import cards_bp
from routes.auth import auth_bp


def create_app(config_name=None):
    """
    创建并配置 Flask 应用
    
    Args:
        config_name: 配置名称 ('development', 'testing', 'production')
                    如果为 None，则从环境变量读取
    
    Returns:
        Flask: 配置好的 Flask 应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init_app(app)
    
    # 配置 CORS（跨域资源共享）
    # 需求：6.5 - THE Backend SHALL 处理跨域请求（CORS）
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # 生产环境应该限制为特定域名
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 配置日志记录
    # 需求：10.2 - WHEN 数据库操作失败时，THE Backend SHALL 记录错误日志并返回错误响应
    configure_logging(app)
    
    # 注册路由蓝图
    # 需求：6.1 - THE Backend SHALL 提供 RESTful API 接口供前端调用
    app.register_blueprint(boards_bp, url_prefix='/api/boards')
    app.register_blueprint(lists_bp, url_prefix='/api/lists')
    app.register_blueprint(cards_bp, url_prefix='/api/cards')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 注册错误处理器
    # 需求：6.4 - WHEN 后端处理失败时，THE Backend SHALL 返回明确的错误信息和状态码
    register_error_handlers(app)
    
    return app


def configure_logging(app):
    """
    配置应用日志记录
    
    Args:
        app: Flask 应用实例
    """
    if not app.debug and not app.testing:
        # 创建日志目录
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # 配置文件日志处理器
        file_handler = RotatingFileHandler(
            'logs/taskboard.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Taskboard application startup')


def register_error_handlers(app):
    """
    注册错误处理器
    
    Args:
        app: Flask 应用实例
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        处理验证错误
        
        需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
        
        Args:
            error: ValidationError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 400)
        """
        app.logger.warning(f'Validation error: {error.message}')
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': error.message,
                'details': error.details
            }
        }), 400
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        """
        处理认证错误
        
        需求：2.3, 2.4 - 用户名或密码错误
        
        Args:
            error: AuthenticationError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 401)
        """
        app.logger.warning(f'Authentication error: {error.message}')
        return jsonify({
            'error': {
                'code': 'AUTHENTICATION_ERROR',
                'message': error.message
            }
        }), 401
    
    @app.errorhandler(TokenExpiredError)
    def handle_token_expired_error(error):
        """
        处理令牌过期错误
        
        需求：3.2 - 令牌已过期
        
        Args:
            error: TokenExpiredError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 401)
        """
        app.logger.info(f'Token expired: {error.message}')
        return jsonify({
            'error': {
                'code': 'TOKEN_EXPIRED',
                'message': error.message
            }
        }), 401
    
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(error):
        """
        处理令牌无效错误
        
        需求：3.3 - 令牌无效
        
        Args:
            error: InvalidTokenError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 401)
        """
        app.logger.warning(f'Invalid token: {error.message}')
        return jsonify({
            'error': {
                'code': 'INVALID_TOKEN',
                'message': error.message
            }
        }), 401
    
    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized_error(error):
        """
        处理未授权错误
        
        需求：3.4 - 未授权
        
        Args:
            error: UnauthorizedError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 401)
        """
        app.logger.info(f'Unauthorized: {error.message}')
        return jsonify({
            'error': {
                'code': 'UNAUTHORIZED',
                'message': error.message
            }
        }), 401
    
    @app.errorhandler(ForbiddenError)
    def handle_forbidden_error(error):
        """
        处理无权访问错误
        
        需求：4.2, 4.4, 4.5 - 无权访问
        
        Args:
            error: ForbiddenError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 403)
        """
        app.logger.warning(f'Forbidden: {error.message}')
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': error.message
            }
        }), 403
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """
        处理资源不存在错误
        
        需求：10.1 - WHEN 网络请求失败时，THE System SHALL 显示网络错误提示
        
        Args:
            error: NotFoundError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 404)
        """
        app.logger.info(f'Resource not found: {error.message}')
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': error.message,
                'details': error.details
            }
        }), 404
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """
        处理 SQLAlchemy 数据库错误
        
        需求：10.2 - WHEN 数据库操作失败时，THE Backend SHALL 记录错误日志并返回错误响应
        需求：10.4 - WHEN 服务器内部错误时，THE Backend SHALL 返回 500 状态码和错误描述
        需求：10.5 - THE System SHALL 确保错误不会导致数据不一致
        
        Args:
            error: SQLAlchemyError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 500)
        """
        # 记录完整的错误堆栈到日志
        app.logger.error(f'Database error: {str(error)}', exc_info=True)
        
        # 回滚数据库会话，确保数据一致性
        db.session.rollback()
        
        # 返回通用错误信息（不暴露内部细节）
        return jsonify({
            'error': {
                'code': 'DATABASE_ERROR',
                'message': '数据库操作失败，请稍后重试'
            }
        }), 500
    
    @app.errorhandler(DatabaseError)
    def handle_custom_database_error(error):
        """
        处理自定义数据库错误
        
        需求：10.2 - WHEN 数据库操作失败时，THE Backend SHALL 记录错误日志并返回错误响应
        需求：10.4 - WHEN 服务器内部错误时，THE Backend SHALL 返回 500 状态码和错误描述
        
        Args:
            error: DatabaseError 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 500)
        """
        # 记录错误信息和原始异常
        if error.original_error:
            app.logger.error(
                f'Database error: {error.message}, Original: {str(error.original_error)}',
                exc_info=True
            )
        else:
            app.logger.error(f'Database error: {error.message}', exc_info=True)
        
        # 回滚数据库会话
        db.session.rollback()
        
        return jsonify({
            'error': {
                'code': 'DATABASE_ERROR',
                'message': error.message
            }
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """
        处理未预期的异常
        
        需求：10.4 - WHEN 服务器内部错误时，THE Backend SHALL 返回 500 状态码和错误描述
        
        Args:
            error: Exception 异常实例
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 500)
        """
        # 记录完整的错误堆栈
        app.logger.error(f'Unexpected error: {str(error)}', exc_info=True)
        
        # 尝试回滚数据库会话
        try:
            db.session.rollback()
        except Exception:
            pass
        
        # 返回通用错误信息
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': '服务器内部错误，请稍后重试'
            }
        }), 500
    
    @app.errorhandler(404)
    def handle_404_error(error):
        """
        处理 404 路由不存在错误
        
        Args:
            error: 404 错误
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 404)
        """
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': '请求的路由不存在'
            }
        }), 404
    
    @app.errorhandler(405)
    def handle_405_error(error):
        """
        处理 405 方法不允许错误
        
        Args:
            error: 405 错误
        
        Returns:
            tuple: (JSON 响应, HTTP 状态码 405)
        """
        return jsonify({
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': '请求方法不允许'
            }
        }), 405


# 创建应用实例（用于开发服务器）
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
