from dataclasses import dataclass, field
from typing import List, Optional

from .base import Component


@dataclass
class Container(Component):
    """容器基类，用于布局"""

    gap: str = "4"  # gap between items
    padding: str = "0"  # padding
    margin: str = "0"  # margin
    children: Optional[List[Component]] = None  # 子组件列表

    def __init__(
        self, id: Optional[str] = None, padding: str = "0", margin: str = "0", **kwargs
    ):
        if "children" in kwargs:
            self.children = kwargs.pop("children")
        self.padding = padding
        self.margin = margin
        super().__init__(id=id, **kwargs)
        if self.children is None:
            self.children = []

    def add(self, component: Component) -> None:
        """添加子组件"""
        if self.children is None:
            self.children = []
        if component not in self.children:  # 避免重复添加
            self.children.append(component)

    def to_html(self) -> str:
        if not self.children:
            return ""
        children_html = "\n".join(child.to_html() for child in (self.children or []))
        classes = [f"space-y-{self.gap}", f"p-{self.padding}", f"m-{self.margin}"]
        return f"""
        <div id="{self.id}" class="{' '.join(classes)}">
            {children_html}
        </div>
        """


@dataclass
class FlexRow(Container):
    """水平弹性布局"""

    justify: str = "start"  # start, end, center, between, around
    align: str = "start"  # start, end, center, stretch
    wrap: bool = False

    def __init__(
        self,
        justify: str = "start",
        align: str = "start",
        wrap: bool = False,
        id: Optional[str] = None,
        padding: str = "0",
        margin: str = "0",
        **kwargs,
    ):
        self.justify = justify
        self.align = align
        self.wrap = wrap
        super().__init__(id=id, padding=padding, margin=margin, **kwargs)

    def to_html(self) -> str:
        if not self.children:
            return ""

        justify_map = {
            "start": "justify-start",
            "end": "justify-end",
            "center": "justify-center",
            "between": "justify-between",
            "around": "justify-around",
        }

        align_map = {
            "start": "items-start",
            "end": "items-end",
            "center": "items-center",
            "stretch": "items-stretch",
        }

        classes = [
            "flex",
            justify_map.get(self.justify, "justify-start"),
            align_map.get(self.align, "items-start"),
            f"gap-{self.gap}",
            f"p-{self.padding}",
            f"m-{self.margin}",
        ]

        if self.wrap:
            classes.append("flex-wrap")

        children_html = "\n".join(child.to_html() for child in self.children)
        return f"""
        <div id="{self.id}" class="{' '.join(classes)}">
            {children_html}
        </div>
        """


@dataclass
class FlexColumn(Container):
    """垂直弹性布局"""

    justify: str = "start"  # start, end, center, between, around
    align: str = "start"  # start, end, center, stretch

    def __init__(
        self,
        justify: str = "start",
        align: str = "start",
        id: Optional[str] = None,
        padding: str = "0",
        margin: str = "0",
        **kwargs,
    ):
        self.justify = justify
        self.align = align
        super().__init__(id=id, padding=padding, margin=margin, **kwargs)

    def to_html(self) -> str:
        if not self.children:
            return ""

        justify_map = {
            "start": "justify-start",
            "end": "justify-end",
            "center": "justify-center",
            "between": "justify-between",
            "around": "justify-around",
        }

        align_map = {
            "start": "items-start",
            "end": "items-end",
            "center": "items-center",
            "stretch": "items-stretch",
        }

        classes = [
            "flex",
            "flex-col",
            justify_map.get(self.justify, "justify-start"),
            align_map.get(self.align, "items-start"),
            f"gap-{self.gap}",
            f"p-{self.padding}",
            f"m-{self.margin}",
        ]

        children_html = "\n".join(child.to_html() for child in self.children)
        return f"""
        <div id="{self.id}" class="{' '.join(classes)}">
            {children_html}
        </div>
        """


@dataclass
class Grid(Container):
    """网格布局"""

    cols: int = 2  # 列数
    rows: Optional[int] = None  # 行数（可选）
    gap: str = "4"  # 间距

    def __init__(
        self,
        cols: int = 2,
        rows: Optional[int] = None,
        gap: str = "4",
        id: Optional[str] = None,
        padding: str = "0",
        margin: str = "0",
        **kwargs,
    ):
        self.cols = cols
        self.rows = rows
        self.gap = gap
        super().__init__(id=id, padding=padding, margin=margin, **kwargs)

    def to_html(self) -> str:
        if not self.children:
            return ""

        classes = [
            "grid",
            f"grid-cols-{self.cols}",
            f"gap-{self.gap}",
            f"p-{self.padding}",
            f"m-{self.margin}",
        ]

        if self.rows:
            classes.append(f"grid-rows-{self.rows}")

        children_html = "\n".join(child.to_html() for child in self.children)
        return f"""
        <div id="{self.id}" class="{' '.join(classes)}">
            {children_html}
        </div>
        """
