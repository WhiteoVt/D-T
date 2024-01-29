import os
import requests
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from diceandtiles.drf.models import Product, Fetched_Product

class Command(BaseCommand):
    help = 'Check and create entries in Products from Fetched_Products'

    def handle(self, *args, **options):
        fetched_products = Fetched_Product.objects.all()

        for fetched_product in fetched_products:
           

            # Check if entry already exists in Products
            if not Product.objects.filter(bggid=fetched_product.bggid).exists():
                # Create new entry in Products
                new_product = Product(
                    bggid=fetched_product.bggid,
                    name=fetched_product.name,
                    description=fetched_product.description,                 
                    thumbnail_url=fetched_product.thumbnail_url,
                    image_url=fetched_product.image_url,
                    min_players=fetched_product.min_players,
                    max_players=fetched_product.max_players
                )
                if not fetched_product.slug:
                    new_product.slug = slugify(fetched_product.name)
                else:
                    new_product.slug = fetched_product.slug

                new_product.save()
                
                self.stdout.write(self.style.SUCCESS(f'Created new entry in Products for bggid={fetched_product.bggid}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Entry with bggid={fetched_product.bggid} already exists in Products'))
