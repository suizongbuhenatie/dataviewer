import pytest
from nestvis.components import TextInput, Button

def test_text_input_basic():
    """测试文本输入框基本功能"""
    text_input = TextInput()
    assert text_input.placeholder == ""
    assert text_input.value == ""
    assert text_input.label is None

def test_text_input_with_params():
    """测试带参数的文本输入框"""
    text_input = TextInput(
        placeholder="请输入...",
        value="初始值",
        label="用户名"
    )
    assert text_input.placeholder == "请输入..."
    assert text_input.value == "初始值"
    assert text_input.label == "用户名"

def test_button_basic():
    """测试按钮基本功能"""
    button = Button()
    assert button.text == "Button"
    assert button.onclick == ""
    assert button.label is None

def test_button_with_params():
    """测试带参数的按钮"""
    button = Button(
        text="提交",
        onclick="handleSubmit()",
        label="提交按钮"
    )
    assert button.text == "提交"
    assert button.onclick == "handleSubmit()"
    assert button.label == "提交按钮"

def test_button_custom_attributes():
    """测试按钮自定义属性"""
    button = Button(
        text="自定义",
        custom_class="primary",
        data_testid="submit-btn"
    )
    assert button.text == "自定义"
    assert button.custom_class == "primary"
    assert button.data_testid == "submit-btn"

def test_text_input_custom_attributes():
    """测试文本输入框自定义属性"""
    text_input = TextInput(
        type="password",
        required=True,
        maxlength=20
    )
    assert text_input.type == "password"
    assert text_input.required is True
    assert text_input.maxlength == 20 