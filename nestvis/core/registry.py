import warnings
from typing import Dict, Optional

class ComponentRegistry:
    """组件注册表，用于管理和验证组件ID"""
    _instance = None
    _components: Dict[str, 'Component'] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComponentRegistry, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, component: 'Component') -> None:
        """注册组件"""
        if component.id in cls._components:
            existing = cls._components[component.id]
            warnings.warn(
                f"ID '{component.id}' 已被使用:\n"
                f"  - 当前组件: {component.__class__.__name__}\n"
                f"  - 已存在组件: {existing.__class__.__name__}\n"
                f"请确保每个组件的ID都是唯一的"
            )
        cls._components[component.id] = component
    
    @classmethod
    def unregister(cls, component: 'Component') -> None:
        """取消注册组件"""
        if component.id in cls._components:
            del cls._components[component.id]
    
    @classmethod
    def clear(cls) -> None:
        """清空注册表"""
        cls._components.clear()
    
    @classmethod
    def get(cls, id: str) -> Optional['Component']:
        """获取指定ID的组件"""
        return cls._components.get(id) 