from dataclasses import dataclass
from typing import Optional

from .base import Component


@dataclass
class Video(Component):
    """视频组件"""

    src: str  # 视频路径
    width: int = 400  # 宽度（像素）
    height: Optional[int] = None  # 高度（像素）
    css_class: str = ""  # CSS类名

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)

    def to_html(self) -> str:
        # 处理样式
        style = []
        if self.width:
            style.append(f"width: {self.width}px")
        if self.height:
            style.append(f"height: {self.height}px")

        style_attr = f' style="{"; ".join(style)}"' if style else ""

        # 处理类名
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