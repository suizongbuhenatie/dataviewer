from dataclasses import dataclass
from typing import Optional

from .base import Component


"""Video Component"""

@dataclass
class Video(Component):
    src: str  # Video path
    width: int = 400  # Width (pixels)
    height: Optional[int] = None  # Height (pixels)
    css_class: str = ""  # CSS class name

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)

    def to_html(self) -> str:
        # Handle styles
        style = []
        if self.width:
            style.append(f"width: {self.width}px")
        if self.height:
            style.append(f"height: {self.height}px")

        style_attr = f' style="{"; ".join(style)}"' if style else ""

        # Handle class name
        classes = []
        if self.css_class:
            classes.extend(self.css_class.split())
        class_attr = f' class="{" ".join(classes)}"'

        width = f' width="{self.width}px"' if self.width else ""
        height = f' height="{self.height}px"' if self.height else ""
        return (
            f'<video{width}{height} controls loading="lazy">'
            f'<source src="{self.src}" type="video/mp4"></video>'
        )
