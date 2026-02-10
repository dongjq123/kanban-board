"""
测试错误处理中间件

本模块测试 Flask 应用的错误处理器，确保各种错误情况都能正确处理并返回适当的响应。

需求：6.4, 10.1, 10.2, 10.4
"""

import pytest
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from utils.exceptions import ValidationError, NotFoundError, DatabaseError
from app import create_app


class TestValidationErrorHandler:
    """测试 ValidationError 错误处理器"""
    
    def test_validation_error_returns_400(self, app, client):
        """测试 ValidationError 返回 400 状态码"""
        
        @app.route('/test/validation-error')
        def trigger_validation_error():
            raise ValidationError("看板名称不能为空")
        
        response = client.get('/test/validation-error')
        
        assert response.status_code == 400
        assert response.json['error']['code'] == 'VALIDATION_ERROR'
        assert response.json['error']['message'] == "看板名称不能为空"
    
    def test_validation_error_with_details(self, app, client):
        """测试 ValidationError 包含详细信息"""
        
        @app.route('/test/validation-error-details')
        def trigger_validation_error_with_details():
            raise ValidationError(
                "看板名称不能为空",
                details={'field': 'name', 'constraint': 'required'}
            )
        
        response = client.get('/test/validation-error-details')
        
        assert response.status_code == 400
        assert response.json['error']['code'] == 'VALIDATION_ERROR'
        assert response.json['error']['message'] == "看板名称不能为空"
        assert response.json['error']['details']['field'] == 'name'
        assert response.json['error']['details']['constraint'] == 'required'
    
    def test_validation_error_empty_string(self, app, client):
        """测试空字符串验证错误"""
        
        @app.route('/test/empty-string')
        def trigger_empty_string_error():
            raise ValidationError(
                "字段不能为空",
                details={'field': 'title', 'constraint': 'non_empty'}
            )
        
        response = client.get('/test/empty-string')
        
        assert response.status_code == 400
        assert response.json['error']['code'] == 'VALIDATION_ERROR'
        assert '不能为空' in response.json['error']['message']
    
    def test_validation_error_type_mismatch(self, app, client):
        """测试类型不匹配验证错误"""
        
        @app.route('/test/type-mismatch')
        def trigger_type_mismatch_error():
            raise ValidationError(
                "字段类型错误",
                details={
                    'field': 'position',
                    'expected_type': 'int',
                    'actual_type': 'str'
                }
            )
        
        response = client.get('/test/type-mismatch')
        
        assert response.status_code == 400
        assert response.json['error']['details']['expected_type'] == 'int'
        assert response.json['error']['details']['actual_type'] == 'str'


class TestNotFoundErrorHandler:
    """测试 NotFoundError 错误处理器"""
    
    def test_not_found_error_returns_404(self, app, client):
        """测试 NotFoundError 返回 404 状态码"""
        
        @app.route('/test/not-found-error')
        def trigger_not_found_error():
            raise NotFoundError("看板不存在")
        
        response = client.get('/test/not-found-error')
        
        assert response.status_code == 404
        assert response.json['error']['code'] == 'NOT_FOUND'
        assert response.json['error']['message'] == "看板不存在"
    
    def test_not_found_error_with_details(self, app, client):
        """测试 NotFoundError 包含详细信息"""
        
        @app.route('/test/not-found-error-details')
        def trigger_not_found_error_with_details():
            raise NotFoundError(
                "看板不存在",
                details={'resource': 'board', 'id': 123}
            )
        
        response = client.get('/test/not-found-error-details')
        
        assert response.status_code == 404
        assert response.json['error']['code'] == 'NOT_FOUND'
        assert response.json['error']['message'] == "看板不存在"
        assert response.json['error']['details']['resource'] == 'board'
        assert response.json['error']['details']['id'] == 123
    
    def test_not_found_error_for_list(self, app, client):
        """测试列表不存在错误"""
        
        @app.route('/test/list-not-found')
        def trigger_list_not_found():
            raise NotFoundError(
                "列表不存在",
                details={'resource': 'list', 'id': 456}
            )
        
        response = client.get('/test/list-not-found')
        
        assert response.status_code == 404
        assert response.json['error']['details']['resource'] == 'list'
    
    def test_not_found_error_for_card(self, app, client):
        """测试卡片不存在错误"""
        
        @app.route('/test/card-not-found')
        def trigger_card_not_found():
            raise NotFoundError(
                "卡片不存在",
                details={'resource': 'card', 'id': 789}
            )
        
        response = client.get('/test/card-not-found')
        
        assert response.status_code == 404
        assert response.json['error']['details']['resource'] == 'card'


class TestDatabaseErrorHandler:
    """测试数据库错误处理器"""
    
    def test_sqlalchemy_error_returns_500(self, app, client):
        """测试 SQLAlchemyError 返回 500 状态码"""
        
        @app.route('/test/sqlalchemy-error')
        def trigger_sqlalchemy_error():
            raise SQLAlchemyError("Database connection failed")
        
        response = client.get('/test/sqlalchemy-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'DATABASE_ERROR'
        assert '数据库操作失败' in response.json['error']['message']
    
    def test_sqlalchemy_error_does_not_expose_details(self, app, client):
        """测试 SQLAlchemyError 不暴露内部细节"""
        
        @app.route('/test/sqlalchemy-error-details')
        def trigger_sqlalchemy_error_with_details():
            raise SQLAlchemyError("Internal database error with sensitive info")
        
        response = client.get('/test/sqlalchemy-error-details')
        
        assert response.status_code == 500
        # 确保不暴露敏感的内部错误信息
        assert 'sensitive info' not in response.json['error']['message']
        assert 'Internal database error' not in response.json['error']['message']
    
    def test_integrity_error_returns_500(self, app, client):
        """测试 IntegrityError（外键约束错误）返回 500"""
        
        @app.route('/test/integrity-error')
        def trigger_integrity_error():
            raise IntegrityError("Foreign key constraint failed", None, None)
        
        response = client.get('/test/integrity-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'DATABASE_ERROR'
    
    def test_operational_error_returns_500(self, app, client):
        """测试 OperationalError（数据库操作错误）返回 500"""
        
        @app.route('/test/operational-error')
        def trigger_operational_error():
            raise OperationalError("Connection timeout", None, None)
        
        response = client.get('/test/operational-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'DATABASE_ERROR'
    
    def test_custom_database_error_returns_500(self, app, client):
        """测试自定义 DatabaseError 返回 500 状态码"""
        
        @app.route('/test/custom-database-error')
        def trigger_custom_database_error():
            raise DatabaseError("数据库连接失败")
        
        response = client.get('/test/custom-database-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'DATABASE_ERROR'
        assert response.json['error']['message'] == "数据库连接失败"
    
    def test_custom_database_error_with_original_error(self, app, client):
        """测试带原始错误的 DatabaseError"""
        
        @app.route('/test/database-error-with-original')
        def trigger_database_error_with_original():
            original = ValueError("Invalid connection string")
            raise DatabaseError("数据库配置错误", original_error=original)
        
        response = client.get('/test/database-error-with-original')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'DATABASE_ERROR'
        assert response.json['error']['message'] == "数据库配置错误"


class TestGeneralErrorHandler:
    """测试通用异常处理器"""
    
    def test_unexpected_exception_returns_500(self, app, client):
        """测试未预期的异常返回 500 状态码"""
        
        @app.route('/test/unexpected-error')
        def trigger_unexpected_error():
            raise Exception("Unexpected error occurred")
        
        response = client.get('/test/unexpected-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'INTERNAL_ERROR'
        assert '服务器内部错误' in response.json['error']['message']
    
    def test_unexpected_error_does_not_expose_details(self, app, client):
        """测试未预期的异常不暴露内部细节"""
        
        @app.route('/test/unexpected-error-details')
        def trigger_unexpected_error_with_details():
            raise Exception("Sensitive internal error information")
        
        response = client.get('/test/unexpected-error-details')
        
        assert response.status_code == 500
        # 确保不暴露敏感信息
        assert 'Sensitive' not in response.json['error']['message']
        assert 'internal error information' not in response.json['error']['message']
    
    def test_value_error_returns_500(self, app, client):
        """测试 ValueError 返回 500"""
        
        @app.route('/test/value-error')
        def trigger_value_error():
            raise ValueError("Invalid value")
        
        response = client.get('/test/value-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'INTERNAL_ERROR'
    
    def test_type_error_returns_500(self, app, client):
        """测试 TypeError 返回 500"""
        
        @app.route('/test/type-error')
        def trigger_type_error():
            raise TypeError("Type mismatch")
        
        response = client.get('/test/type-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'INTERNAL_ERROR'
    
    def test_key_error_returns_500(self, app, client):
        """测试 KeyError 返回 500"""
        
        @app.route('/test/key-error')
        def trigger_key_error():
            raise KeyError("Missing key")
        
        response = client.get('/test/key-error')
        
        assert response.status_code == 500
        assert response.json['error']['code'] == 'INTERNAL_ERROR'


class TestHTTPErrorHandlers:
    """测试 HTTP 错误处理器"""
    
    def test_404_route_not_found(self, client):
        """测试访问不存在的路由返回 404"""
        response = client.get('/api/nonexistent-route')
        
        assert response.status_code == 404
        assert response.json['error']['code'] == 'NOT_FOUND'
        assert '路由不存在' in response.json['error']['message']
    
    def test_405_method_not_allowed(self, app, client):
        """测试使用不允许的 HTTP 方法返回 405"""
        
        @app.route('/test/get-only', methods=['GET'])
        def get_only_route():
            return {'message': 'success'}
        
        # 尝试使用 POST 方法访问只允许 GET 的路由
        response = client.post('/test/get-only')
        
        assert response.status_code == 405
        assert response.json['error']['code'] == 'METHOD_NOT_ALLOWED'
        assert '方法不允许' in response.json['error']['message']


class TestErrorResponseFormat:
    """测试错误响应格式"""
    
    def test_error_response_has_correct_structure(self, app, client):
        """测试错误响应具有正确的结构"""
        
        @app.route('/test/error-structure')
        def trigger_error():
            raise ValidationError("测试错误", details={'field': 'test'})
        
        response = client.get('/test/error-structure')
        
        # 验证响应结构
        assert 'error' in response.json
        assert 'code' in response.json['error']
        assert 'message' in response.json['error']
        assert 'details' in response.json['error']
    
    def test_error_response_is_json(self, app, client):
        """测试错误响应是 JSON 格式"""
        
        @app.route('/test/json-format')
        def trigger_error():
            raise NotFoundError("测试错误")
        
        response = client.get('/test/json-format')
        
        assert response.content_type == 'application/json'
    
    def test_different_errors_have_different_codes(self, app, client):
        """测试不同的错误有不同的错误码"""
        
        @app.route('/test/validation')
        def trigger_validation():
            raise ValidationError("验证错误")
        
        @app.route('/test/notfound')
        def trigger_notfound():
            raise NotFoundError("未找到")
        
        @app.route('/test/database')
        def trigger_database():
            raise DatabaseError("数据库错误")
        
        validation_response = client.get('/test/validation')
        notfound_response = client.get('/test/notfound')
        database_response = client.get('/test/database')
        
        assert validation_response.json['error']['code'] == 'VALIDATION_ERROR'
        assert notfound_response.json['error']['code'] == 'NOT_FOUND'
        assert database_response.json['error']['code'] == 'DATABASE_ERROR'


class TestErrorLogging:
    """测试错误日志记录"""
    
    def test_validation_error_is_logged(self, app, client, caplog):
        """测试 ValidationError 被记录到日志"""
        
        @app.route('/test/log-validation')
        def trigger_validation():
            raise ValidationError("验证错误")
        
        with caplog.at_level('WARNING'):
            client.get('/test/log-validation')
        
        # 验证日志中包含错误信息
        assert any('Validation error' in record.message for record in caplog.records)
    
    def test_not_found_error_is_logged(self, app, client, caplog):
        """测试 NotFoundError 被记录到日志"""
        
        @app.route('/test/log-notfound')
        def trigger_notfound():
            raise NotFoundError("资源不存在")
        
        with caplog.at_level('INFO'):
            client.get('/test/log-notfound')
        
        # 验证日志中包含错误信息
        assert any('Resource not found' in record.message for record in caplog.records)
    
    def test_database_error_is_logged(self, app, client, caplog):
        """测试数据库错误被记录到日志"""
        
        @app.route('/test/log-database')
        def trigger_database():
            raise SQLAlchemyError("数据库错误")
        
        with caplog.at_level('ERROR'):
            client.get('/test/log-database')
        
        # 验证日志中包含错误信息
        assert any('Database error' in record.message for record in caplog.records)
    
    def test_unexpected_error_is_logged(self, app, client, caplog):
        """测试未预期的错误被记录到日志"""
        
        @app.route('/test/log-unexpected')
        def trigger_unexpected():
            raise Exception("未预期的错误")
        
        with caplog.at_level('ERROR'):
            client.get('/test/log-unexpected')
        
        # 验证日志中包含错误信息
        assert any('Unexpected error' in record.message for record in caplog.records)


class TestAuthenticationErrorHandlers:
    """测试认证相关错误处理器"""
    
    def test_authentication_error_returns_401(self, app, client):
        """测试 AuthenticationError 返回 401 状态码"""
        from utils.exceptions import AuthenticationError
        
        @app.route('/test/auth-error')
        def trigger_auth_error():
            raise AuthenticationError("用户名或密码错误")
        
        response = client.get('/test/auth-error')
        
        assert response.status_code == 401
        assert response.json['error']['code'] == 'AUTHENTICATION_ERROR'
        assert response.json['error']['message'] == "用户名或密码错误"
    
    def test_token_expired_error_returns_401(self, app, client):
        """测试 TokenExpiredError 返回 401 状态码"""
        from utils.exceptions import TokenExpiredError
        
        @app.route('/test/token-expired')
        def trigger_token_expired():
            raise TokenExpiredError()
        
        response = client.get('/test/token-expired')
        
        assert response.status_code == 401
        assert response.json['error']['code'] == 'TOKEN_EXPIRED'
        assert '令牌已过期' in response.json['error']['message']
    
    def test_invalid_token_error_returns_401(self, app, client):
        """测试 InvalidTokenError 返回 401 状态码"""
        from utils.exceptions import InvalidTokenError
        
        @app.route('/test/invalid-token')
        def trigger_invalid_token():
            raise InvalidTokenError()
        
        response = client.get('/test/invalid-token')
        
        assert response.status_code == 401
        assert response.json['error']['code'] == 'INVALID_TOKEN'
        assert '令牌无效' in response.json['error']['message']
    
    def test_unauthorized_error_returns_401(self, app, client):
        """测试 UnauthorizedError 返回 401 状态码"""
        from utils.exceptions import UnauthorizedError
        
        @app.route('/test/unauthorized')
        def trigger_unauthorized():
            raise UnauthorizedError()
        
        response = client.get('/test/unauthorized')
        
        assert response.status_code == 401
        assert response.json['error']['code'] == 'UNAUTHORIZED'
        assert '未授权' in response.json['error']['message']
    
    def test_forbidden_error_returns_403(self, app, client):
        """测试 ForbiddenError 返回 403 状态码"""
        from utils.exceptions import ForbiddenError
        
        @app.route('/test/forbidden')
        def trigger_forbidden():
            raise ForbiddenError()
        
        response = client.get('/test/forbidden')
        
        assert response.status_code == 403
        assert response.json['error']['code'] == 'FORBIDDEN'
        assert '无权访问' in response.json['error']['message']
    
    def test_authentication_error_with_custom_message(self, app, client):
        """测试带自定义消息的 AuthenticationError"""
        from utils.exceptions import AuthenticationError
        
        @app.route('/test/custom-auth-error')
        def trigger_custom_auth_error():
            raise AuthenticationError("账户已被锁定")
        
        response = client.get('/test/custom-auth-error')
        
        assert response.status_code == 401
        assert response.json['error']['message'] == "账户已被锁定"
    
    def test_forbidden_error_with_custom_message(self, app, client):
        """测试带自定义消息的 ForbiddenError"""
        from utils.exceptions import ForbiddenError
        
        @app.route('/test/custom-forbidden')
        def trigger_custom_forbidden():
            raise ForbiddenError("无权删除该资源")
        
        response = client.get('/test/custom-forbidden')
        
        assert response.status_code == 403
        assert response.json['error']['message'] == "无权删除该资源"


class TestErrorHandlerIntegration:
    """测试错误处理器集成"""
    
    def test_multiple_errors_in_sequence(self, app, client):
        """测试连续处理多个不同类型的错误"""
        
        @app.route('/test/error1')
        def error1():
            raise ValidationError("错误1")
        
        @app.route('/test/error2')
        def error2():
            raise NotFoundError("错误2")
        
        @app.route('/test/error3')
        def error3():
            raise DatabaseError("错误3")
        
        response1 = client.get('/test/error1')
        response2 = client.get('/test/error2')
        response3 = client.get('/test/error3')
        
        assert response1.status_code == 400
        assert response2.status_code == 404
        assert response3.status_code == 500
    
    def test_error_handler_does_not_affect_successful_requests(self, app, client):
        """测试错误处理器不影响成功的请求"""
        
        @app.route('/test/success')
        def success():
            return {'message': 'success'}
        
        @app.route('/test/error')
        def error():
            raise ValidationError("错误")
        
        # 先触发错误
        error_response = client.get('/test/error')
        assert error_response.status_code == 400
        
        # 然后发送成功请求
        success_response = client.get('/test/success')
        assert success_response.status_code == 200
        assert success_response.json['message'] == 'success'
    
    def test_authentication_errors_in_sequence(self, app, client):
        """测试连续处理多个认证相关错误"""
        from utils.exceptions import (
            AuthenticationError,
            TokenExpiredError,
            UnauthorizedError,
            ForbiddenError
        )
        
        @app.route('/test/auth1')
        def auth1():
            raise AuthenticationError()
        
        @app.route('/test/auth2')
        def auth2():
            raise TokenExpiredError()
        
        @app.route('/test/auth3')
        def auth3():
            raise UnauthorizedError()
        
        @app.route('/test/auth4')
        def auth4():
            raise ForbiddenError()
        
        response1 = client.get('/test/auth1')
        response2 = client.get('/test/auth2')
        response3 = client.get('/test/auth3')
        response4 = client.get('/test/auth4')
        
        assert response1.status_code == 401
        assert response2.status_code == 401
        assert response3.status_code == 401
        assert response4.status_code == 403
