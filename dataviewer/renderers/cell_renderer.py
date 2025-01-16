import html
from dataclasses import dataclass
from typing import Any


@dataclass
class DefaultRenderer:
    level: int = -1

    def __repr__(self) -> str:
        return "DefaultRenderer()"

    def can_render(self, value: Any) -> bool:
        return True

    def render(self, value: Any) -> str:
        if value is None:
            return ""
        elif isinstance(value, bool):
            return "Yes" if value else "No"
        elif isinstance(value, (list, dict)):
            import json

            formatted = json.dumps(value, ensure_ascii=False, indent=2)
            return html.escape(formatted)
        elif isinstance(value, str):
            return html.escape(value)
        return html.escape(str(value))
