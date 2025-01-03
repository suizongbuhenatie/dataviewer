from typing import Optional
from dataclasses import dataclass
from .base import Component
from ..renderers.cell_image_renderer import CellImageRenderer

@dataclass
class Image(Component):
    """图片组件"""
    src: str  # 图片路径
    width: Optional[int] = None  # 宽度（像素）
    height: Optional[int] = None  # 高度（像素）
    alt: str = ""  # 替代文本
    css_class: str = ""  # CSS类名
    lazy_load: bool = True  # 是否启用懒加载
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
    def to_html(self) -> str:
        # 处理样式
        style = []
        if self.width:
            style.append(f"width: {self.width}px")
        if self.height:
            style.append(f"height: {self.height}px")
            
        style_attr = f' style="{"; ".join(style)}"' if style else ''
        
        # 处理类名
        classes = []
        if self.css_class:
            classes.extend(self.css_class.split())
        classes.append("zoomable-image")
        class_attr = f' class="{" ".join(classes)}"'
        
        # 处理图片源
        try:
            src = CellImageRenderer.encode_image(self.src) if not any(proto in self.src.lower() for proto in ['http://', 'https://', 'data:']) else self.src
        except (FileNotFoundError, ValueError) as e:
            return f'<span class="text-red-500">Error: {str(e)}</span>'
        
        # 添加懒加载属性
        loading_attr = ' loading="lazy"' if self.lazy_load else ''
        
        return f'<img src="{src}" alt="{self.alt}"{style_attr}{class_attr}{loading_attr}>' 