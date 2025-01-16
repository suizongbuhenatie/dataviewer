from dataclasses import dataclass, field
from typing import List, Optional

from .base import Component


"""Base container class for layout"""

@dataclass
class Container(Component):
    children: Optional[List[Component]] = None  # List of child components
    gap: str = "4"  # Gap between items
    padding: str = "0"  # Padding
    margin: str = "0"  # Margin

    def __init__(self, id: Optional[str] = None, gap: str = "4", padding: str = "0", margin: str = "0", **kwargs):
        super().__init__(id=id, **kwargs)
        self.gap = gap
        self.padding = padding
        self.margin = margin
        if self.children is None:
            self.children = []

    def add(self, component: Component) -> None:
        """Add child component"""
        if component not in self.children:  # Avoid duplicate additions
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


"""Horizontal flex layout"""

@dataclass
class FlexRow(Container):
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


"""Vertical flex layout"""

@dataclass
class FlexColumn(Container):
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


"""Grid layout"""

@dataclass
class Grid(Container):
    cols: int = 2  # Number of columns
    rows: Optional[int] = None  # Number of rows (optional)
    gap: str = "4"  # gap between items

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
