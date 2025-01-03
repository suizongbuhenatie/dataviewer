from nestvis import Page
from nestvis.components import Table, Header

data = [
    {"id": 1, "name": "产品A", "price": 100, "description": "这是产品A的描述"},
    {"id": 2, "name": "产品B", "price": 200, "description": "这是产品B的描述"}, 
    {"id": 3, "name": "产品C", "price": 300, "description": "这是产品C的描述"}
]

with Page("表格演示") as page:
    Header("表格组件演示", level=1)
    Table(data=data, hoverable=True, striped=True)
    page.save("output/table_demo.html")