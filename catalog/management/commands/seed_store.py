from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal
from django.core.files import File
import os
from pathlib import Path


class Command(BaseCommand):
    help = "Seed initial categories and products"

    def handle(self, *args, **options):
        # Mapeo de productos a nombres de archivo de imagen
        image_mapping = {
            "Tenis Urban Pro": "tenis_urban_pro.png",
            "Botas Trekking X": "botas_trekking_x.png",
            "Aroma Nocturno": "aroma_nocturno.png",
            "Cítrico Fresh": "cítrico_fresh.png",
            "Whey Protein 1kg": "whey_protein_1kg.png",
            "Caseína 1kg": "caseína_1kg.png",
        }

        data = {
            "zapatos": [
                {"name": "Tenis Urban Pro", "price": Decimal("79.99"), "stock": 50, "description": "Tenis cómodos para uso diario."},
                {"name": "Botas Trekking X", "price": Decimal("129.90"), "stock": 20, "description": "Botas resistentes para montaña."},
            ],
            "lociones": [
                {"name": "Aroma Nocturno", "price": Decimal("59.00"), "stock": 40, "description": "Fragancia elegante para la noche."},
                {"name": "Cítrico Fresh", "price": Decimal("45.50"), "stock": 60, "description": "Aroma fresco y ligero."},
            ],
            "proteinas": [
                {"name": "Whey Protein 1kg", "price": Decimal("35.00"), "stock": 100, "description": "Proteína de suero sabor vainilla."},
                {"name": "Caseína 1kg", "price": Decimal("39.90"), "stock": 70, "description": "Proteína de absorción lenta para la noche."},
            ],
        }

        # Obtener la ruta base del proyecto
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        images_dir = base_dir / "media" / "products"

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
                
                # Asignar imagen si existe y el producto no tiene una
                if not prod.image and p["name"] in image_mapping:
                    image_filename = image_mapping[p["name"]]
                    image_path = images_dir / image_filename
                    
                    if image_path.exists():
                        with open(image_path, 'rb') as img_file:
                            prod.image.save(image_filename, File(img_file), save=True)
                        self.stdout.write(self.style.SUCCESS(f"  → Image assigned to {prod.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  ⚠ Image not found: {image_path}"))
                
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} products for {category.name}"))
