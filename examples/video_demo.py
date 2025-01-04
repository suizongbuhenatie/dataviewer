from dataviewer import Page
from dataviewer.components import FlexRow, Header, Video

# 创建页面
with Page("视频组件演示") as page:
    # 添加标题
    Header("视频组件演示", level=1)

    # 创建一个水平布局容器并添加图片
    with FlexRow(justify="center", align="center", gap="20") as row:
        # 添加三张不同大小的图片以便区分
        Video(src="example.mp4", width=200)
        Video(src="example.mp4", width=300)
        Video(src="example.mp4", width=400)

    # 保存页面
    page.save("output/video_demo.html")
