"""
输入验证工具单元测试

本模块测试 utils/validators.py 中的验证函数。
测试覆盖正常情况、边缘情况和错误情况。

需求：6.3, 10.3
"""

import pytest
from utils.validators import (
    validate_required_fields,
    validate_non_empty_string,
    validate_type,
    validate_positive_integer,
    validate_string_length
)
from utils.exceptions import ValidationError


class TestValidateRequiredFields:
    """测试 validate_required_fields 函数"""
    
    def test_valid_data_with_all_required_fields(self):
        """测试包含所有必需字段的有效数据"""
        data = {'name': 'Test Board', 'description': 'Test'}
        validate_required_fields(data, ['name'])
        # 不应抛出异常
    
    def test_valid_data_with_multiple_required_fields(self):
        """测试包含多个必需字段的有效数据"""
        data = {'name': 'Test', 'title': 'Title', 'position': 0}
        validate_required_fields(data, ['name', 'title', 'position'])
        # 不应抛出异常
    
    def test_missing_single_required_field(self):
        """测试缺少单个必需字段"""
        data = {'description': 'Test'}
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, ['name'])
        
        assert '缺少必需字段' in str(exc_info.value)
        assert 'name' in str(exc_info.value)
        assert exc_info.value.details['constraint'] == 'required'
        assert 'name' in exc_info.value.details['missing_fields']
    
    def test_missing_multiple_required_fields(self):
        """测试缺少多个必需字段"""
        data = {'description': 'Test'}
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, ['name', 'title'])
        
        assert '缺少必需字段' in str(exc_info.value)
        assert exc_info.value.details['constraint'] == 'required'
        assert set(exc_info.value.details['missing_fields']) == {'name', 'title'}
    
    def test_empty_required_fields_list(self):
        """测试空的必需字段列表"""
        data = {'name': 'Test'}
        validate_required_fields(data, [])
        # 不应抛出异常
    
    def test_invalid_data_type(self):
        """测试无效的数据类型（非字典）"""
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields("not a dict", ['name'])
        
        assert '无效的请求数据格式' in str(exc_info.value)
        assert exc_info.value.details['constraint'] == 'type'
        assert exc_info.value.details['expected'] == 'dict'
    
    def test_none_as_data(self):
        """测试 None 作为数据"""
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(None, ['name'])
        
        assert '无效的请求数据格式' in str(exc_info.value)
    
    def test_field_with_none_value(self):
        """测试字段值为 None（字段存在但值为 None）"""
        data = {'name': None}
        validate_required_fields(data, ['name'])
        # 字段存在，即使值为 None 也通过验证
        # 值的验证由其他验证函数负责


class TestValidateNonEmptyString:
    """测试 validate_non_empty_string 函数"""
    
    def test_valid_non_empty_string(self):
        """测试有效的非空字符串"""
        validate_non_empty_string('Test Board', 'name')
        # 不应抛出异常
    
    def test_valid_string_with_spaces(self):
        """测试包含空格的有效字符串"""
        validate_non_empty_string('Test Board Name', 'name')
        # 不应抛出异常
    
    def test_valid_string_with_special_characters(self):
        """测试包含特殊字符的有效字符串"""
        validate_non_empty_string('Test-Board_123!', 'name')
        # 不应抛出异常
    
    def test_empty_string(self):
        """测试空字符串"""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string('', 'name')
        
        assert 'name 不能为空' in str(exc_info.value)
        assert exc_info.value.details['field'] == 'name'
        assert exc_info.value.details['constraint'] == 'non_empty_string'
    
    def test_whitespace_only_string(self):
        """测试仅包含空白字符的字符串"""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string('   ', 'name')
        
        assert 'name 不能为空' in str(exc_info.value)
        assert exc_info.value.details['field'] == 'name'
    
    def test_tab_and_newline_only_string(self):
        """测试仅包含制表符和换行符的字符串"""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string('\t\n\r', 'name')
        
        assert 'name 不能为空' in str(exc_info.value)
    
    def test_none_value(self):
        """测试 None 值"""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string(None, 'name')
        
        assert 'name 不能为空' in str(exc_info.value)
    
    def test_non_string_type(self):
        """测试非字符串类型"""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string(123, 'name')
        
        assert 'name 不能为空' in str(exc_info.value)
    
    def test_string_with_leading_trailing_spaces(self):
        """测试前后有空格但中间有内容的字符串"""
        validate_non_empty_string('  Test  ', 'name')
        # 应该通过验证，因为 strip() 后不为空


class TestValidateType:
    """测试 validate_type 函数"""
    
    def test_valid_string_type(self):
        """测试有效的字符串类型"""
        validate_type('test', 'name', str)
        # 不应抛出异常
    
    def test_valid_integer_type(self):
        """测试有效的整数类型"""
        validate_type(123, 'position', int)
        # 不应抛出异常
    
    def test_valid_float_type(self):
        """测试有效的浮点数类型"""
        validate_type(3.14, 'value', float)
        # 不应抛出异常
    
    def test_valid_boolean_type(self):
        """测试有效的布尔类型"""
        validate_type(True, 'flag', bool)
        # 不应抛出异常
    
    def test_valid_list_type(self):
        """测试有效的列表类型"""
        validate_type(['tag1', 'tag2'], 'tags', list)
        # 不应抛出异常
    
    def test_valid_dict_type(self):
        """测试有效的字典类型"""
        validate_type({'key': 'value'}, 'data', dict)
        # 不应抛出异常
    
    def test_invalid_type_string_instead_of_int(self):
        """测试类型不匹配：字符串而非整数"""
        with pytest.raises(ValidationError) as exc_info:
            validate_type('123', 'position', int)
        
        assert 'position 必须是 int 类型' in str(exc_info.value)
        assert exc_info.value.details['field'] == 'position'
        assert exc_info.value.details['constraint'] == 'type'
        assert exc_info.value.details['expected'] == 'int'
        assert exc_info.value.details['actual'] == 'str'
    
    def test_invalid_type_int_instead_of_string(self):
        """测试类型不匹配：整数而非字符串"""
        with pytest.raises(ValidationError) as exc_info:
            validate_type(123, 'name', str)
        
        assert 'name 必须是 str 类型' in str(exc_info.value)
    
    def test_invalid_type_dict_instead_of_list(self):
        """测试类型不匹配：字典而非列表"""
        with pytest.raises(ValidationError) as exc_info:
            validate_type({'key': 'value'}, 'tags', list)
        
        assert 'tags 必须是 list 类型' in str(exc_info.value)
    
    def test_none_value(self):
        """测试 None 值"""
        with pytest.raises(ValidationError) as exc_info:
            validate_type(None, 'name', str)
        
        assert 'name 必须是 str 类型' in str(exc_info.value)
    
    def test_zero_is_valid_int(self):
        """测试 0 是有效的整数"""
        validate_type(0, 'position', int)
        # 不应抛出异常
    
    def test_empty_list_is_valid(self):
        """测试空列表是有效的列表类型"""
        validate_type([], 'tags', list)
        # 不应抛出异常


class TestValidatePositiveInteger:
    """测试 validate_positive_integer 函数"""
    
    def test_valid_zero(self):
        """测试 0 是有效的非负整数"""
        validate_positive_integer(0, 'position')
        # 不应抛出异常
    
    def test_valid_positive_integer(self):
        """测试正整数"""
        validate_positive_integer(5, 'position')
        validate_positive_integer(100, 'position')
        validate_positive_integer(999999, 'position')
        # 不应抛出异常
    
    def test_negative_integer(self):
        """测试负整数"""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer(-1, 'position')
        
        assert 'position 必须是非负整数' in str(exc_info.value)
        assert exc_info.value.details['field'] == 'position'
        assert exc_info.value.details['constraint'] == 'positive_integer'
        assert exc_info.value.details['value'] == -1
    
    def test_string_number(self):
        """测试字符串形式的数字"""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer('5', 'position')
        
        assert 'position 必须是整数类型' in str(exc_info.value)
        assert exc_info.value.details['constraint'] == 'type'
    
    def test_float_number(self):
        """测试浮点数"""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer(5.5, 'position')
        
        assert 'position 必须是整数类型' in str(exc_info.value)
    
    def test_none_value(self):
        """测试 None 值"""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer(None, 'position')
        
        assert 'position 必须是整数类型' in str(exc_info.value)
    
    def test_boolean_value(self):
        """测试布尔值（在 Python 中 bool 是 int 的子类）"""
        # 注意：在 Python 中，bool 是 int 的子类，True == 1, False == 0
        # 这个测试验证布尔值会被接受（虽然在实际使用中应该避免）
        validate_positive_integer(True, 'position')  # True == 1
        validate_positive_integer(False, 'position')  # False == 0
        # 不应抛出异常


class TestValidateStringLength:
    """测试 validate_string_length 函数"""
    
    def test_valid_string_within_limit(self):
        """测试长度在限制内的字符串"""
        validate_string_length('Test', 'name', 255)
        validate_string_length('A' * 255, 'name', 255)
        # 不应抛出异常
    
    def test_empty_string_within_limit(self):
        """测试空字符串（长度为 0）"""
        validate_string_length('', 'name', 255)
        # 不应抛出异常（长度验证不检查是否为空）
    
    def test_string_exceeds_limit(self):
        """测试超过长度限制的字符串"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string_length('A' * 256, 'name', 255)
        
        assert 'name 长度不能超过 255 个字符' in str(exc_info.value)
        assert exc_info.value.details['field'] == 'name'
        assert exc_info.value.details['constraint'] == 'max_length'
        assert exc_info.value.details['max_length'] == 255
        assert exc_info.value.details['actual_length'] == 256
    
    def test_string_exactly_at_limit(self):
        """测试长度恰好等于限制的字符串"""
        validate_string_length('A' * 100, 'name', 100)
        # 不应抛出异常
    
    def test_non_string_type(self):
        """测试非字符串类型"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string_length(123, 'name', 255)
        
        assert 'name 必须是字符串类型' in str(exc_info.value)
        assert exc_info.value.details['constraint'] == 'type'
    
    def test_none_value(self):
        """测试 None 值"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string_length(None, 'name', 255)
        
        assert 'name 必须是字符串类型' in str(exc_info.value)
    
    def test_unicode_characters(self):
        """测试 Unicode 字符（中文等）"""
        validate_string_length('测试看板名称', 'name', 255)
        # 不应抛出异常
        
        # 测试超长的中文字符串
        with pytest.raises(ValidationError) as exc_info:
            validate_string_length('测' * 256, 'name', 255)
        
        assert 'name 长度不能超过 255 个字符' in str(exc_info.value)
    
    def test_different_max_lengths(self):
        """测试不同的最大长度限制"""
        validate_string_length('Test', 'name', 10)
        validate_string_length('Test', 'name', 4)
        
        with pytest.raises(ValidationError):
            validate_string_length('Test', 'name', 3)


class TestValidationIntegration:
    """测试验证函数的集成使用场景"""
    
    def test_validate_board_creation_data(self):
        """测试看板创建数据的完整验证"""
        data = {'name': 'Test Board'}
        
        # 验证必需字段
        validate_required_fields(data, ['name'])
        
        # 验证名称非空
        validate_non_empty_string(data['name'], 'name')
        
        # 验证名称长度
        validate_string_length(data['name'], 'name', 255)
        
        # 所有验证都应通过
    
    def test_validate_list_creation_data(self):
        """测试列表创建数据的完整验证"""
        data = {'name': 'To Do', 'position': 0}
        
        # 验证必需字段
        validate_required_fields(data, ['name'])
        
        # 验证名称非空
        validate_non_empty_string(data['name'], 'name')
        
        # 验证位置是非负整数
        if 'position' in data:
            validate_positive_integer(data['position'], 'position')
        
        # 所有验证都应通过
    
    def test_validate_card_creation_data(self):
        """测试卡片创建数据的完整验证"""
        data = {
            'title': 'Implement feature',
            'description': 'Add new functionality',
            'tags': ['backend', 'urgent'],
            'position': 0
        }
        
        # 验证必需字段
        validate_required_fields(data, ['title'])
        
        # 验证标题非空
        validate_non_empty_string(data['title'], 'title')
        
        # 验证标题长度
        validate_string_length(data['title'], 'title', 255)
        
        # 验证可选字段类型
        if 'description' in data and data['description'] is not None:
            validate_type(data['description'], 'description', str)
        
        if 'tags' in data and data['tags'] is not None:
            validate_type(data['tags'], 'tags', list)
        
        if 'position' in data:
            validate_positive_integer(data['position'], 'position')
        
        # 所有验证都应通过
    
    def test_validate_invalid_board_data(self):
        """测试无效的看板数据"""
        # 缺少必需字段
        with pytest.raises(ValidationError):
            validate_required_fields({}, ['name'])
        
        # 空名称
        with pytest.raises(ValidationError):
            validate_non_empty_string('', 'name')
        
        # 名称过长
        with pytest.raises(ValidationError):
            validate_string_length('A' * 256, 'name', 255)
    
    def test_validate_invalid_position_data(self):
        """测试无效的位置数据"""
        # 负数位置
        with pytest.raises(ValidationError):
            validate_positive_integer(-1, 'position')
        
        # 字符串位置
        with pytest.raises(ValidationError):
            validate_positive_integer('0', 'position')
