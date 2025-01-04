import base64
import os
import re
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from ..core.page import Page

_IMAGE_PREVIEW_INITIALIZED = False


@dataclass
class CellImageRenderer:
    """单元格图片渲染器"""

    patterns: List[re.Pattern] = field(default_factory=list)
    width: str = "200px"  # 图片宽度
    height: Optional[str] = None  # 图片高度（可选）
    lazy_load: bool = True  # 是否启用懒加载
    level: int = 1

    def __repr__(self) -> str:
        return "CellImageRenderer()"

    def __post_init__(self):
        """初始化时添加必要的样式和脚本到页面"""
        if "image_preview" not in Page._init_flags:
            Page._init_flags.add("image_preview")

            Page._additional_head_content = (
                Page._additional_head_content
                + """
            <style>
                .image-preview-modal {
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(255,255,255,0.85);
                    cursor: pointer;
                }
                .image-preview-modal img {
                    margin: auto;
                    display: block;
                    max-width: 90%;
                    max-height: 90%;
                    position: relative;
                    top: 50%;
                    transform: translateY(-50%) !important;
                    cursor: default !important;
                    transition: none !important;
                }
                .image-preview-modal img:hover {
                    transform: translateY(-50%) !important;
                }
                .image-preview-modal.active {
                    display: block;
                }
                .image-list {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    padding: 4px;
                }
                .image-list img {
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                .image-list img:hover {
                    transform: scale(1.05);
                }
                .cell-image {
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                .cell-image:hover {
                    transform: scale(1.05);
                }
            </style>
            <div id="imagePreviewModal" class="image-preview-modal">
                <img id="previewImage" src="" alt="预览图片" />
            </div>
            <script>
                function openImagePreview(img) {
                    const modal = document.getElementById('imagePreviewModal');
                    const previewImg = document.getElementById('previewImage');
                    
                    window.openImagePreview = function(img) {
                        previewImg.src = img.src;
                        modal.classList.add('active');
                    };
                    
                    modal.onclick = function() {
                        modal.classList.remove('active');
                    };
                };
            </script>
            """
            )

        self.patterns.extend(
            [
                re.compile(r"^img://.*"),
                re.compile(r".*\.(?:png|jpg|jpeg|gif|webp|svg)$"),
            ]
        )
        self.base64_patterns = [re.compile(r"^/9j")]

    def has_valid_base64_pattern(self, path: str) -> bool:
        return isinstance(path, str) and any(
            pattern.match(path) for pattern in self.base64_patterns
        )

    def has_valid_pattern(self, path: str) -> bool:
        return isinstance(path, str) and any(
            pattern.match(path) for pattern in self.patterns
        )

    def can_render(self, value: Any) -> bool:
        """检查是否可以渲染该值"""
        if isinstance(value, str):
            return self.has_valid_pattern(value) or self.has_valid_base64_pattern(value)
        elif isinstance(value, list):
            return bool(value) and all(
                self.has_valid_pattern(item) or self.has_valid_base64_pattern(item)
                for item in value
            )
        return False

    def render(self, value: Union[str, List[str]]) -> str:
        """渲染图片或图片列表"""

        def render_single_image(img_path: str) -> str:
            # 添加懒加载属性
            loading_attr = ' loading="lazy"' if self.lazy_load else ""
            if self.has_valid_base64_pattern(img_path):
                img_path = f"data:image/jpeg;base64,{img_path}"

            return f"""
            <img src="{img_path}" 
                 style="width: {self.width};"
                 class="cell-image"
                 onclick="openImagePreview(this)"{loading_attr}
                 alt="图片" />
            """

        if isinstance(value, list):
            images_html = [render_single_image(img_path) for img_path in value]
            n_images = len(images_html)
            if n_images < 5:
                return f'<div style="display: grid; grid-template-columns: repeat({n_images}, 1fr); gap: 10px;">{"".join(images_html)}</div>'
            else:
                return f'<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;">{"".join(images_html)}</div>'
        else:
            return render_single_image(value)
