import pytest
from dataviewer.components import Header, Tag, Table


def test_header_basic():
    """测试标题基本功能"""
    header = Header(text="测试标题")
    assert header.text == "测试标题"
    assert header.level == 1
    assert header.align == "left"


def test_header_with_params():
    """测试带参数的标题"""
    header = Header(text="自定义标题", level=2, align="center")
    assert header.text == "自定义标题"
    assert header.level == 2
    assert header.align == "center"


def test_header_invalid_level():
    """测试无效的标题级别"""
    with pytest.raises(ValueError):
        Header(text="标题", level=7)
    with pytest.raises(ValueError):
        Header(text="标题", level=0)


def test_tag_basic():
    """测试标签基本功能"""
    tag = Tag(text="测试标签")
    assert tag.text == "测试标签"
    assert tag.color == "blue"
    assert tag.size == "md"


def test_tag_with_params():
    """测试带参数的标签"""
    tag = Tag(text="自定义标签", color="green", size="lg")
    assert tag.text == "自定义标签"
    assert tag.color == "green"
    assert tag.size == "lg"


def test_table_basic():
    """测试表格基本功能"""
    data = [{"id": 1, "name": "测试1"}, {"id": 2, "name": "测试2"}]
    table = Table(data=data)
    assert table.data == data
    # columns 会自动从数据中推断
    expected_columns = [{"key": "id", "title": "Id"}, {"key": "name", "title": "Name"}]
    assert table.columns == expected_columns
    assert table.page_size is None
    assert table.current_page == 1


def test_table_empty_data():
    """测试空数据表格"""
    table = Table(data=[])
    assert table.data == []
    assert table.columns == []


def test_table_infer_columns_with_different_keys():
    """测试不同行具有不同键的情况下的列推断"""
    data = [
        {"id": 1, "name": "测试1"},
        {"id": 2, "name": "测试2", "extra": "额外"},
        {"name": "测试3", "age": 25},
    ]
    table = Table(data=data)
    expected_columns = [
        {"key": "age", "title": "Age"},
        {"key": "extra", "title": "Extra"},
        {"key": "id", "title": "Id"},
        {"key": "name", "title": "Name"},
    ]
    assert table.columns == expected_columns


def test_table_manual_columns():
    """测试手动指定列"""
    data = [{"id": 1, "name": "测试1"}, {"id": 2, "name": "测试2"}]
    custom_columns = [{"key": "id", "title": "编号"}, {"key": "name", "title": "名称"}]
    table = Table(data=data, columns=custom_columns)
    assert table.columns == custom_columns


def test_table_manual_columns_subset():
    """测试手动指定部分列"""
    data = [{"id": 1, "name": "测试1", "age": 25}, {"id": 2, "name": "测试2", "age": 30}]
    custom_columns = [{"key": "name", "title": "名称"}, {"key": "age", "title": "年龄"}]
    table = Table(data=data, columns=custom_columns)
    assert table.columns == custom_columns


def test_table_with_params():
    """测试带参数的表格"""
    data = [{"id": 1, "name": "测试1"}, {"id": 2, "name": "测试2"}]
    columns = [{"key": "id", "title": "ID"}, {"key": "name", "title": "名称"}]
    table = Table(
        data=data, columns=columns, page_size=10, hoverable=True, resizable=True
    )
    assert table.data == data
    assert table.columns == columns
    assert table.page_size == 10
    assert table.hoverable is True
    assert table.resizable is True


def test_table_sorting():
    """测试表格排序功能"""
    data = [{"id": 1, "name": "测试1"}, {"id": 2, "name": "测试2"}]
    table = Table(data=data, sort_by="id", sort_desc=True)
    assert table.sort_by == "id"
    assert table.sort_desc is True


def test_table_column_width():
    """测试表格列宽设置"""
    table = Table(data=[], min_column_width=100, max_column_width=300)
    assert table.min_column_width == 100
    assert table.max_column_width == 300
