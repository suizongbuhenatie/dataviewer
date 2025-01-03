# NestVis

一个简单易用的Python数据可视化工具,支持组件化开发和灵活布局。主要特点:

- 组件化开发,提供丰富的预置组件
- 支持灵活的布局系统(FlexRow、FlexColumn、Grid等)
- 内置多种主题和样式
- 简单直观的API设计

## 主要组件

### 布局组件
- `FlexRow`: 水平弹性布局容器
- `FlexColumn`: 垂直弹性布局容器
- `Grid`: 网格布局容器

### 展示组件
- `Table`: 表格组件，支持分页、排序、自定义列宽等功能
- `JsonView`: JSON数据可视化组件，支持折叠/展开、深色/浅色主题
- `Image`: 图片组件，支持懒加载和缩放
- `Header`: 标题组件，支持多级标题和对齐方式
- `Tag`: 标签组件，支持多种颜色和尺寸

## 使用示例

### 表格组件示例
```python
from nestvis.components import Table
from nestvis.core import Page

# 创建数据
data = [
    {"id": 1, "name": "张三", "age": 25},
    {"id": 2, "name": "李四", "age": 30}
]

# 创建页面
page = Page("表格示例")

# 添加表格组件
with page:
    Table(
        data=data,
        page_size=10,
        hoverable=True,
        striped=True,
        bordered=True
    )

# 保存页面
page.save("table_demo.html")
```

### JSON视图组件示例
```python
from nestvis.components import JsonView, FlexColumn
from nestvis.core import Page

# 示例JSON数据
data = {
    "name": "张三",
    "age": 30,
    "hobbies": ["读书", "游泳"],
    "address": {
        "city": "北京",
        "street": "朝阳路"
    }
}

# 创建页面
page = Page("JSON示例")

with page:
    with FlexColumn(padding="2"):
        JsonView(data, theme="dark")

page.save("json_demo.html")
```

### 布局组件示例
```python
from nestvis.components import FlexRow, FlexColumn, Header, Image
from nestvis.core import Page

page = Page("布局示例")

with page:
    with FlexRow(gap="20px", justify="between"):
        with FlexColumn(padding="2"):
            Header("左侧内容")
            Image("path/to/image.jpg", width=300)
        with FlexColumn(padding="2"):
            Header("右侧内容")
            Image("path/to/image2.jpg", width=300)

page.save("layout_demo.html")
```

## 组件属性说明

### Table 组件
- `data`: 表格数据列表
- `columns`: 可选的列配置
- `page_size`: 每页显示的行数
- `hoverable`: 是否启用悬停效果
- `striped`: 是否启用条纹样式
- `bordered`: 是否显示边框
- `sort_by`: 排序字段
- `sort_desc`: 是否降序排序

### JsonView 组件
- `data`: JSON数据
- `theme`: 主题样式 ("dark"/"light")
- `default_expand_level`: 默认展开层级

### Image 组件
- `src`: 图片路径
- `width`: 宽度（像素）
- `height`: 高度（像素）
- `alt`: 替代文本
- `lazy_load`: 是否启用懒加载

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进 NestVis。

## 许可证

本项目采用 MIT 许可证。
