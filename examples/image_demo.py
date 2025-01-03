from dataviewer import Page
from dataviewer.components import Image, Header, FlexRow

# 创建页面
with Page("图片组件演示") as page:
    # 添加标题
    Header("图片组件演示", level=1)
    
    # 创建一个水平布局容器并添加图片
    with FlexRow(justify="center", align="center", gap="20") as row:
        # 添加三张不同大小的图片以便区分
        Image(src="example.webp", width=200)
        Image(src="example.webp", width=300)
        Image(src="example.webp", width=400)
            
    # 保存页面
    page.save("output/image_demo.html")