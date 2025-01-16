from dataviewer import Page
from dataviewer.components import FlexRow, Header, Image

# Create page
with Page("Image Component Demo") as page:
    # Add title
    Header("Image Component Demo", level=1)

    # Create a horizontal layout container and add images
    with FlexRow(justify="center", align="center", gap="20") as row:
        # Add three images of different sizes for comparison
        Image(src="example.jpg", width=200)
        Image(src="example.jpg", width=300)
        Image(src="example.jpg", width=400)

    # Save page
    page.save("output/image_demo.html")
