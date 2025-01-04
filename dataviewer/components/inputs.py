from dataclasses import dataclass
from typing import Optional

from .base import LabeledComponent


@dataclass
class TextInput(LabeledComponent):
    """文本输入框组件"""

    placeholder: str = ""
    value: str = ""

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)

    def to_html(self) -> str:
        label_html = (
            f'<label for="{self.id}" class="block text-sm font-medium text-gray-700">{self.label}</label>'
            if self.label
            else ""
        )
        return f"""
        <div class="mt-1">
            {label_html}
            <input
                type="text"
                id="{self.id}"
                name="{self.id}"
                value="{self.value}"
                placeholder="{self.placeholder}"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
        </div>
        """


@dataclass
class Button(LabeledComponent):
    """按钮组件"""

    text: str = "Button"
    onclick: str = ""

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)

    def to_html(self) -> str:
        onclick_attr = f'onclick="{self.onclick}"' if self.onclick else ""
        return f"""
        <button
            type="button"
            id="{self.id}"
            {onclick_attr}
            class="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
            {self.text}
        </button>
        """
