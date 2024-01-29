from django.db import models
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



class Product(models.Model):
    bggid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)       
    description =models.TextField(blank=True)
    is_active = models.BooleanField(default=True) 
    
    slug = models.SlugField(max_length=100, blank=True)
    min_players=models.IntegerField(blank=True)
    max_players=models.IntegerField(blank=True)
    image_url=models.URLField(blank=True)
    image1 =models.ImageField(upload_to='images/', null=True, blank=True)
    image2 =models.ImageField(upload_to='images/', null=True, blank=True)
    image3 =models.ImageField(upload_to='images/', null=True, blank=True)
    image4 =models.ImageField(upload_to='images/', null=True, blank=True)
    image5 =models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail =models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail_url=models.URLField(blank=True)
    


    def __str__(self):
     return self.name
    
class Productweb(models.Model):
    bggid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)       
    description =models.TextField(blank=True)
    is_active = models.BooleanField(default=True) 
    
    slug = models.SlugField(max_length=100, blank=True)
    min_players=models.IntegerField(blank=True)
    max_players=models.IntegerField(blank=True)
    image_url=models.URLField(blank=True)
    image1 =models.ImageField(upload_to='images/', null=True, blank=True)
    image2 =models.ImageField(upload_to='images/', null=True, blank=True)
    image3 =models.ImageField(upload_to='images/', null=True, blank=True)
    image4 =models.ImageField(upload_to='images/', null=True, blank=True)
    image5 =models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail =models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail_url=models.URLField(blank=True)
    


    def __str__(self):
     return self.name
    

class Fetched_Product(models.Model):
    bggid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)       
    description =models.TextField(blank=True)    

    slug = models.SlugField(max_length=100, null=True, blank=True)
    min_players=models.IntegerField(null=True, blank=True)
    max_players=models.IntegerField(null=True, blank=True)
    image_url=models.URLField(blank=True)
    thumbnail_url=models.URLField(blank=True)
    

    def __str__(self):
     return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug based on the name field
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.owner)

class Vote(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    value = models.IntegerField(default='0')
    owner = models.ForeignKey('auth.User', related_name='votes', on_delete=models.CASCADE)
    
    def __str__(self):
        return 'User {} voted {} on product {}'.format(self.owner, self.value, self.product)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
     return self.user.username
    
class OwnedProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)    
    owner = models.ForeignKey('auth.User', related_name='ownedproducts', on_delete=models.CASCADE)