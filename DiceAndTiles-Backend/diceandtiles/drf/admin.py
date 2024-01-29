from django.contrib import admin
from django.core.management import call_command
from .models import Product, Comment, Profile, Vote, Fetched_Product, OwnedProduct
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.contrib.auth.models import User
import random



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']
    ordering = ['id']

    actions = ['get_remote_image','make_users_cast_vote']

    def make_users_cast_vote(self, request, queryset):
        # Get all registered users
        all_users = User.objects.exclude(is_staff=True)

        for product in queryset:
            # Get users who haven't voted for the current product
            users_without_vote = all_users.exclude(votes__product=product)

            # Create a vote with a random value (1 or 2) for each user
            for user in users_without_vote:
                value = random.choice([1, 2])
                Vote.objects.create(product=product, owner=user, value=value)
                print(f'user {user.id} voted on {product.slug}')


              
    make_users_cast_vote.short_description = "Make users cast votes for selected products"

    def get_remote_image(self, request, queryset):
        for product in queryset:
            if product.image_url and not product.image1:
             try:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(product.image_url).read())
                img_temp.flush()
                for x in range (1, 6):                                       
                    getattr(product, f"image{x}").save(f"{product.pk}_image{x}.jpg", File(img_temp))
                product.save()
                print(f'Successfully downloaded and assigned JPG image for Product {product.slug}')
                self.message_user(request, f'Successfully downloaded and assigned JPG image for Product {product.slug}')
             except Exception as e:
                self.message_user(request, f'Error downloading or assigning image for Product {product.slug}: {e}', level='error')
                print(f'Error downloading or assigning image for Product {product.slug}: {e}')
            if product.thumbnail_url and not product.thumbnail:
             try:
                img_temp2 = NamedTemporaryFile(delete=True)
                img_temp2.write(urlopen(product.thumbnail_url).read())
                img_temp2.flush()                                                   
                product.thumbnail.save(f"{product.pk}_thumbnail.jpg", File(img_temp2))
                product.save()
                print(f'Successfully downloaded and assigned JPG thumbnail for Product {product.slug}')
                self.message_user(request, f'Successfully downloaded and assigned JPG thumbnail for Product {product.slug}')
             except Exception as e:
                self.message_user(request, f'Error downloading or assigning thumbnail for Product {product.slug}: {e}', level='error')
                print(f'Error downloading or assigning thumbnail for Product {product.slug}: {e}')

    get_remote_image.short_description = 'download image for product'

@admin.register(Fetched_Product)
class Fetched_ProductAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']
    ordering = ['id']
    actions = ['custom_action','fetch','insert']

    def custom_action(self, request, queryset):
        # Call your custom command using call_command
        call_command('populatecommand')

    custom_action.short_description = 'Populate PRODUCTS table command'

    def fetch(self, request, queryset):
        # Call your custom command using call_command
        call_command('scrapperfetch')

    fetch.short_description = 'fetch data from bgg to scrapper'

    def insert(self, request, queryset):
        # Call your custom command using call_command
        call_command('scrapperinsert')

    insert.short_description = 'populate db with products fetched via scrapper'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','body','created_on','owner']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    actions = ['custom_action']

    def custom_action(self, request, queryset):
        # Call your custom command using call_command
        call_command('create_users')
    custom_action.short_description = 'create users 1-200'
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['product','value','owner']


@admin.register(OwnedProduct)
class OwnedProductAdmin(admin.ModelAdmin):
    list_display = ['product','owner']



