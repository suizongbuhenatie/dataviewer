from dataviewer import Page
from dataviewer.components import FlexRow, Header, Video

# Create page
with Page("Video Component Demo") as page:
    # Add title
    Header("Video Component Demo", level=1)

    # Create a horizontal layout container and add videos
    with FlexRow(justify="center", align="center", gap="20") as row:
        # Add three videos of different sizes for comparison
        Video(src="example.mp4", width=200)
        Video(src="example.mp4", width=300)
        Video(src="example.mp4", width=400)

    # Save page
    page.save("output/video_demo.html")
