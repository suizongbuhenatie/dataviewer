from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from functools import lru_cache
from .base import Component, LabeledComponent
from ..renderers import CellRendererRegistry

def cached_render(func):
    """渲染结果缓存装饰器"""
    cache = {}
    def wrapper(self, *args, **kwargs):
        key = (self.id, str(self.__dict__))
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        return cache[key]
    return wrapper

@dataclass
class Header(Component):
    """标题组件"""
    text: str
    level: int = 1  # h1-h6
    align: str = "left"  # left, center, right
    color: str = "gray"  # 支持的颜色: gray, blue, green, red, yellow, purple
    
    # 预计算样式映射
    _ALIGN_MAP = {
        "left": "text-left",
        "center": "text-center",
        "right": "text-right"
    }
    
    _SIZE_MAP = {
        1: "text-4xl font-bold tracking-tight mb-8",
        2: "text-3xl font-semibold tracking-tight mb-6",
        3: "text-2xl font-semibold mb-5",
        4: "text-xl font-medium mb-4",
        5: "text-lg font-medium mb-3",
        6: "text-base font-medium mb-2"
    }
    
    _COLOR_MAP = {
        "gray": "text-gray-900",
        "blue": "text-blue-600",
        "green": "text-green-600",
        "red": "text-red-600",
        "yellow": "text-yellow-600",
        "purple": "text-purple-600"
    }
    
    def __init__(self, text: str, level: int = 1, align: str = "left", color: str = "gray", id: Optional[str] = None):
        self.text = text
        self.level = level
        self.align = align
        self.color = color
        super().__init__(id=id)
    
    def __post_init__(self):
        if not 1 <= self.level <= 6:
            raise ValueError("标题级别必须在1-6之间")
        if self.color not in self._COLOR_MAP:
            raise ValueError(f"不支持的颜色: {self.color}，支持的颜色有: {', '.join(self._COLOR_MAP.keys())}")
    
    @cached_render
    def to_html(self) -> str:
        classes = [
            self._ALIGN_MAP.get(self.align, "text-left"),
            self._SIZE_MAP.get(self.level, "text-base"),
            self._COLOR_MAP.get(self.color, "text-gray-900"),
            "font-sans"
        ]
        
        class_str = ' '.join(classes)
        return '<h%d id="%s" class="%s">%s</h%d>' % (
            self.level, self.id, class_str, self.text, self.level
        )

@dataclass
class Tag(Component):
    """标签组件"""
    text: str
    color: str = "blue"
    size: str = "md"
    
    # 预计算样式映射
    _COLOR_MAP = {
        "blue": "bg-blue-100 text-blue-800",
        "red": "bg-red-100 text-red-800",
        "green": "bg-green-100 text-green-800",
        "yellow": "bg-yellow-100 text-yellow-800",
        "gray": "bg-gray-100 text-gray-800"
    }
    
    _SIZE_MAP = {
        "sm": "text-xs px-2 py-1",
        "md": "text-sm px-3 py-1.5",
        "lg": "text-base px-4 py-2"
    }
    
    _BASE_CLASSES = [
        "inline-flex",
        "items-center",
        "rounded-full",
        "font-medium"
    ]
    
    def __init__(self, text: str, color: str = "blue", size: str = "md", id: Optional[str] = None):
        self.text = text
        self.color = color
        self.size = size
        super().__init__(id=id)
    
    @cached_render
    def to_html(self) -> str:
        classes = self._BASE_CLASSES + [
            self._COLOR_MAP.get(self.color, "bg-gray-100 text-gray-800"),
            self._SIZE_MAP.get(self.size, "text-sm px-3 py-1.5")
        ]
        
        class_str = ' '.join(classes)
        return '<span id="%s" class="%s">%s</span>' % (
            self.id, class_str, self.text
        ) 