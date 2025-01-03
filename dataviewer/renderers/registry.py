from typing import List, Optional, Any
from .cell_image_renderer import CellImageRenderer
from dataviewer import logger


class CellRendererRegistry:
    """Cell Renderer Registry"""

    _renderers: List[CellImageRenderer] = []

    @classmethod
    def register(cls, renderer: CellImageRenderer) -> None:
        """Register Renderer"""
        logger.info(f"Registering Renderer: {renderer}")
        cls._renderers.append(renderer)

    @classmethod
    def unregister(cls, renderer: CellImageRenderer) -> None:
        """Unregister Renderer"""
        logger.info(f"Unregistering Renderer: {renderer}")
        if renderer in cls._renderers:
            cls._renderers.remove(renderer)

    @classmethod
    def clear(cls) -> None:
        """Clear all Renderers"""
        logger.info("Clearing all Renderers")
        cls._renderers.clear()

    @classmethod
    def render(cls, value: Any) -> Optional[str]:
        """Render value using registered renderer"""
        for renderer in cls._renderers:
            if renderer.can_render(value):
                return renderer.render(value)
        return None
