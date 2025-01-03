from typing import Any, Callable, Dict, Optional, Union, List
import html
from abc import ABC, abstractmethod

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

class CellRendererRegistry:
    """单元格渲染器注册表"""
    _renderers: List[CellRenderer] = []
    
    @classmethod
    def register(cls, renderer: CellRenderer) -> None:
        """注册渲染器"""
        cls._renderers.append(renderer)
    
    @classmethod
    def clear(cls) -> None:
        """清空所有渲染器"""
        cls._renderers.clear()
    
    @classmethod
    def get_renderers(cls) -> List[CellRenderer]:
        """获取所有注册的渲染器"""
        return cls._renderers

# 使用示例：
"""
# 注册图片渲染器
CellRendererRegistry.register(ImageRenderer(prefix="img://", width="100px"))

# 在表格中使用
data = [
    {
        "name": "产品1",
        "image": "img://https://example.com/image1.jpg",
        "description": "这是产品1的描述"
    },
    {
        "name": "产品2",
        "image": "img://https://example.com/image2.jpg",
        "description": "这是产品2的描述"
    }
]

# Table组件会自动使用CellRendererRegistry来渲染单元格
table = Table(id="products", data=data)
""" 