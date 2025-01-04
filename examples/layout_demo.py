from dataviewer import Page
from dataviewer.components import FlexColumn, FlexRow, Grid, Header, Tag

# 使用with语句创建页面和组件
with Page("布局演示", padding="6") as page:
    Header("布局组件演示", level=1)

    # 展示不同大小和颜色的标题
    Header("不同大小和颜色的标题演示", level=2, color="purple")
    Header("这是一级标题", level=1, color="blue")
    Header("这是二级标题", level=2, color="green")
    Header("这是三级标题", level=3, color="red")
    Header("这是四级标题", level=4, color="yellow")
    Header("这是五级标题", level=5, color="gray")

    Header("水平布局 (FlexRow)", level=2, color="green")
    with FlexRow(justify="between", gap="4") as row:
        [Tag(text=f"标签 {i+1}", color="blue") for i in range(3)]

    Header("垂直布局 (FlexColumn)", level=2, color="red")
    with FlexColumn(align="center", gap="4") as col:
        [Tag(text=f"标签 {i+1}", color="green") for i in range(3)]

    Header("网格布局 (Grid)", level=2, color="yellow")
    with Grid(cols=3, gap="4") as grid:
        [Tag(text=f"标签 {i+1}", color="red") for i in range(9)]

    page.save("output/layout_demo.html")
