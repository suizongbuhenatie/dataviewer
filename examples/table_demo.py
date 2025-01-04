import base64
import io

from PIL import Image

from dataviewer import Page
from dataviewer.components import Header, Table

with Image.open("examples/example.jpg") as img:
    img = img.convert("RGB")
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        image = base64.b64encode(output.getvalue()).decode()

data = [
    {
        "id": 1,
        "name": "产品A",
        "price": 100,
        "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。",
        "image": [image, image, image],
        "info": {
            "name": "优雅的测试数据1",
            "age": 18,
            "gender": "male",
            "description": "这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据这是优雅的测试数据",
        },
    },
    {
        "id": 2,
        "name": "产品B",
        "price": 200,
        "image": [
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
            "example.jpg",
        ],
        "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。",
        "video": "example.mp4",
    },
    {
        "id": 2,
        "name": "产品B",
        "price": 200,
        "image": "example.jpg",
        "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。",
        "video": "example.mp4",
    },
    {
        "id": 3,
        "name": "产品C",
        "price": 300,
        "image": image,
        "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。",
    },
]

with Page("表格演示") as page:
    Header("表格组件演示", level=1)
    Table(data=data)
    page.save("output/table_demo.html")
