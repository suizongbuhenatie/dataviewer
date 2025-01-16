# DataViewer

<div align="center">
  <img src="imgs/banner.jpg" alt="DataViewer Banner" width="100%" style="border-radius: 10px;"/>
  <p>
    <a href="https://github.com/suizongbuhenatie/dataviewer/stargazers">
      <img alt="GitHub stars" src="https://img.shields.io/github/stars/suizongbuhenatie/dataviewer">
    </a>
    <a href="https://github.com/suizongbuhenatie/dataviewer/network">
      <img alt="GitHub forks" src="https://img.shields.io/github/forks/suizongbuhenatie/dataviewer">
    </a>
    <a href="https://github.com/suizongbuhenatie/dataviewer/issues">
      <img alt="GitHub issues" src="https://img.shields.io/github/issues/suizongbuhenatie/dataviewer">
    </a>
    <a href="https://github.com/suizongbuhenatie/dataviewer/blob/main/LICENSE">
      <img alt="License" src="https://img.shields.io/github/license/suizongbuhenatie/dataviewer">
    </a>
  </p>
</div>

## Overview

DataViewer is a modern, high-performance Python library designed for interactive data visualization and presentation. Built with a focus on developer experience and flexibility, it provides a powerful component-based architecture that makes it easy to create sophisticated data visualizations and dashboards.

<div align="center">
    <div style="display: flex; justify-content: center; align-items: center;gap: 10px;">
        <img src="imgs/screenshot.jpg" alt="DataViewer Example" width="50%" style="border-radius: 10px;"/>
        <img src="imgs/screenshot2.jpg" alt="DataViewer Example" width="50%" style="border-radius: 10px;"/>
    </div>
</div>

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Quick Install
```bash
pip install git+https://github.com/suizongbuhenatie/dataviewer.git
```

### Development Install
```bash
git clone https://github.com/suizongbuhenatie/dataviewer.git
cd dataviewer
pip install -e .
```

## Quick Start

Run the demo examples to see DataViewer in action:
```bash
python examples/run_demos.py  # Results will be in the output directory
```

## Core Components

### Layout Components
- `FlexRow`: Horizontal flexible container with customizable alignment and spacing
- `FlexColumn`: Vertical flexible container with adjustable properties
- `Grid`: Advanced grid layout system for complex arrangements

### Display Components
- `Table`: Feature-rich table component with pagination, sorting, and customizable column widths
- `JsonView`: Interactive JSON visualization with collapsible nodes and theme support
- `Image`: Optimized image component with lazy loading and zoom capabilities
- `Header`: Hierarchical header component with alignment options
- `Tag`: Versatile tag component with various styles and sizes
- `Video`: Enhanced video component with customizable controls and styling

## Usage Examples

### Table Component
```python
from dataviewer import Page, Table

data = [
    {"id": 1, "name": "John Doe", "age": 25},
    {"id": 2, "name": "Jane Smith", "age": 30}
]

with Page("Table Example") as page:
    Table(data=data)
    page.save("table_demo.html")
```

### JSON Viewer Component
```python
from dataviewer import Page, JsonView, FlexColumn

data = {
    "name": "John Doe",
    "age": 30,
    "hobbies": ["reading", "swimming"],
    "address": {
        "city": "New York",
        "street": "5th Avenue"
    }
}

with Page("JSON Example") as page:
    with FlexColumn(padding="2"):
        JsonView(data, theme="dark")
    page.save("json_demo.html")
```

### Layout Example
```python
from dataviewer import Page, FlexRow, FlexColumn, Header, Image

with Page("Layout Example") as page:
    with FlexRow(gap="20px", justify="between"):
        with FlexColumn(padding="2"):
            Header("Left Content")
            Image("path/to/image.jpg", width=300)
        with FlexColumn(padding="2"):
            Header("Right Content")
            Image("path/to/image2.jpg", width=300)
    page.save("layout_demo.html")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
