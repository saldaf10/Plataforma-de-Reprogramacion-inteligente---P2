from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class Command(BaseCommand):
    help = "Seed initial categories and products"

    def _generate_image(self, text: str, color: str = "#01c9ff") -> ContentFile:
        img = Image.new("RGB", (800, 600), color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        draw.text((20, 20), text, fill=(255, 255, 255), font=font)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=80)
        return ContentFile(buf.getvalue(), name=f"{text.replace(' ', '_').lower()}.jpg")

    def handle(self, *args, **options):
        data = {
            "zapatos": [
                {"name": "Tenis Urban Pro", "price": Decimal("79.99"), "stock": 50, "description": "Tenis cómodos para uso diario.", "color": "#5b6cf0"},
                {"name": "Botas Trekking X", "price": Decimal("129.90"), "stock": 20, "description": "Botas resistentes para montaña.", "color": "#4aa3df"},
            ],
            "lociones": [
                {"name": "Aroma Nocturno", "price": Decimal("59.00"), "stock": 40, "description": "Fragancia elegante para la noche.", "color": "#764ba2"},
                {"name": "Cítrico Fresh", "price": Decimal("45.50"), "stock": 60, "description": "Aroma fresco y ligero.", "color": "#01c9ff"},
            ],
            "proteinas": [
                {"name": "Whey Protein 1kg", "price": Decimal("35.00"), "stock": 100, "description": "Proteína de suero sabor vainilla.", "color": "#52b788"},
                {"name": "Caseína 1kg", "price": Decimal("39.90"), "stock": 70, "description": "Proteína de absorción lenta para la noche.", "color": "#2d6a4f"},
            ],
        }

        for cat_name, products in data.items():
            category, _ = Category.objects.get_or_create(name=cat_name.title())
            created = 0
            for p in products:
                prod, _ = Product.objects.get_or_create(
                    name=p["name"],
                    defaults={
                        "category": category,
                        "price": p["price"],
                        "stock": p["stock"],
                        "description": p["description"],
                    },
                )
                if not prod.image:
                    img_file = self._generate_image(prod.name, p.get("color", "#01c9ff"))
                    prod.image.save(img_file.name, img_file, save=True)
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} products for {category.name}"))
