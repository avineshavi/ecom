from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other seller-related fields as needed

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    guest_user_id = models.CharField(max_length=255, null=True, blank=True)
    products = models.ManyToManyField('Product')

    def __str__(self):
        return f"Cart - {self.user.username if self.user else 'Guest'}"
