from dataviewer.components import JsonView, FlexColumn, Header, FlexRow
from dataviewer.core import Page

# 创建一个示例JSON数据
sample_data = {
    "name": "张三",
    "age": 30,
    "is_student": False,
    "hobbies": ["读书", "游泳", "编程"],
    "address": {"city": "北京", "street": "朝阳路", "number": 123},
    "family": {
        "father": {"name": "张大山", "age": 55},
        "mother": {"name": "李小花", "age": 53},
        "siblings": [{"name": "张小妹", "age": 25}],
    },
}

# 创建页面
page = Page("JSON组件演示")

with page:
    with FlexRow(gap="20px", justify="between"):
        with FlexColumn(padding="2"):
            Header("深色主题")
            JsonView(sample_data, theme="dark")

        with FlexColumn(padding="2"):
            Header("浅色主题")
            JsonView(sample_data, theme="light")

if __name__ == "__main__":
    page.save("output/json_demo.html")
