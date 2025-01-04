import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..renderers import (
    CellImageRenderer,
    CellRendererRegistry,
    CellVideoRenderer,
    DefaultRenderer,
)
from .base import Component

_INIT_CELL_RENDERER = False
if not _INIT_CELL_RENDERER:
    CellRendererRegistry.register(CellImageRenderer())
    CellRendererRegistry.register(DefaultRenderer())
    CellRendererRegistry.register(CellVideoRenderer())

    CellRendererRegistry.show_renderers()
    _INIT_CELL_RENDERER = True


@dataclass
class Table(Component):
    """表格组件"""

    data: List[Dict[str, Any]]
    columns: Optional[List[Dict[str, str]]] = None
    page_size: Optional[int] = None
    current_page: int = 1
    hoverable: bool = True
    striped: bool = True
    bordered: bool = True
    compact: bool = False
    sort_by: Optional[str] = None
    sort_desc: bool = False
    min_column_width: int = 300
    max_column_width: int = 300
    resizable: bool = False
    column_widths: Dict[str, str] = field(default_factory=dict)

    # 预计算样式
    _TABLE_BASE_CLASSES = ["table-auto", "divide-y", "divide-gray-200", "bg-white"]
    _CELL_BASE_CLASSES = ["px-4", "py-3"]
    _CELL_COMPACT_CLASSES = ["px-2", "py-2"]
    _HEADER_BASE_CLASSES = [
        "text-left",
        "text-xs",
        "font-medium",
        "text-gray-500",
        "uppercase",
        "tracking-wider",
        "whitespace-normal",
        "break-words",
    ]

    def __init__(
        self,
        data: List[Dict[str, Any]],
        columns: Optional[List[Dict[str, str]]] = None,
        page_size: Optional[int] = None,
        current_page: int = 1,
        hoverable: bool = True,
        striped: bool = True,
        bordered: bool = True,
        compact: bool = False,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        min_column_width: Optional[int] = None,
        max_column_width: Optional[int] = None,
        resizable: bool = False,
        column_widths: Optional[Dict[str, str]] = None,
        id: Optional[str] = None,
    ):
        self.data = data
        self.columns = columns
        self.page_size = page_size
        self.current_page = current_page
        self.hoverable = hoverable
        self.striped = striped
        self.bordered = bordered
        self.compact = compact

        super().__init__(id=id)

        if self.columns is None:
            self._infer_columns()

    def _get_column_type(self, value: Any) -> Tuple[bool, bool]:
        """判断列类型"""
        rendered = CellRendererRegistry.render(value)
        is_image = rendered and "<img" in rendered
        is_image_array = isinstance(value, list) and any(
            isinstance(item, str)
            and CellRendererRegistry.render(item)
            and "<img" in CellRendererRegistry.render(item)
            for item in value
        )
        if is_image:
            return "image"
        elif is_image_array:
            return "image_array"
        else:
            return "default"

    def _infer_columns(self) -> None:
        """从数据中推断列信息"""
        if not self.data:
            self.columns = []
            return

        # 使用列表推导式优化性能
        all_keys = []
        for row in self.data:
            for key in row:
                if key not in all_keys:
                    all_keys.append(key)

        self.columns = [
            {"key": key, "title": key.replace("_", " ").title()} for key in all_keys
        ]

    def _get_display_data(self) -> List[Dict[str, Any]]:
        """获取要显示的数据"""
        if not self.data:
            return []

        if self.sort_by:
            data = sorted(
                self.data, key=lambda x: x.get(self.sort_by, ""), reverse=self.sort_desc
            )
        else:
            data = self.data

        if self.page_size:
            start = (self.current_page - 1) * self.page_size
            return data[start : start + self.page_size]

        return data

    def _render_cell(self, value: Any, col_type: str) -> str:
        """渲染单元格内容"""
        if col_type in ["image", "image_array"]:
            return CellRendererRegistry.render(value)

        if isinstance(value, dict):
            # 优化一下json的显示
            try:
                value = json.dumps(value, indent=4, ensure_ascii=False)
                value = f"<pre>{value}</pre>"
                return value
            except Exception as e:
                pass

        rendered = CellRendererRegistry.render(value)
        return rendered if rendered is not None else str(value)

    def get_cell_style(self, col_type: str) -> str:
        if col_type == "image_array":
            return 'style="max-width: 1200px;"'
        elif col_type == "image":
            return 'style="max-width: 1200px;"'
        else:
            return 'style="max-width: 600px;min-width: 120px;"'

    def to_html(self) -> str:
        if not self.data:
            return ""

        display_data = self._get_display_data()

        # 构建表格类名
        table_classes = self._TABLE_BASE_CLASSES.copy()
        if self.bordered:
            table_classes.append("border")

        # 获取基础单元格类名
        base_cell_classes = (
            self._CELL_COMPACT_CLASSES if self.compact else self._CELL_BASE_CLASSES
        )

        # 构建表格头部
        header_cells = []

        # 预先获取第一行数据
        first_row = self.data[0]
        for col in self.columns:
            key = col["key"]
            value = first_row.get(key)

            header_classes = [*self._HEADER_BASE_CLASSES, *base_cell_classes]

            col_type = self._get_column_type(value)
            style = self.get_cell_style(col_type)

            header_cells.append(
                '<th scope="col" class="%s" %s>%s</th>'
                % (" ".join(header_classes), style, col.get("title", key))
            )

        # 构建表格内容
        rows_html = []
        for i, row in enumerate(display_data):
            cells = []
            for col in self.columns:
                key = col["key"]
                value = row.get(key, "")

                col_type = self._get_column_type(value)
                rendered_value = self._render_cell(value, col_type)

                cell_classes = base_cell_classes.copy()
                if self.striped and i % 2 == 1:
                    cell_classes.append("bg-gray-50")
                if self.hoverable:
                    cell_classes.append("hover:bg-gray-100")

                width_style = self.get_cell_style(col_type)

                cells.append(
                    '<td class="%s" %s>%s</td>'
                    % (" ".join(cell_classes), width_style, rendered_value)
                )

            rows_html.append("<tr>%s</tr>" % "".join(cells))

        return """
        <div class="relative rounded-lg shadow">
            <div class="overflow-x-auto rounded-lg">
                <table id="%s" class="%s">
                    <thead class="sticky top-0 z-50 bg-gray-50 shadow-sm backdrop-blur-sm bg-opacity-75">
                        <tr>%s</tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 bg-white">%s</tbody>
                </table>
            </div>
        </div>""" % (
            self.id,
            " ".join(table_classes),
            "".join(header_cells),
            "".join(rows_html),
        )
