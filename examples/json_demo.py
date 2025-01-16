from dataviewer.components import FlexColumn, FlexRow, Header, JsonView
from dataviewer.core import Page

# Create an example JSON data
sample_data = {
    "name": "John",
    "age": 30,
    "hobbies": ["Reading", "Swimming", "Programming"],
    "address": {"city": "Beijing", "street": "Chaoyang Road", "number": 123},
    "married": True,
    "father": {"name": "John Sr.", "age": 55},
    "mother": {"name": "Mary", "age": 53},
    "siblings": [{"name": "Jane", "age": 25}],
}

# Create page
page = Page("JSON Component Demo")

with page:
    with FlexRow(gap="20px", justify="between"):
        with FlexColumn(padding="2"):
            Header("Dark Theme")
            JsonView(sample_data, theme="dark")

        with FlexColumn(padding="2"):
            Header("Light Theme")
            JsonView(sample_data, theme="light")

if __name__ == "__main__":
    page.save("output/json_demo.html")
