import pytest
from dataviewer.components import Container, FlexRow, FlexColumn, Grid, Button


def test_container_basic():
    """测试容器基本功能"""
    container = Container()
    assert container.children is None
    assert container.gap == "4"


def test_container_with_children():
    """测试带子组件的容器"""
    button1 = Button(text="按钮1")
    button2 = Button(text="按钮2")
    container = Container(children=[button1, button2])
    assert len(container.children) == 2
    assert container.children[0].text == "按钮1"
    assert container.children[1].text == "按钮2"


def test_flex_row():
    """测试水平弹性布局"""
    row = FlexRow(justify="center", align="center", wrap=True)
    assert row.justify == "center"
    assert row.align == "center"
    assert row.wrap is True


def test_flex_row_defaults():
    """测试水平弹性布局默认值"""
    row = FlexRow()
    assert row.justify == "start"
    assert row.align == "start"
    assert row.wrap is False


def test_flex_column():
    """测试垂直弹性布局"""
    column = FlexColumn(justify="between", align="stretch")
    assert column.justify == "between"
    assert column.align == "stretch"


def test_flex_column_defaults():
    """测试垂直弹性布局默认值"""
    column = FlexColumn()
    assert column.justify == "start"
    assert column.align == "start"


def test_grid():
    """测试网格布局"""
    grid = Grid(cols=3, rows=2, gap="8")
    assert grid.cols == 3
    assert grid.rows == 2
    assert grid.gap == "8"


def test_grid_defaults():
    """测试网格布局默认值"""
    grid = Grid()
    assert grid.cols == 2
    assert grid.rows is None
    assert grid.gap == "4"


def test_nested_containers():
    """测试嵌套容器"""
    button1 = Button(text="按钮1")
    button2 = Button(text="按钮2")
    row = FlexRow(children=[button1])
    column = FlexColumn(children=[row, button2])

    assert len(column.children) == 2
    assert isinstance(column.children[0], FlexRow)
    assert isinstance(column.children[1], Button)
    assert column.children[0].children[0].text == "按钮1"
    assert column.children[1].text == "按钮2"
