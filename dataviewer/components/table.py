from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from .base import Component
from ..renderers import CellRendererRegistry, DefaultRenderer, CellImageRenderer

_INIT_CELL_RENDERER = False
if not _INIT_CELL_RENDERER:
    CellRendererRegistry.register(CellImageRenderer())
    CellRendererRegistry.register(DefaultRenderer())
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

        self.column_widths = column_widths or {}
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
        return is_image, is_image_array

    def _infer_columns(self) -> None:
        """从数据中推断列信息"""
        if not self.data:
            self.columns = []
            return

        # 使用列表推导式优化性能
        all_keys = sorted({key for row in self.data for key in row})
        self.columns = [
            {"key": key, "title": key.replace("_", " ").title()} for key in all_keys
        ]

        if self.data:
            first_row = self.data[0]
            for key in all_keys:
                if key not in self.column_widths:
                    value = first_row.get(key)
                    is_image, is_image_array = self._get_column_type(value)
                    if not (is_image or is_image_array):
                        self.column_widths[
                            key
                        ] = f"clamp({self.min_column_width}px, auto, {self.max_column_width}px)"

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

    def _render_cell(self, value: Any, is_image: bool, is_image_array: bool) -> str:
        """渲染单元格内容"""
        if is_image_array:
            # 预先计算图片网格容器样式
            container_style = 'class="w-[120px] h-[120px] flex items-center justify-center overflow-hidden"'
            image_grid = []
            for img_value in value:
                rendered_img = CellRendererRegistry.render(img_value)
                if rendered_img and "<img" in rendered_img:
                    image_grid.append(f"<div {container_style}>{rendered_img}</div>")

            return '<div class="grid grid-cols-5 gap-1 w-[620px]">%s</div>' % "".join(
                image_grid
            )

        rendered = CellRendererRegistry.render(value)
        return rendered if rendered is not None else str(value)

    def get_cell_style(self, is_image: bool, is_image_array: bool) -> str:
        if is_image_array:
            return 'style="max-width: 1200px;"'
        elif is_image:
            return 'style="max-width: 600px;"'
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
        column_types = {}  # 预先计算列类型

        # 预先获取第一行数据
        first_row = self.data[0]
        for col in self.columns:
            key = col["key"]
            value = first_row.get(key)
            column_types[key] = self._get_column_type(value)

            is_image, is_image_array = column_types[key]

            header_classes = [*self._HEADER_BASE_CLASSES, *base_cell_classes]

            width_style = self.get_cell_style(is_image, is_image_array)

            header_cells.append(
                '<th scope="col" class="%s" %s>%s</th>'
                % (
                    " ".join(header_classes),
                    width_style,
                    col.get("title", key),
                )
            )

        # 构建表格内容
        rows_html = []
        for i, row in enumerate(display_data):
            cells = []
            for col in self.columns:
                key = col["key"]
                value = row.get(key, "")

                is_image, is_image_array = column_types[key]
                rendered_value = self._render_cell(value, is_image, is_image_array)

                cell_classes = base_cell_classes.copy()
                if self.striped and i % 2 == 1:
                    cell_classes.append("bg-gray-50")
                if self.hoverable:
                    cell_classes.append("hover:bg-gray-100")

                if not (is_image or is_image_array):
                    cell_classes.extend(
                        ["whitespace-normal", "break-words", "overflow-hidden"]
                    )

                width_style = self.get_cell_style(is_image, is_image_array)

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
