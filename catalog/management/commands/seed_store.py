from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal
from django.core.files import File
from pathlib import Path


class Command(BaseCommand):
    help = "Seed initial categories and products"

    def handle(self, *args, **options):
        # Mapeo de productos a nombres de archivo tal como existen en el repo
        # Las imágenes están en la carpeta "imagenes" en la raíz del proyecto
        image_mapping = {
            "Tenis Urban Pro": "tenisurbanpro.png",
            "Botas Trekking X": "botastrekkingx.png",
            "Aroma Nocturno": "aromanocturno.png",
            "Cítrico Fresh": "Citricofresh.png",
            "Whey Protein 1kg": "Wheyprotein1kg.png",
            "Caseína 1kg": "Caseina1kg.png",
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

        # Obtener la ruta base del proyecto y la carpeta de imágenes existente
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        images_dir = base_dir / "imagenes"
        # Asegurar carpeta de media/products exista
        from django.conf import settings
        media_products = Path(settings.MEDIA_ROOT) / "products"
        media_products.mkdir(parents=True, exist_ok=True)

        for cat_name, products in data.items():
            category, _ = Category.objects.get_or_create(name=cat_name.title())  # type: ignore[attr-defined]
            created = 0
            for p in products:
                prod, _ = Product.objects.get_or_create(  # type: ignore[attr-defined]
                    name=p["name"],
                    defaults={
                        "category": category,
                        "price": p["price"],
                        "stock": p["stock"],
                        "description": p["description"],
                    },
                )
                
                # Asignar/actualizar imagen si existe en el repo
                if p["name"] in image_mapping:
                    image_filename = image_mapping[p["name"]]
                    image_path = images_dir / image_filename
                    
                    if image_path.exists():
                        with open(image_path, 'rb') as img_file:
                            # Guardar bajo el upload_to de Product (products/)
                            prod.image.save(image_filename, File(img_file), save=True)
                        self.stdout.write(self.style.SUCCESS(f"  → Image set for {prod.name}: {prod.image.name}"))  # type: ignore[attr-defined]
                    else:
                        self.stdout.write(self.style.WARNING(f"  ⚠ Image not found: {image_path}"))  # type: ignore[attr-defined]
                
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} products for {category.name}"))  # type: ignore[attr-defined]
