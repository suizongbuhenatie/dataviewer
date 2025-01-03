import pytest
import os
from nestvis.core import Page
from nestvis.components import Button, TextInput, FlexRow, Header

def test_page_creation():
    """测试页面创建"""
    page = Page("测试页面")
    assert page.title == "测试页面"
    assert len(page.components) == 0

def test_add_component():
    """测试添加组件"""
    page = Page("测试页面")
    button = Button(text="测试按钮")
    
    page.add(button)
    assert len(page.components) == 1
    assert page.components[0] is button

def test_multiple_components():
    """测试添加多个组件"""
    page = Page("测试页面")
    components = [
        Header(text="标题"),
        TextInput(placeholder="输入"),
        Button(text="提交")
    ]
    
    for component in components:
        page.add(component)
    
    assert len(page.components) == 3
    assert all(a is b for a, b in zip(page.components, components))

def test_with_context():
    """测试with语句上下文"""
    with Page("测试页面") as page:
        button = Button(text="测试按钮")
        page.add(button)
    
    assert len(page.components) == 1
    assert isinstance(page.components[0], Button)

def test_nested_components():
    """测试嵌套组件"""
    page = Page("测试页面")
    row = FlexRow(children=[
        Button(text="按钮1"),
        Button(text="按钮2")
    ])
    page.add(row)
    
    assert len(page.components) == 1
    assert isinstance(page.components[0], FlexRow)
    assert len(page.components[0].children) == 2

def test_page_render():
    """测试页面渲染"""
    page = Page("测试页面")
    button = Button(text="测试按钮")
    page.add(button)
    
    html = page.render()
    assert "测试页面" in html
    assert "tailwindcss" in html
    assert '<div class="container">' in html

def test_page_save(tmp_path):
    """测试页面保存"""
    output_file = tmp_path / "test.html"
    page = Page("测试页面")
    button = Button(text="测试按钮")
    page.add(button)
    
    page.save(str(output_file))
    assert output_file.exists()
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "测试页面" in content
        assert "tailwindcss" in content

def test_additional_head_content():
    """测试额外的头部内容"""
    page = Page("测试页面")
    page._additional_head_content = '<style>.custom { color: red; }</style>'
    
    html = page.render()
    assert '<style>.custom { color: red; }</style>' in html 