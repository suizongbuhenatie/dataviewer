import pytest
from nestvis.core import ComponentRegistry
from nestvis.components import Button, TextInput, FlexRow, Header

@pytest.fixture(autouse=True)
def clear_registry():
    """每个测试前自动清空组件注册表"""
    ComponentRegistry.clear()
    yield
    ComponentRegistry.clear()

@pytest.fixture
def sample_components():
    """返回一组示例组件"""
    return [
        Header(text="测试标题"),
        TextInput(placeholder="请输入"),
        Button(text="提交")
    ]

@pytest.fixture
def nested_layout():
    """返回一个嵌套布局示例"""
    return FlexRow(children=[
        Button(text="按钮1"),
        FlexRow(children=[
            Button(text="按钮2"),
            Button(text="按钮3")
        ])
    ]) 