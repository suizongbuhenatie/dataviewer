from dataviewer import Page
from dataviewer.components import Table, Header
from PIL import Image
import io
import base64

data = [
    {"id": 1, "name": "产品A", "price": 100, "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。"},
    {"id": 2, "name": "产品B", "price": 200, "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。"},
    {"id": 3, "name": "产品C", "price": 300, "description": "这款手提包是时尚达人的不二之选。它整体采用高品质的耐磨皮革制成，触感柔软且极具质感。简约的设计风格，没有过多繁杂的装饰，却在线条的勾勒下尽显优雅大气。包身容量很大，内部合理的隔层可轻松容纳手机、钱包、化妆品等日常用品。提手部分加固处理，手提舒适且不易断裂。经典的纯色外观，无论是休闲出行还是职场办公都能完美搭配。无论是逛街、上班还是参加聚会，背着它都能彰显您的时尚品味和独特魅力。"},
]

with Image.open("examples/example.jpg") as img:
    img = img.convert("RGB")
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        image = base64.b64encode(output.getvalue()).decode()

for item in data:
    item["image"] = image

data[0]['image'] = [image, image, image]
data[0]["map"] = {
    "name": "test_data1",
    "age": 18,
    "gender": "male",
    "test": "test_data2",
    "description": "这是测试数据2",
}

with Page("表格演示") as page:
    Header("表格组件演示", level=1)
    Table(data=data)
    page.save("output/table_demo.html")
