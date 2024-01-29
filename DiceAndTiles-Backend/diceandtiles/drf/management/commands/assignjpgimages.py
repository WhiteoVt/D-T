# assign_images.py
import requests
import os
from django.core.management.base import BaseCommand
from diceandtiles.drf.models import Product
from django.core.files import File

class Command(BaseCommand):
    help = 'Assign locally downloaded images to Product model fields'

    def handle(self, *args, **options):
        products = Product.objects.all()

        for product in products:
            try:
                for x in range(1, 6):
                    image_path = f'./media/images/{product.pk}_image{x}.jpg'
                    thumbnail_path = f'./media/images/{product.pk}_thumbnail.jpg'

                    # Assign images to the appropriate fields
                    if x == 1:
                        product.image1.save(os.path.basename(image_path), File(open(image_path, 'rb')))
                    elif x == 2:
                        product.image2.save(os.path.basename(image_path), File(open(image_path, 'rb')))
                    elif x == 3:
                        product.image3.save(os.path.basename(image_path), File(open(image_path, 'rb')))
                    elif x == 4:
                        product.image4.save(os.path.basename(image_path), File(open(image_path, 'rb')))
                    elif x == 5:
                        product.image5.save(os.path.basename(image_path), File(open(image_path, 'rb')))

                # Assign thumbnail to the appropriate field
                product.thumbnail.save(os.path.basename(thumbnail_path), File(open(thumbnail_path, 'rb')))

                product.save()
                print(f'Successfully assigned images for Product {product.slug}')
            except Exception as e:
                print(f'Error assigning images for Product {product.slug}: {e}')

