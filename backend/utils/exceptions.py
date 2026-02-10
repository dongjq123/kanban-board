"""
自定义异常类

本模块定义了应用程序中使用的自定义异常类，用于处理不同类型的错误情况。
这些异常类支持错误处理中间件提供统一的错误响应格式。

需求：10.1, 10.2, 10.3, 10.4
"""


class ValidationError(Exception):
    """
    验证错误异常
    
    当用户输入无效数据时抛出此异常。
    对应 HTTP 状态码 400 Bad Request。
    
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Attributes:
        message (str): 错误消息
        details (dict): 错误详细信息，包含字段名和约束信息
    """
    
    def __init__(self, message, details=None):
        """
        初始化验证错误异常
        
        Args:
            message (str): 错误消息
            details (dict, optional): 错误详细信息。默认为 None。
                示例: {'field': 'name', 'constraint': 'required'}
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(Exception):
    """
    资源不存在错误异常
    
    当请求的资源（看板、列表或卡片）不存在时抛出此异常。
    对应 HTTP 状态码 404 Not Found。
    
    需求：10.1 - WHEN 网络请求失败时，THE System SHALL 显示网络错误提示
    
    Attributes:
        message (str): 错误消息
        details (dict): 错误详细信息，包含资源类型和 ID
    """
    
    def __init__(self, message, details=None):
        """
        初始化资源不存在错误异常
        
        Args:
            message (str): 错误消息
            details (dict, optional): 错误详细信息。默认为 None。
                示例: {'resource': 'board', 'id': 123}
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DatabaseError(Exception):
    """
    数据库错误异常
    
    当数据库操作失败时抛出此异常。
    对应 HTTP 状态码 500 Internal Server Error。
    
    需求：10.2 - WHEN 数据库操作失败时，THE Backend SHALL 记录错误日志并返回错误响应
    需求：10.4 - WHEN 服务器内部错误时，THE Backend SHALL 返回 500 状态码和错误描述
    需求：10.5 - THE System SHALL 确保错误不会导致数据不一致
    
    Attributes:
        message (str): 错误消息
        original_error (Exception): 原始数据库异常对象
    """
    
    def __init__(self, message, original_error=None):
        """
        初始化数据库错误异常
        
        Args:
            message (str): 错误消息
            original_error (Exception, optional): 原始数据库异常对象。默认为 None。
        """
        super().__init__(message)
        self.message = message
        self.original_error = original_error


class AuthenticationError(Exception):
    """
    认证失败错误
    
    当用户名/密码错误时抛出此异常。
    对应 HTTP 状态码 401 Unauthorized。
    
    需求：2.3, 2.4 - 用户名或密码错误
    """
    
    def __init__(self, message="用户名或密码错误"):
        super().__init__(message)
        self.message = message


class TokenExpiredError(Exception):
    """
    令牌过期错误
    
    当 JWT 令牌过期时抛出此异常。
    对应 HTTP 状态码 401 Unauthorized。
    
    需求：3.2 - 令牌已过期
    """
    
    def __init__(self, message="令牌已过期，请重新登录"):
        super().__init__(message)
        self.message = message


class InvalidTokenError(Exception):
    """
    令牌无效错误
    
    当 JWT 令牌无效时抛出此异常。
    对应 HTTP 状态码 401 Unauthorized。
    
    需求：3.3 - 令牌无效
    """
    
    def __init__(self, message="令牌无效"):
        super().__init__(message)
        self.message = message


class UnauthorizedError(Exception):
    """
    未授权访问错误
    
    当请求未包含令牌时抛出此异常。
    对应 HTTP 状态码 401 Unauthorized。
    
    需求：3.4 - 未授权
    """
    
    def __init__(self, message="未授权，请先登录"):
        super().__init__(message)
        self.message = message


class ForbiddenError(Exception):
    """
    无权访问资源错误
    
    当用户尝试访问不属于自己的资源时抛出此异常。
    对应 HTTP 状态码 403 Forbidden。
    
    需求：4.2, 4.4, 4.5 - 无权访问
    """
    
    def __init__(self, message="无权访问该资源"):
        super().__init__(message)
        self.message = message

