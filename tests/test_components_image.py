import pytest
from pathlib import Path
from dataviewer.components import Image
from dataviewer.renderers import CellImageRenderer


def test_image_basic(tmp_path):
    """测试图片基本功能"""
    # 创建测试图片
    image_path = tmp_path / "test.png"
    with open(image_path, "wb") as f:
        f.write(b"fake image data")

    image = Image(src=str(image_path))
    assert image.src == str(image_path)
    assert image.width is None
    assert image.height is None
    assert image.alt == ""
    assert image.css_class == ""


def test_image_with_params(tmp_path):
    """测试带参数的图片"""
    # 创建测试图片
    image_path = tmp_path / "test.png"
    with open(image_path, "wb") as f:
        f.write(b"fake image data")

    image = Image(
        src=str(image_path),
        width=100,
        height=200,
        alt="测试图片",
        css_class="rounded shadow",
    )
    assert image.src == str(image_path)
    assert image.width == 100
    assert image.height == 200
    assert image.alt == "测试图片"
    assert image.css_class == "rounded shadow"


def test_image_nonexistent():
    """测试不存在的图片"""
    with pytest.raises(FileNotFoundError):
        image = Image(src="nonexistent.png")
        image.to_html()


def test_image_invalid_type(tmp_path):
    """测试无效的文件类型"""
    # 创建测试文件
    file_path = tmp_path / "test.txt"
    with open(file_path, "w") as f:
        f.write("not an image")

    with pytest.raises(ValueError):
        image = Image(src=str(file_path))
        image.to_html()


def test_image_html_rendering(tmp_path):
    """测试图片HTML渲染"""
    # 创建测试图片
    image_path = tmp_path / "test.png"
    with open(image_path, "wb") as f:
        f.write(b"fake image data")

    image = Image(
        src=str(image_path), width=100, height=200, alt="测试图片", css_class="rounded"
    )

    html = image.to_html()
    assert "width: 100px" in html
    assert "height: 200px" in html
    assert 'alt="测试图片"' in html
    assert 'class="rounded zoomable-image"' in html
    assert "data:image/png;base64," in html
