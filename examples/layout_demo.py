from dataviewer import Page
from dataviewer.components import FlexColumn, FlexRow, Grid, Header, Tag

# Create page and components using with statement
with Page("Layout Demo", padding="6") as page:
    Header("Layout Components Demo", level=1)

    # Show different sizes and colors of headers
    Header("Different Sizes and Colors of Headers Demo", level=2, color="purple")
    Header("This is H1 Header", level=1, color="blue")
    Header("This is H2 Header", level=2, color="green")
    Header("This is H3 Header", level=3, color="red")
    Header("This is H4 Header", level=4, color="yellow")
    Header("This is H5 Header", level=5, color="gray")

    Header("Horizontal Layout (FlexRow)", level=2, color="green")
    with FlexRow(justify="between", gap="4") as row:
        [Tag(text=f"Tag {i+1}", color="blue") for i in range(3)]

    Header("Vertical Layout (FlexColumn)", level=2, color="red")
    with FlexColumn(align="center", gap="4") as col:
        [Tag(text=f"Tag {i+1}", color="green") for i in range(3)]

    Header("Grid Layout (Grid)", level=2, color="yellow")
    with Grid(cols=3, gap="4") as grid:
        [Tag(text=f"Tag {i+1}", color="red") for i in range(9)]

    page.save("output/layout_demo.html")
