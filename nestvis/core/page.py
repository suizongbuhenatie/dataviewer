from typing import List
from ..components.base import Component, ComponentContext

class Page:
    """页面类,用于组织渲染界面"""
    _additional_head_content: str = ""  # 用于存储额外的头部内容
    
    def __init__(self, title: str, padding: str = "0"):
        self.title = title
        self.padding = padding
        self.components: List[Component] = []
        
    def add(self, component: Component) -> None:
        """添加组件到页面"""
        if component not in self.components:  # 避免重复添加
            self.components.append(component)
        
    def __enter__(self):
        """支持with语句"""
        ComponentContext.clear()  # 清空组件上下文
        ComponentContext.push(self)  # 将页面添加到上下文
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """with语句退出时的处理"""
        current = ComponentContext.pop()
        if current is not self:  # 如果当前上下文不是本页面，说明上下文栈出错了
            ComponentContext.clear()  # 清空所有上下文
            raise RuntimeError("页面上下文管理出错")

    def save(self, filename: str) -> None:
        """保存页面到HTML文件"""
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.render())

    def render(self) -> str:
        """生成页面的HTML内容"""
        components_html = "\n".join(component.to_html() for component in self.components if component)
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com/3.4.16"></script>
    <style>
        body {{
            width: 100%;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            width: 100%;
            margin: 0 auto;
        }}
    </style>
    {self._additional_head_content}
</head>
<body>
    <div class="p-{self.padding}">
        {components_html}
    </div>
</body>
</html>"""