"""
测试自定义异常类

本模块测试自定义异常类的创建和属性。

需求：10.1, 10.2, 10.3, 10.4
需求：2.3, 2.4, 3.2, 3.3, 3.4, 4.2, 4.4, 4.5 (认证相关异常)
"""

import pytest
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


class TestValidationError:
    """测试 ValidationError 异常类"""
    
    def test_validation_error_with_message_only(self):
        """测试只提供消息创建 ValidationError"""
        error = ValidationError("看板名称不能为空")
        
        assert str(error) == "看板名称不能为空"
        assert error.message == "看板名称不能为空"
        assert error.details == {}
    
    def test_validation_error_with_details(self):
        """测试提供消息和详细信息创建 ValidationError"""
        details = {
            'field': 'name',
            'constraint': 'required'
        }
        error = ValidationError("看板名称不能为空", details=details)
        
        assert str(error) == "看板名称不能为空"
        assert error.message == "看板名称不能为空"
        assert error.details == details
        assert error.details['field'] == 'name'
        assert error.details['constraint'] == 'required'
    
    def test_validation_error_is_exception(self):
        """测试 ValidationError 是 Exception 的子类"""
        error = ValidationError("测试错误")
        assert isinstance(error, Exception)
    
    def test_validation_error_can_be_raised(self):
        """测试 ValidationError 可以被抛出和捕获"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("测试错误", details={'field': 'test'})
        
        assert exc_info.value.message == "测试错误"
        assert exc_info.value.details == {'field': 'test'}
    
    def test_validation_error_with_empty_string(self):
        """测试空字符串验证错误"""
        error = ValidationError(
            "字段不能为空",
            details={'field': 'title', 'constraint': 'non_empty'}
        )
        
        assert error.message == "字段不能为空"
        assert error.details['constraint'] == 'non_empty'
    
    def test_validation_error_with_type_mismatch(self):
        """测试类型不匹配验证错误"""
        error = ValidationError(
            "字段类型错误",
            details={
                'field': 'position',
                'expected_type': 'int',
                'actual_type': 'str'
            }
        )
        
        assert error.message == "字段类型错误"
        assert error.details['expected_type'] == 'int'
        assert error.details['actual_type'] == 'str'


class TestNotFoundError:
    """测试 NotFoundError 异常类"""
    
    def test_not_found_error_with_message_only(self):
        """测试只提供消息创建 NotFoundError"""
        error = NotFoundError("看板不存在")
        
        assert str(error) == "看板不存在"
        assert error.message == "看板不存在"
        assert error.details == {}
    
    def test_not_found_error_with_details(self):
        """测试提供消息和详细信息创建 NotFoundError"""
        details = {
            'resource': 'board',
            'id': 123
        }
        error = NotFoundError("看板不存在", details=details)
        
        assert str(error) == "看板不存在"
        assert error.message == "看板不存在"
        assert error.details == details
        assert error.details['resource'] == 'board'
        assert error.details['id'] == 123
    
    def test_not_found_error_is_exception(self):
        """测试 NotFoundError 是 Exception 的子类"""
        error = NotFoundError("测试错误")
        assert isinstance(error, Exception)
    
    def test_not_found_error_can_be_raised(self):
        """测试 NotFoundError 可以被抛出和捕获"""
        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError("资源不存在", details={'resource': 'list', 'id': 456})
        
        assert exc_info.value.message == "资源不存在"
        assert exc_info.value.details == {'resource': 'list', 'id': 456}
    
    def test_not_found_error_for_board(self):
        """测试看板不存在错误"""
        error = NotFoundError(
            "看板不存在",
            details={'resource': 'board', 'id': 1}
        )
        
        assert error.message == "看板不存在"
        assert error.details['resource'] == 'board'
    
    def test_not_found_error_for_list(self):
        """测试列表不存在错误"""
        error = NotFoundError(
            "列表不存在",
            details={'resource': 'list', 'id': 2}
        )
        
        assert error.message == "列表不存在"
        assert error.details['resource'] == 'list'
    
    def test_not_found_error_for_card(self):
        """测试卡片不存在错误"""
        error = NotFoundError(
            "卡片不存在",
            details={'resource': 'card', 'id': 3}
        )
        
        assert error.message == "卡片不存在"
        assert error.details['resource'] == 'card'


class TestDatabaseError:
    """测试 DatabaseError 异常类"""
    
    def test_database_error_with_message_only(self):
        """测试只提供消息创建 DatabaseError"""
        error = DatabaseError("数据库连接失败")
        
        assert str(error) == "数据库连接失败"
        assert error.message == "数据库连接失败"
        assert error.original_error is None
    
    def test_database_error_with_original_error(self):
        """测试提供消息和原始错误创建 DatabaseError"""
        original = Exception("Connection timeout")
        error = DatabaseError("数据库操作失败", original_error=original)
        
        assert str(error) == "数据库操作失败"
        assert error.message == "数据库操作失败"
        assert error.original_error is original
        assert str(error.original_error) == "Connection timeout"
    
    def test_database_error_is_exception(self):
        """测试 DatabaseError 是 Exception 的子类"""
        error = DatabaseError("测试错误")
        assert isinstance(error, Exception)
    
    def test_database_error_can_be_raised(self):
        """测试 DatabaseError 可以被抛出和捕获"""
        original = ValueError("Invalid value")
        with pytest.raises(DatabaseError) as exc_info:
            raise DatabaseError("数据库错误", original_error=original)
        
        assert exc_info.value.message == "数据库错误"
        assert exc_info.value.original_error is original
    
    def test_database_error_for_connection_failure(self):
        """测试数据库连接失败错误"""
        error = DatabaseError("无法连接到数据库")
        
        assert error.message == "无法连接到数据库"
        assert error.original_error is None
    
    def test_database_error_for_transaction_failure(self):
        """测试数据库事务失败错误"""
        original = Exception("Transaction rollback")
        error = DatabaseError("事务执行失败", original_error=original)
        
        assert error.message == "事务执行失败"
        assert error.original_error is not None
    
    def test_database_error_preserves_original_exception_type(self):
        """测试 DatabaseError 保留原始异常类型"""
        original = ValueError("Invalid input")
        error = DatabaseError("数据库错误", original_error=original)
        
        assert isinstance(error.original_error, ValueError)
        assert str(error.original_error) == "Invalid input"


class TestExceptionInteraction:
    """测试异常类之间的交互"""
    
    def test_different_exception_types_are_distinct(self):
        """测试不同的异常类型是独立的"""
        validation_error = ValidationError("验证错误")
        not_found_error = NotFoundError("未找到")
        database_error = DatabaseError("数据库错误")
        
        assert type(validation_error) != type(not_found_error)
        assert type(validation_error) != type(database_error)
        assert type(not_found_error) != type(database_error)
    
    def test_can_catch_specific_exception_types(self):
        """测试可以捕获特定的异常类型"""
        # 测试捕获 ValidationError
        with pytest.raises(ValidationError):
            raise ValidationError("验证错误")
        
        # 测试捕获 NotFoundError
        with pytest.raises(NotFoundError):
            raise NotFoundError("未找到")
        
        # 测试捕获 DatabaseError
        with pytest.raises(DatabaseError):
            raise DatabaseError("数据库错误")
    
    def test_all_exceptions_are_base_exceptions(self):
        """测试所有自定义异常都是 Exception 的子类"""
        validation_error = ValidationError("验证错误")
        not_found_error = NotFoundError("未找到")
        database_error = DatabaseError("数据库错误")
        
        assert isinstance(validation_error, Exception)
        assert isinstance(not_found_error, Exception)
        assert isinstance(database_error, Exception)
    
    def test_exception_with_complex_details(self):
        """测试异常可以包含复杂的详细信息"""
        details = {
            'field': 'tags',
            'constraint': 'type',
            'expected': 'list',
            'actual': 'string',
            'value': 'invalid',
            'nested': {
                'info': 'additional context'
            }
        }
        error = ValidationError("标签格式错误", details=details)
        
        assert error.details['field'] == 'tags'
        assert error.details['nested']['info'] == 'additional context'



class TestAuthenticationError:
    """测试 AuthenticationError 异常类"""
    
    def test_authentication_error_with_default_message(self):
        """测试使用默认消息创建 AuthenticationError"""
        error = AuthenticationError()
        
        assert str(error) == "用户名或密码错误"
        assert error.message == "用户名或密码错误"
    
    def test_authentication_error_with_custom_message(self):
        """测试使用自定义消息创建 AuthenticationError"""
        error = AuthenticationError("登录失败")
        
        assert str(error) == "登录失败"
        assert error.message == "登录失败"
    
    def test_authentication_error_is_exception(self):
        """测试 AuthenticationError 是 Exception 的子类"""
        error = AuthenticationError()
        assert isinstance(error, Exception)
    
    def test_authentication_error_can_be_raised(self):
        """测试 AuthenticationError 可以被抛出和捕获"""
        with pytest.raises(AuthenticationError) as exc_info:
            raise AuthenticationError("认证失败")
        
        assert exc_info.value.message == "认证失败"
    
    def test_authentication_error_for_invalid_credentials(self):
        """测试无效凭证的认证错误"""
        error = AuthenticationError("用户名或密码错误")
        
        assert error.message == "用户名或密码错误"


class TestTokenExpiredError:
    """测试 TokenExpiredError 异常类"""
    
    def test_token_expired_error_with_default_message(self):
        """测试使用默认消息创建 TokenExpiredError"""
        error = TokenExpiredError()
        
        assert str(error) == "令牌已过期，请重新登录"
        assert error.message == "令牌已过期，请重新登录"
    
    def test_token_expired_error_with_custom_message(self):
        """测试使用自定义消息创建 TokenExpiredError"""
        error = TokenExpiredError("会话已过期")
        
        assert str(error) == "会话已过期"
        assert error.message == "会话已过期"
    
    def test_token_expired_error_is_exception(self):
        """测试 TokenExpiredError 是 Exception 的子类"""
        error = TokenExpiredError()
        assert isinstance(error, Exception)
    
    def test_token_expired_error_can_be_raised(self):
        """测试 TokenExpiredError 可以被抛出和捕获"""
        with pytest.raises(TokenExpiredError) as exc_info:
            raise TokenExpiredError()
        
        assert "令牌已过期" in exc_info.value.message


class TestInvalidTokenError:
    """测试 InvalidTokenError 异常类"""
    
    def test_invalid_token_error_with_default_message(self):
        """测试使用默认消息创建 InvalidTokenError"""
        error = InvalidTokenError()
        
        assert str(error) == "令牌无效"
        assert error.message == "令牌无效"
    
    def test_invalid_token_error_with_custom_message(self):
        """测试使用自定义消息创建 InvalidTokenError"""
        error = InvalidTokenError("令牌格式错误")
        
        assert str(error) == "令牌格式错误"
        assert error.message == "令牌格式错误"
    
    def test_invalid_token_error_is_exception(self):
        """测试 InvalidTokenError 是 Exception 的子类"""
        error = InvalidTokenError()
        assert isinstance(error, Exception)
    
    def test_invalid_token_error_can_be_raised(self):
        """测试 InvalidTokenError 可以被抛出和捕获"""
        with pytest.raises(InvalidTokenError) as exc_info:
            raise InvalidTokenError("签名验证失败")
        
        assert exc_info.value.message == "签名验证失败"


class TestUnauthorizedError:
    """测试 UnauthorizedError 异常类"""
    
    def test_unauthorized_error_with_default_message(self):
        """测试使用默认消息创建 UnauthorizedError"""
        error = UnauthorizedError()
        
        assert str(error) == "未授权，请先登录"
        assert error.message == "未授权，请先登录"
    
    def test_unauthorized_error_with_custom_message(self):
        """测试使用自定义消息创建 UnauthorizedError"""
        error = UnauthorizedError("需要登录")
        
        assert str(error) == "需要登录"
        assert error.message == "需要登录"
    
    def test_unauthorized_error_is_exception(self):
        """测试 UnauthorizedError 是 Exception 的子类"""
        error = UnauthorizedError()
        assert isinstance(error, Exception)
    
    def test_unauthorized_error_can_be_raised(self):
        """测试 UnauthorizedError 可以被抛出和捕获"""
        with pytest.raises(UnauthorizedError) as exc_info:
            raise UnauthorizedError()
        
        assert "未授权" in exc_info.value.message


class TestForbiddenError:
    """测试 ForbiddenError 异常类"""
    
    def test_forbidden_error_with_default_message(self):
        """测试使用默认消息创建 ForbiddenError"""
        error = ForbiddenError()
        
        assert str(error) == "无权访问该资源"
        assert error.message == "无权访问该资源"
    
    def test_forbidden_error_with_custom_message(self):
        """测试使用自定义消息创建 ForbiddenError"""
        error = ForbiddenError("无权修改该资源")
        
        assert str(error) == "无权修改该资源"
        assert error.message == "无权修改该资源"
    
    def test_forbidden_error_is_exception(self):
        """测试 ForbiddenError 是 Exception 的子类"""
        error = ForbiddenError()
        assert isinstance(error, Exception)
    
    def test_forbidden_error_can_be_raised(self):
        """测试 ForbiddenError 可以被抛出和捕获"""
        with pytest.raises(ForbiddenError) as exc_info:
            raise ForbiddenError("无权删除该资源")
        
        assert exc_info.value.message == "无权删除该资源"


class TestAuthenticationExceptionInteraction:
    """测试认证相关异常类之间的交互"""
    
    def test_different_auth_exception_types_are_distinct(self):
        """测试不同的认证异常类型是独立的"""
        auth_error = AuthenticationError()
        token_expired = TokenExpiredError()
        invalid_token = InvalidTokenError()
        unauthorized = UnauthorizedError()
        forbidden = ForbiddenError()
        
        assert type(auth_error) != type(token_expired)
        assert type(auth_error) != type(invalid_token)
        assert type(auth_error) != type(unauthorized)
        assert type(auth_error) != type(forbidden)
        assert type(token_expired) != type(invalid_token)
        assert type(unauthorized) != type(forbidden)
    
    def test_can_catch_specific_auth_exception_types(self):
        """测试可以捕获特定的认证异常类型"""
        # 测试捕获 AuthenticationError
        with pytest.raises(AuthenticationError):
            raise AuthenticationError()
        
        # 测试捕获 TokenExpiredError
        with pytest.raises(TokenExpiredError):
            raise TokenExpiredError()
        
        # 测试捕获 InvalidTokenError
        with pytest.raises(InvalidTokenError):
            raise InvalidTokenError()
        
        # 测试捕获 UnauthorizedError
        with pytest.raises(UnauthorizedError):
            raise UnauthorizedError()
        
        # 测试捕获 ForbiddenError
        with pytest.raises(ForbiddenError):
            raise ForbiddenError()
    
    def test_all_auth_exceptions_are_base_exceptions(self):
        """测试所有认证异常都是 Exception 的子类"""
        auth_error = AuthenticationError()
        token_expired = TokenExpiredError()
        invalid_token = InvalidTokenError()
        unauthorized = UnauthorizedError()
        forbidden = ForbiddenError()
        
        assert isinstance(auth_error, Exception)
        assert isinstance(token_expired, Exception)
        assert isinstance(invalid_token, Exception)
        assert isinstance(unauthorized, Exception)
        assert isinstance(forbidden, Exception)
    
    def test_auth_exceptions_have_message_attribute(self):
        """测试所有认证异常都有 message 属性"""
        auth_error = AuthenticationError()
        token_expired = TokenExpiredError()
        invalid_token = InvalidTokenError()
        unauthorized = UnauthorizedError()
        forbidden = ForbiddenError()
        
        assert hasattr(auth_error, 'message')
        assert hasattr(token_expired, 'message')
        assert hasattr(invalid_token, 'message')
        assert hasattr(unauthorized, 'message')
        assert hasattr(forbidden, 'message')
    
    def test_auth_exceptions_with_custom_messages(self):
        """测试所有认证异常都支持自定义消息"""
        auth_error = AuthenticationError("自定义认证错误")
        token_expired = TokenExpiredError("自定义过期错误")
        invalid_token = InvalidTokenError("自定义无效错误")
        unauthorized = UnauthorizedError("自定义未授权错误")
        forbidden = ForbiddenError("自定义禁止错误")
        
        assert auth_error.message == "自定义认证错误"
        assert token_expired.message == "自定义过期错误"
        assert invalid_token.message == "自定义无效错误"
        assert unauthorized.message == "自定义未授权错误"
        assert forbidden.message == "自定义禁止错误"
