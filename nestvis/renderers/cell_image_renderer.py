import base64
import os
from typing import List, Optional, Any, Union
from dataclasses import dataclass
from ..core.page import Page

_IMAGE_PREVIEW_INITIALIZED = False

@dataclass
class CellImageRenderer:
    """单元格图片渲染器"""
    patterns: List[str]  # 匹配的文件扩展名
    width: str = "100px"  # 图片宽度
    height: Optional[str] = None  # 图片高度（可选）
    lazy_load: bool = True  # 是否启用懒加载
    
    def __post_init__(self):
        """初始化时添加必要的样式和脚本到页面"""
        global _IMAGE_PREVIEW_INITIALIZED
        if not _IMAGE_PREVIEW_INITIALIZED:
            _IMAGE_PREVIEW_INITIALIZED = True
            Page._additional_head_content = Page._additional_head_content + """
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
                document.addEventListener('DOMContentLoaded', function() {
                    const modal = document.getElementById('imagePreviewModal');
                    const previewImg = document.getElementById('previewImage');
                    
                    window.openImagePreview = function(img) {
                        previewImg.src = img.src;
                        modal.classList.add('active');
                    };
                    
                    modal.onclick = function() {
                        modal.classList.remove('active');
                    };
                });
            </script>
            """
    
    @staticmethod
    def encode_image(image_path: str) -> str:
        """将图片编码为base64字符串"""
        if any(proto in image_path.lower() for proto in ['http://', 'https://', 'data:']):
            return image_path
            
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
            
        # 返回相对路径
        return image_path
    
    def can_render(self, value: Any) -> bool:
        """检查是否可以渲染该值"""
        def has_valid_pattern(path: str) -> bool:
            return isinstance(path, str) and any(pattern.lower() in path.lower() for pattern in self.patterns)
            
        if isinstance(value, str):
            return has_valid_pattern(value)
        elif isinstance(value, list):
            return bool(value) and all(has_valid_pattern(item) for item in value)
        return False
    
    def render(self, value: Union[str, List[str]]) -> str:
        """渲染图片或图片列表"""
        def render_single_image(img_path: str) -> str:
            # 添加懒加载属性
            loading_attr = ' loading="lazy"' if self.lazy_load else ''
                
            return f"""
            <img src="{img_path}" 
                 style="width: {self.width};"
                 class="cell-image"
                 onclick="openImagePreview(this)"{loading_attr}
                 alt="图片" />
            """
        
        if isinstance(value, list):
            images_html = [render_single_image(img_path) for img_path in value]
            # 使用额外的样式包装器来控制每行显示的数量
            return " ".join(images_html)
        else:
            return render_single_image(value) 