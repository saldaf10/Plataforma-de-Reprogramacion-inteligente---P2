from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal
from django.core.files import File
import os
from pathlib import Path


class Command(BaseCommand):
    help = "Seed initial categories and products"

    def handle(self, *args, **options):
        # Mapeo de productos a nombres de archivo de imagen (usando los nombres reales de los archivos)
        image_mapping = {
            "Tenis Urban Pro": "tenisurbanpro.png",
            "Botas Trekking X": "botastrekkingx.png",
            "Aroma Nocturno": "aromanocturno.png",
            "Cítrico Fresh": "Citricofresh.png",
            "Whey Protein 1kg": "Wheyprotein1kg.png",
            "Caseína 1kg": "Caseina1kg.png",
            # También mapear productos del generate_test_data.py
            "Zapatos Deportivos Pro": "tenisurbanpro.png",  # Usar imagen similar
            "Loción Corporal Fresh": "Citricofresh.png",  # Usar imagen similar
            "Proteína Whey 1kg": "Wheyprotein1kg.png",
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
        # Buscar imágenes en la carpeta imagenes/ primero, luego en media/products/
        images_dir = base_dir / "imagenes"
        media_products_dir = base_dir / "media" / "products"
        
        # Crear directorio media/products si no existe
        media_products_dir.mkdir(parents=True, exist_ok=True)

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
                    # Buscar primero en imagenes/, luego en media/products/
                    image_path = images_dir / image_filename
                    if not image_path.exists():
                        image_path = media_products_dir / image_filename
                    
                    if image_path.exists():
                        with open(image_path, 'rb') as img_file:
                            prod.image.save(image_filename, File(img_file), save=True)
                        self.stdout.write(self.style.SUCCESS(f"  → Image assigned to {prod.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  ⚠ Image not found: {image_filename}"))
                
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} products for {category.name}"))
