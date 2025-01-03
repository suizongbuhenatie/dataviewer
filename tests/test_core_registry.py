import pytest
import warnings
from dataviewer.core import ComponentRegistry
from dataviewer.components import Button, TextInput

def test_registry_singleton():
    """测试注册表单例模式"""
    registry1 = ComponentRegistry()
    registry2 = ComponentRegistry()
    assert registry1 is registry2

def test_component_registration():
    """测试组件注册"""
    registry = ComponentRegistry()
    button = Button(id="test-button")
    
    registry.register(button)
    assert registry.get("test-button") is button

def test_component_unregistration():
    """测试组件取消注册"""
    registry = ComponentRegistry()
    button = Button(id="test-button")
    
    registry.register(button)
    registry.unregister(button)
    assert registry.get("test-button") is None

def test_registry_clear():
    """测试清空注册表"""
    registry = ComponentRegistry()
    button1 = Button(id="button1")
    button2 = Button(id="button2")
    
    registry.register(button1)
    registry.register(button2)
    registry.clear()
    
    assert registry.get("button1") is None
    assert registry.get("button2") is None

def test_duplicate_id_warning():
    """测试重复ID警告"""
    registry = ComponentRegistry()
    button = Button(id="duplicate-id")
    text_input = TextInput(id="duplicate-id")
    
    registry.register(button)
    with pytest.warns(UserWarning):
        registry.register(text_input)

def test_get_nonexistent_component():
    """测试获取不存在的组件"""
    registry = ComponentRegistry()
    assert registry.get("nonexistent-id") is None

def test_multiple_components():
    """测试多个组件注册"""
    registry = ComponentRegistry()
    components = [
        Button(id=f"button-{i}") for i in range(5)
    ]
    
    for component in components:
        registry.register(component)
    
    for i, component in enumerate(components):
        assert registry.get(f"button-{i}") is component 