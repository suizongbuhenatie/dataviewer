from dataviewer import Page, Table, Header, Tag, FlexRow, Container
from dataviewer import CellRendererRegistry, CellImageRenderer

# 清除之前的渲染器
CellRendererRegistry.clear()

# 注册新的渲染器
CellRendererRegistry.register(
    CellImageRenderer(
        patterns=[".png", ".jpg"], width="120px"  # 使用文件扩展名作为匹配模式  # 设置宽度为 120px
    )
)

# 准备数据
data = [
    {
        "name": f"产品{i}",
        "status": "在售" if i % 2 == 0 else "缺货",
        "price": f"¥{1000 + i * 100}",
        "description": f"这是一款高品质的产品{i},采用顶级材质精心打造,具有卓越的性能表现和时尚前卫的外观设计。产品经过严格的质量把控,具有超长使用寿命,是您工作生活的理想之选。我们提供完善的售后服务,让您购物无忧。",
        "image": [
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
            "examples/example.png",
        ],
        "image2": "examples/example.png",
        "image3": "examples/example.png",
        "image4": "examples/example.png",
        "image5": "examples/example.png",
        "image6": "examples/example.png",
        "image7": "examples/example.png",
        "image8": "examples/example.png",
        "image9": "examples/example.png",
        "image10": "examples/example.png",
    }
    for i in range(100)
]


def create_auto_columns_page():
    """创建使用自动推断columns的页面"""
    with Page("产品展示 - 自动列", padding="4") as page:
        Header("test", align="center")
        Table(
            data=data, hoverable=True,
        )

    page.save("products.html")


if __name__ == "__main__":
    create_auto_columns_page()
