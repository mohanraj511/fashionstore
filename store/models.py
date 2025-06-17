from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('shirts', 'Shirts'),
        ('pants', 'Pants'),
        ('watches', 'Watches'),
        ('caps', 'Caps'),
        ('perfume', 'Perfume'),
        ('socks', 'Socks'),
        ('underwear', 'Underwear'),
        ('shorts', 'Shorts'),
        ('human', 'Human'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name

# ✅ Profile model outside Product
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    def _str_(self):
        return self.user.username
    def create_user_profile(sender,instance,created,**kwrgs):
        if created:
            Profile.objects.create(user=instance)
class CartItem(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at =models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price*self.quantity      
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_paid =models.BooleanField(default =False)
    address=models.TextField(null=False,blank=False)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Save price at order time

    def _str_(self):
        return f"{self.quantity} x {self.product.name}"