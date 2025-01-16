import warnings
from typing import Dict, Optional


class ComponentRegistry:
    """Component registry for managing and validating component IDs"""

    _instance = None
    _components: Dict[str, "Component"] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComponentRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, component: "Component") -> None:
        """Register a component"""
        existing = self._components.get(component.id)
        if existing is not None:
            raise ValueError(
                f"ID '{component.id}' is already in use:\n"
                f"  - Current component: {component.__class__.__name__}\n"
                f"  - Existing component: {existing.__class__.__name__}\n"
                f"Please ensure each component has a unique ID"
            )
        self._components[component.id] = component

    def unregister(self, component: "Component") -> None:
        """Unregister a component"""
        if component.id in self._components:
            del self._components[component.id]

    def clear(self) -> None:
        """Clear the registry"""
        self._components.clear()

    def get(self, id: str) -> Optional["Component"]:
        """Get component by ID"""
        return self._components.get(id)
