from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Optional


class ComponentContext:
    """组件上下文管理器，用于管理组件的自动添加"""

    _context_stacks: Dict[int, List["Component"]] = {}  # 每个线程一个上下文栈

    @classmethod
    def _get_stack(cls) -> List["Component"]:
        """获取当前线程的上下文栈"""
        import threading

        thread_id = threading.get_ident()
        if thread_id not in cls._context_stacks:
            cls._context_stacks[thread_id] = []
        return cls._context_stacks[thread_id]

    @classmethod
    def push(cls, component: "Component") -> None:
        """将组件添加到上下文栈"""
        cls._get_stack().append(component)

    @classmethod
    def pop(cls) -> Optional["Component"]:
        """从上下文栈移除并返回最后一个组件"""
        stack = cls._get_stack()
        if stack:
            return stack.pop()
        return None

    @classmethod
    def current(cls) -> Optional["Component"]:
        """获取当前上下文中的组件"""
        stack = cls._get_stack()
        return stack[-1] if stack else None

    @classmethod
    def clear(cls) -> None:
        """清空上下文栈"""
        import threading

        thread_id = threading.get_ident()
        if thread_id in cls._context_stacks:
            cls._context_stacks[thread_id].clear()


class Component:
    """组件基类"""

    _id_counter: ClassVar[Dict[str, int]] = defaultdict(int)  # 每个组件类型的计数器

    def __init__(self, id: Optional[str] = None, **kwargs):
        """初始化组件
        
        Args:
            id: 可选的组件ID，如果不提供则自动生成
            **kwargs: 其他参数，传递给子类
        """
        # 设置组件ID
        if id is not None:
            self._id = id
        else:
            # 自动生成ID
            cls_name = self.__class__.__name__.lower()
            Component._id_counter[cls_name] += 1
            self._id = f"{cls_name}-{Component._id_counter[cls_name]}"

        # 验证ID
        if not self._id:
            raise ValueError("组件ID不能为空")
        if not self._id.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"组件ID '{self._id}' 只能包含字母、数字、下划线和连字符")

        # 处理其他属性
        for k, v in kwargs.items():
            setattr(self, k, v)

        # 调用子类的初始化后处理
        self.__post_init__()

        # 自动添加到当前上下文
        current = ComponentContext.current()
        if current is not None and hasattr(current, "add"):
            current.add(self)

    def __post_init__(self):
        """初始化后的处理，子类可以重写此方法"""
        pass

    @property
    def id(self) -> str:
        """获取组件ID"""
        return self._id

    def to_html(self) -> str:
        """将组件渲染为HTML"""
        raise NotImplementedError("Subclass must implement to_html method")

    def __enter__(self):
        """进入上下文"""
        # 保存当前上下文
        self._prev_context = ComponentContext.current()
        ComponentContext.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        # 恢复之前的上下文
        current = ComponentContext.pop()
        if current is not self:
            raise RuntimeError("组件上下文管理出错")
        if self._prev_context is not None:
            ComponentContext.push(self._prev_context)


@dataclass
class LabeledComponent(Component):
    """带标签的组件基类"""

    label: Optional[str] = None

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
