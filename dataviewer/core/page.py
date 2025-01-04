from typing import List, Set

from ..components.base import Component, ComponentContext


class Page:
    """Page class, used to organize the rendering interface"""

    _additional_head_content: str = ""  # Used to store additional header content
    _init_flags: Set[str] = set()

    def __init__(self, title: str, padding: str = "4"):
        self.title = title
        self.padding = padding
        self.components: List[Component] = []

    def add(self, component: Component) -> None:
        """Add a component to the page"""
        if component not in self.components:  # Avoid duplicate addition
            self.components.append(component)

    def __enter__(self):
        """Support with statement"""
        ComponentContext.clear()  # Clear the component context
        ComponentContext.push(self)  # Add the page to the context
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Processing when exiting the with statement"""
        current = ComponentContext.pop()
        if (
            current is not self
        ):  # If the current context is not this page, it means the context stack is wrong
            ComponentContext.clear()  # Clear all contexts
            raise RuntimeError("Page context management error")

    def save(self, filename: str) -> None:
        """Save the page to an HTML file"""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.render())

    def render(self) -> str:
        """Generate the HTML content of the page"""
        components_html = "\n".join(
            component.to_html() for component in self.components if component
        )
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com/3.4.16"></script>
    <style>
        body {{
            width: 100%;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            width: 100%;
            margin: 0 auto;
        }}

        th, td, pre {{
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: break-spaces;
        }}
    </style>
    {self._additional_head_content}
</head>
<body>
    <div class="p-{self.padding}">
        {components_html}
    </div>
</body>
</html>"""
