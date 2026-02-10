"""
输入验证工具

本模块提供数据验证函数，用于验证 API 请求数据的有效性。
这些函数在路由处理器中被调用，确保数据符合业务规则和约束。

需求：6.3 - WHEN 前端发送请求时，THE Backend SHALL 验证请求的有效性
需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
"""

from utils.exceptions import ValidationError


def validate_required_fields(data, required_fields):
    """
    验证必需字段是否存在
    
    检查数据字典中是否包含所有必需的字段。
    如果缺少任何必需字段，抛出 ValidationError 异常。
    
    需求：6.3 - WHEN 前端发送请求时，THE Backend SHALL 验证请求的有效性
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Args:
        data (dict): 要验证的数据字典
        required_fields (list): 必需字段名称列表
        
    Raises:
        ValidationError: 当缺少必需字段时
        
    Examples:
        >>> validate_required_fields({'name': 'Test'}, ['name'])
        # 通过验证，不抛出异常
        
        >>> validate_required_fields({'title': 'Test'}, ['name', 'title'])
        # 抛出 ValidationError: 缺少必需字段: name
    """
    if not isinstance(data, dict):
        raise ValidationError(
            "无效的请求数据格式",
            details={'constraint': 'type', 'expected': 'dict', 'actual': type(data).__name__}
        )
    
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(
            f"缺少必需字段: {', '.join(missing_fields)}",
            details={'missing_fields': missing_fields, 'constraint': 'required'}
        )


def validate_non_empty_string(value, field_name):
    """
    验证字符串非空且不仅包含空白字符
    
    检查字符串值是否为有效的非空字符串。
    空字符串、None 或仅包含空白字符的字符串都被视为无效。
    
    需求：1.2 - WHEN 用户创建看板时，THE System SHALL 要求提供看板名称
    需求：2.2 - WHEN 用户创建列表时，THE System SHALL 要求提供列表名称
    需求：3.3 - WHEN 用户创建卡片时，THE System SHALL 要求提供卡片标题
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Args:
        value: 要验证的值
        field_name (str): 字段名称，用于错误消息
        
    Raises:
        ValidationError: 当字符串为空或仅包含空白字符时
        
    Examples:
        >>> validate_non_empty_string('Test Board', 'name')
        # 通过验证，不抛出异常
        
        >>> validate_non_empty_string('', 'name')
        # 抛出 ValidationError: name 不能为空
        
        >>> validate_non_empty_string('   ', 'name')
        # 抛出 ValidationError: name 不能为空
        
        >>> validate_non_empty_string(None, 'name')
        # 抛出 ValidationError: name 不能为空
    """
    if value is None or not isinstance(value, str) or not value.strip():
        raise ValidationError(
            f"{field_name} 不能为空",
            details={'field': field_name, 'constraint': 'non_empty_string'}
        )


def validate_type(value, field_name, expected_type):
    """
    验证数据类型
    
    检查值是否为预期的数据类型。
    支持基本类型（str, int, float, bool）和复杂类型（list, dict）。
    
    需求：6.3 - WHEN 前端发送请求时，THE Backend SHALL 验证请求的有效性
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Args:
        value: 要验证的值
        field_name (str): 字段名称，用于错误消息
        expected_type (type): 预期的数据类型
        
    Raises:
        ValidationError: 当值的类型不匹配时
        
    Examples:
        >>> validate_type(123, 'position', int)
        # 通过验证，不抛出异常
        
        >>> validate_type('123', 'position', int)
        # 抛出 ValidationError: position 必须是 int 类型
        
        >>> validate_type(['tag1', 'tag2'], 'tags', list)
        # 通过验证，不抛出异常
    """
    if not isinstance(value, expected_type):
        raise ValidationError(
            f"{field_name} 必须是 {expected_type.__name__} 类型",
            details={
                'field': field_name,
                'constraint': 'type',
                'expected': expected_type.__name__,
                'actual': type(value).__name__
            }
        )


def validate_positive_integer(value, field_name):
    """
    验证正整数
    
    检查值是否为非负整数（包括 0）。
    用于验证位置（position）等字段。
    
    需求：2.6 - THE System SHALL 允许用户通过拖拽重新排列列表的顺序
    需求：4.1 - THE System SHALL 允许用户在同一列表内拖拽卡片改变顺序
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Args:
        value: 要验证的值
        field_name (str): 字段名称，用于错误消息
        
    Raises:
        ValidationError: 当值不是非负整数时
        
    Examples:
        >>> validate_positive_integer(0, 'position')
        # 通过验证，不抛出异常
        
        >>> validate_positive_integer(5, 'position')
        # 通过验证，不抛出异常
        
        >>> validate_positive_integer(-1, 'position')
        # 抛出 ValidationError: position 必须是非负整数
        
        >>> validate_positive_integer('5', 'position')
        # 抛出 ValidationError: position 必须是整数类型
    """
    if not isinstance(value, int):
        raise ValidationError(
            f"{field_name} 必须是整数类型",
            details={
                'field': field_name,
                'constraint': 'type',
                'expected': 'int',
                'actual': type(value).__name__
            }
        )
    
    if value < 0:
        raise ValidationError(
            f"{field_name} 必须是非负整数",
            details={
                'field': field_name,
                'constraint': 'positive_integer',
                'value': value
            }
        )


def validate_string_length(value, field_name, max_length):
    """
    验证字符串长度
    
    检查字符串长度是否不超过最大长度限制。
    用于验证名称、标题等有长度限制的字段。
    
    需求：6.3 - WHEN 前端发送请求时，THE Backend SHALL 验证请求的有效性
    需求：10.3 - WHEN 用户输入无效数据时，THE System SHALL 显示验证错误信息
    
    Args:
        value (str): 要验证的字符串
        field_name (str): 字段名称，用于错误消息
        max_length (int): 最大长度限制
        
    Raises:
        ValidationError: 当字符串长度超过限制时
        
    Examples:
        >>> validate_string_length('Test', 'name', 255)
        # 通过验证，不抛出异常
        
        >>> validate_string_length('A' * 256, 'name', 255)
        # 抛出 ValidationError: name 长度不能超过 255 个字符
    """
    if not isinstance(value, str):
        raise ValidationError(
            f"{field_name} 必须是字符串类型",
            details={
                'field': field_name,
                'constraint': 'type',
                'expected': 'str',
                'actual': type(value).__name__
            }
        )
    
    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} 长度不能超过 {max_length} 个字符",
            details={
                'field': field_name,
                'constraint': 'max_length',
                'max_length': max_length,
                'actual_length': len(value)
            }
        )
