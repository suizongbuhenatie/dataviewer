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
        "name": "Product A",
        "price": 100,
        "description": "This handbag is the perfect choice for fashion enthusiasts. Made from high-quality durable leather, it offers a soft touch and premium feel. The minimalist design, free from excessive decorations, exudes elegance through its refined lines. The bag's spacious interior with well-organized compartments easily accommodates phones, wallets, cosmetics, and other daily essentials. The reinforced handle ensures comfortable carrying and durability. Its classic solid color design perfectly complements both casual outings and office wear. Whether shopping, working, or attending gatherings, this bag showcases your fashion sense and unique charm.",
        "image": [image, image, image],
        "info": {
            "name": "Elegant Test Data 1",
            "age": 18,
            "gender": "male",
            "description": "This is elegant test data " * 30,
        },
    },
    {
        "id": 2,
        "name": "Product B",
        "price": 200,
        "image": ["example.jpg"] * 12,
        "description": "This handbag is the perfect choice for fashion enthusiasts. Made from high-quality durable leather, it offers a soft touch and premium feel. The minimalist design, free from excessive decorations, exudes elegance through its refined lines. The bag's spacious interior with well-organized compartments easily accommodates phones, wallets, cosmetics, and other daily essentials. The reinforced handle ensures comfortable carrying and durability. Its classic solid color design perfectly complements both casual outings and office wear. Whether shopping, working, or attending gatherings, this bag showcases your fashion sense and unique charm.",
        "video": "example.mp4",
    },
    {
        "id": 2,
        "name": "Product B",
        "price": 200,
        "image": "example.jpg",
        "description": "This handbag is the perfect choice for fashion enthusiasts. Made from high-quality durable leather, it offers a soft touch and premium feel. The minimalist design, free from excessive decorations, exudes elegance through its refined lines. The bag's spacious interior with well-organized compartments easily accommodates phones, wallets, cosmetics, and other daily essentials. The reinforced handle ensures comfortable carrying and durability. Its classic solid color design perfectly complements both casual outings and office wear. Whether shopping, working, or attending gatherings, this bag showcases your fashion sense and unique charm.",
        "video": "example.mp4",
    },
    {
        "id": 3,
        "name": "Product C",
        "price": 300,
        "image": image,
        "description": "This handbag is the perfect choice for fashion enthusiasts. Made from high-quality durable leather, it offers a soft touch and premium feel. The minimalist design, free from excessive decorations, exudes elegance through its refined lines. The bag's spacious interior with well-organized compartments easily accommodates phones, wallets, cosmetics, and other daily essentials. The reinforced handle ensures comfortable carrying and durability. Its classic solid color design perfectly complements both casual outings and office wear. Whether shopping, working, or attending gatherings, this bag showcases your fashion sense and unique charm.",
    },
]

with Page("Table Demo") as page:
    Header("Table Component Demo", level=1)
    Table(data=data)
    page.save("output/table_demo.html")
