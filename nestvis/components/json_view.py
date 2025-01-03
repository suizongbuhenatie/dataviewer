from typing import Any, Optional
from .base import Component
import json

class JsonView(Component):
    """重新设计的JSON视图组件，支持层级显示和折叠功能"""
    
    # 定义主题颜色
    COLORS = {
        'dark': {
            'background': '#1e1e1e',
            'text': '#d4d4d4', 
            'border': '#333333',
            'toolbar_bg': '#252526',
            'button_bg': '#333333',
            'button_hover': '#404040',
            'toggle': '#6a9955',
            'key': '#9cdcfe',
            'string': '#ce9178',
            'number': '#b5cea8',
            'boolean': '#569cd6',
            'bracket': '#808080',
            'preview': '#808080'
        },
        'light': {
            'background': '#ffffff',
            'text': '#333333',
            'border': '#e8e8e8',
            'toolbar_bg': '#ffffff',
            'button_bg': '#f0f0f0',
            'button_hover': '#e0e0e0',
            'toggle': '#0b7a3e',
            'key': '#0451a5',
            'string': '#a31515',
            'number': '#098658',
            'boolean': '#0000ff',
            'bracket': '#666666',
            'preview': '#666666'
        }
    }
    
    def __init__(self, data: Any, id: Optional[str] = None, theme: str = "dark", default_expand_level: int = 2):
        """初始化JSON视图组件
        
        Args:
            data: 要显示的JSON数据
            id: 可选的组件ID
            theme: 主题，可选 'dark' 或 'light'
            default_expand_level: 默认展开层级
        """
        super().__init__(id=id)
        self.data = data
        self.theme = theme.lower()  # 确保主题值是小写的
        self.default_expand_level = default_expand_level
        
    def to_html(self) -> str:
        """将JSON数据渲染为HTML"""
        # 添加必要的CSS样式
        styles = """
        <style>
            .json-view {
                min-width: 600px;
                font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.6;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                position: relative;
            }
            
            .json-view.theme-dark {
                background: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333333;
            }
            
            .json-view.theme-light {
                background: #ffffff;
                color: #333333;
                border: 1px solid #e8e8e8;
            }
            
            .json-toolbar {
                position: absolute;
                top: 12px;
                right: 12px;
                display: flex;
                gap: 8px;
                z-index: 10;
                padding: 6px;
                border-radius: 6px;
            }
            
            .theme-dark .json-toolbar {
                background: #252526;
            }
            
            .theme-light .json-toolbar {
                background: #ffffff;
            }
            
            .json-toolbar button {
                padding: 4px 12px;
                border-radius: 4px;
                border: none;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s ease;
                white-space: nowrap;
            }
            
            .theme-dark .json-toolbar button {
                background: #333333;
                color: #d4d4d4;
            }
            
            .theme-dark .json-toolbar button:hover {
                background: #404040;
            }
            
            .theme-light .json-toolbar button {
                background: #f0f0f0;
                color: #333333;
            }
            
            .theme-light .json-toolbar button:hover {
                background: #e0e0e0;
            }
            
            .json-content {
                width: 100%;
                padding-top: 32px;
            }
            
            .json-item {
                margin-left: 32px;
                position: relative;
                padding: 4px 0;
            }
            
            .json-toggle {
                cursor: pointer;
                user-select: none;
                display: inline-block;
                width: 24px;
                text-align: center;
                margin-left: -24px;
                font-weight: bold;
            }
            
            .theme-dark .json-toggle {
                color: #6a9955;
            }
            
            .theme-light .json-toggle {
                color: #0b7a3e;
            }
            
            .json-collapsed .json-item {
                display: none;
            }
            
            .theme-dark .json-key {
                color: #9cdcfe;
            }
            
            .theme-light .json-key {
                color: #0451a5;
            }
            
            .json-key {
                margin-right: 4px;
            }
            
            .theme-dark .json-string {
                color: #ce9178;
            }
            
            .theme-light .json-string {
                color: #a31515;
            }
            
            .theme-dark .json-number {
                color: #b5cea8;
            }
            
            .theme-light .json-number {
                color: #098658;
            }
            
            .theme-dark .json-boolean, .theme-dark .json-null {
                color: #569cd6;
            }
            
            .theme-light .json-boolean, .theme-light .json-null {
                color: #0000ff;
            }
            
            .theme-dark .json-bracket {
                color: #808080;
            }
            
            .theme-light .json-bracket {
                color: #666666;
            }
            
            .json-bracket {
                margin: 0 4px;
            }

            .json-view > div {
                padding: 2px 0;
            }

            .json-view div {
                transition: all 0.2s ease;
            }

            .theme-dark .json-preview {
                color: #808080;
            }
            
            .theme-light .json-preview {
                color: #666666;
            }
            
            .json-preview {
                font-style: italic;
                margin-left: 4px;
                display: none;
            }

            .json-collapsed .json-preview {
                display: inline;
            }
        </style>
        """
        
        # 添加JavaScript代码
        script = f"""
        <script>
            (function() {{
                const container = document.getElementById('{self.id}');
                
                function toggleNode(node, collapsed) {{
                    if (node) {{
                        if (collapsed) {{
                            node.classList.add('json-collapsed');
                            const toggle = node.querySelector(':scope > .json-toggle');
                            if (toggle) toggle.textContent = '+';
                        }} else {{
                            node.classList.remove('json-collapsed');
                            const toggle = node.querySelector(':scope > .json-toggle');
                            if (toggle) toggle.textContent = '-';
                        }}
                    }}
                }}
                
                function getNodeLevel(node) {{
                    let level = 0;
                    let current = node;
                    while (current && !current.classList.contains('json-content')) {{
                        const parent = current.parentElement;
                        if (parent && parent.classList.contains('json-item')) {{
                            level++;
                        }}
                        current = parent;
                    }}
                    return level;
                }}
                
                function getNodes() {{
                    return Array.from(container.querySelectorAll('div')).filter(node => 
                        node.querySelector(':scope > .json-toggle')
                    );
                }}
                
                function getExpandedNodes() {{
                    return getNodes().filter(node => !node.classList.contains('json-collapsed'));
                }}
                
                function getCollapsedNodes() {{
                    return getNodes().filter(node => node.classList.contains('json-collapsed'));
                }}
                
                function getNodesAtLevel(level) {{
                    return getNodes().filter(node => getNodeLevel(node) === level);
                }}
                
                function getExpandedNodesAtLevel(level) {{
                    return getExpandedNodes().filter(node => getNodeLevel(node) === level);
                }}
                
                function getMaxExpandedLevel() {{
                    const expandedNodes = getExpandedNodes();
                    if (expandedNodes.length === 0) return 0;
                    return Math.max(...expandedNodes.map(node => getNodeLevel(node)));
                }}
                
                function expandLevel(level) {{
                    // 展开到指定层级的所有节点
                    getNodes().forEach(node => {{
                        const nodeLevel = getNodeLevel(node);
                        if (nodeLevel <= level) {{
                            toggleNode(node, false);  // 展开
                        }} else {{
                            toggleNode(node, true);   // 折叠
                        }}
                    }});
                }}
                
                // 折叠/展开单个节点
                container.addEventListener('click', function(e) {{
                    const toggle = e.target.closest('.json-toggle');
                    if (toggle) {{
                        const parent = toggle.parentElement;
                        if (parent) {{
                            toggleNode(parent, !parent.classList.contains('json-collapsed'));
                        }}
                    }}
                }});
                
                // 全部折叠按钮
                document.getElementById('{self.id}-collapse-all').addEventListener('click', function() {{
                    expandLevel(0);
                }});
                
                // 全部展开按钮
                document.getElementById('{self.id}-expand-all').addEventListener('click', function() {{
                    expandLevel(999);
                }});
                
                // 展开一级按钮
                document.getElementById('{self.id}-expand-one').addEventListener('click', function() {{
                    const currentMaxLevel = getMaxExpandedLevel();
                    expandLevel(currentMaxLevel + 1);
                }});
                
                // 折叠一级按钮
                document.getElementById('{self.id}-collapse-one').addEventListener('click', function() {{
                    const currentMaxLevel = getMaxExpandedLevel();
                    if (currentMaxLevel > 0) {{
                        expandLevel(currentMaxLevel - 1);
                    }}
                }});
                
                // 初始化默认展开层级
                expandLevel({self.default_expand_level});
            }})();
        </script>
        """
        
        def get_preview(value: Any) -> str:
            """生成预览内容"""
            if isinstance(value, dict):
                count = len(value)
                return f"{{ {count} 个字段 }}"
            elif isinstance(value, list):
                count = len(value)
                return f"[ {count} 个元素 ]"
            return ""

        def render_value(value: Any, key: Optional[str] = None) -> str:
            if isinstance(value, dict):
                if not value:
                    return f'<div><span class="json-key">"{key}"</span>: <span class="json-bracket">{{}}</span></div>' if key else '<span class="json-bracket">{{}}</span>'
                
                items = []
                for k, v in value.items():
                    items.append(render_value(v, k))
                
                preview = get_preview(value)
                content = '<div class="json-item">' + ''.join(items) + '</div>'
                if key is not None:
                    return f'''
                        <div>
                            <span class="json-toggle">-</span>
                            <span class="json-key">"{key}"</span>: 
                            <span class="json-bracket">{{</span>
                            <span class="json-preview">{preview}</span>
                            {content}
                            <span class="json-bracket">}}</span>
                        </div>
                    '''
                return f'''
                    <div>
                        <span class="json-toggle">-</span>
                        <span class="json-bracket">{{</span>
                        <span class="json-preview">{preview}</span>
                        {content}
                        <span class="json-bracket">}}</span>
                    </div>
                '''
                
            elif isinstance(value, list):
                if not value:
                    return f'<div><span class="json-key">"{key}"</span>: <span class="json-bracket">[]</span></div>' if key else '<span class="json-bracket">[]</span>'
                
                items = []
                for item in value:
                    items.append(render_value(item))
                
                preview = get_preview(value)
                content = '<div class="json-item">' + ''.join(items) + '</div>'
                if key is not None:
                    return f'''
                        <div>
                            <span class="json-toggle">-</span>
                            <span class="json-key">"{key}"</span>: 
                            <span class="json-bracket">[</span>
                            <span class="json-preview">{preview}</span>
                            {content}
                            <span class="json-bracket">]</span>
                        </div>
                    '''
                return f'''
                    <div>
                        <span class="json-toggle">-</span>
                        <span class="json-bracket">[</span>
                        <span class="json-preview">{preview}</span>
                        {content}
                        <span class="json-bracket">]</span>
                    </div>
                '''
                
            elif isinstance(value, str):
                return f'<div><span class="json-key">"{key}"</span>: <span class="json-string">"{value}"</span></div>' if key else f'<div><span class="json-string">"{value}"</span></div>'
            elif isinstance(value, (int, float)):
                return f'<div><span class="json-key">"{key}"</span>: <span class="json-number">{value}</span></div>' if key else f'<div><span class="json-number">{value}</span></div>'
            elif isinstance(value, bool):
                return f'<div><span class="json-key">"{key}"</span>: <span class="json-boolean">{str(value).lower()}</span></div>' if key else f'<div><span class="json-boolean">{str(value).lower()}</span></div>'
            elif value is None:
                return f'<div><span class="json-key">"{key}"</span>: <span class="json-null">null</span></div>' if key else '<div><span class="json-null">null</span></div>'
            return ''
        
        # 渲染JSON内容
        content = render_value(self.data)
        
        # 添加工具栏和内容容器
        toolbar = f"""
        <div class="json-toolbar">
            <button id="{self.id}-expand-all">展开全部</button>
            <button id="{self.id}-expand-one">展开一级</button>
            <button id="{self.id}-collapse-one">折叠一级</button>
            <button id="{self.id}-collapse-all">折叠全部</button>
        </div>
        """
        
        return f"""
        {styles}
        <div id="{self.id}" class="json-view theme-{self.theme}">
            {toolbar}
            <div class="json-content">
                {content}
            </div>
        </div>
        {script}
        """ 