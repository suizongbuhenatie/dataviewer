from typing import Any, Callable, Dict, Optional, Union, List
import html
from abc import ABC, abstractmethod
from .cell_image_renderer import CellImageRenderer


class CellRenderer(ABC):
    """单元格渲染器基类"""

    @abstractmethod
    def can_render(self, value: Any) -> bool:
        """判断是否可以渲染该值"""
        pass

    @abstractmethod
    def render(self, value: Any) -> str:
        """将值渲染为HTML"""
        pass


class DefaultRenderer(CellRenderer):
    """默认渲染器"""

    def can_render(self, value: Any) -> bool:
        return True

    def render(self, value: Any) -> str:
        if value is None:
            return ""
        elif isinstance(value, bool):
            return "是" if value else "否"
        elif isinstance(value, (list, dict)):
            import json

            formatted = json.dumps(value, ensure_ascii=False, indent=2)
            return html.escape(formatted)
        elif isinstance(value, str):
            return html.escape(value)
        return html.escape(str(value))
