from typing import List, Optional, Any
from .cell_image_renderer import CellImageRenderer

class CellRendererRegistry:
    """单元格渲染器注册表"""
    _renderers: List[CellImageRenderer] = []
    
    @classmethod
    def register(cls, renderer: CellImageRenderer) -> None:
        """注册渲染器"""
        cls._renderers.append(renderer)
    
    @classmethod
    def unregister(cls, renderer: CellImageRenderer) -> None:
        """注销渲染器"""
        if renderer in cls._renderers:
            cls._renderers.remove(renderer)
    
    @classmethod
    def clear(cls) -> None:
        """清空所有渲染器"""
        cls._renderers.clear()
    
    @classmethod
    def render(cls, value: Any) -> Optional[str]:
        """使用注册的渲染器渲染值"""
        for renderer in cls._renderers:
            if renderer.can_render(value):
                return renderer.render(value)
        return None 