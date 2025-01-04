from dataclasses import dataclass, field
from typing import Any, List, Optional
import re


@dataclass
class CellVideoRenderer:
    patterns: List[re.Pattern] = field(default_factory=list)
    width: int = 400
    height: Optional[int] = None
    lazy_load: bool = True
    level: int = 2

    def __repr__(self) -> str:
        return "CellVideoRenderer()"

    def __post_init__(self):
        self.patterns.extend([re.compile(r".*\.(?:mp4|avi|mov|mkv|webm)$")])

    def can_render(self, value: Any) -> bool:
        return isinstance(value, str) and any(
            pattern.match(value) for pattern in self.patterns
        )

    def render(self, value: Any) -> str:
        # 生成HTML代码来播放视频
        width = f' width="{self.width}px"' if self.width else ""
        height = f' height="{self.height}px"' if self.height else ""

        return (
            f'<video{width}{height} controls loading="lazy">'
            f'<source src="{value}" type="video/mp4"></video>'
        )
