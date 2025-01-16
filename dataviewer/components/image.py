from dataclasses import dataclass
from typing import Optional

from ..core.page import Page
from .base import Component


"""Image Component"""

@dataclass
class Image(Component):
    src: str  # Image path
    width: Optional[int] = None  # Width (pixels)
    height: Optional[int] = None  # Height (pixels)
    alt: str = ""  # Alternative text
    css_class: str = ""  # CSS class name
    lazy_load: bool = True  # Enable lazy loading

    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)

    def __post_init__(self):
        """Initializes necessary styles and scripts on the page"""
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
                <img id="previewImage" src="" alt="Preview Image" />
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

    def to_html(self) -> str:
        # 处理样式
        style = []
        if self.width:
            style.append(f"width: {self.width}px")
        if self.height:
            style.append(f"height: {self.height}px")

        style_attr = f' style="{"; ".join(style)}"' if style else ""

        # 处理类名
        classes = []
        if self.css_class:
            classes.extend(self.css_class.split())
        classes.append("zoomable-image")
        class_attr = f' class="{" ".join(classes)}"'

        # 添加懒加载属性
        loading_attr = ' loading="lazy"' if self.lazy_load else ""

        return f'<img src="{self.src}" class="cell-image" onclick="openImagePreview(this)" alt="{self.alt}"{style_attr}{class_attr}{loading_attr}>'
