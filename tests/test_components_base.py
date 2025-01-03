import pytest
from dataviewer.components import Component, LabeledComponent


def test_component_id_generation():
    """测试组件ID的自动生成"""
    component1 = Component()
    component2 = Component()
    assert component1.id.startswith("component-")
    assert component2.id.startswith("component-")
    assert component1.id != component2.id


def test_component_custom_id():
    """测试自定义组件ID"""
    component = Component(id="custom-id")
    assert component.id == "custom-id"


def test_component_invalid_id():
    """测试无效的组件ID"""
    with pytest.raises(ValueError):
        Component(id="invalid@id")
    with pytest.raises(ValueError):
        Component(id="")


def test_labeled_component():
    """测试带标签的组件"""
    component = LabeledComponent(label="测试标签")
    assert component.label == "测试标签"
    assert component.id.startswith("labeledcomponent-")


def test_labeled_component_without_label():
    """测试不带标签的LabeledComponent"""
    component = LabeledComponent()
    assert component.label is None


def test_component_kwargs():
    """测试组件的kwargs处理"""
    component = Component(custom_attr="test")
    assert hasattr(component, "custom_attr")
    assert component.custom_attr == "test"
