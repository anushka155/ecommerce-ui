from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='products/')
    short_description = models.CharField(max_length=255)
    full_description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
status_choice=[
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),

]
    
class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.CharField(max_length=100, unique=True)
    tax = models.DecimalField(max_digits=10,decimal_places=2)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    service_charge = models.DecimalField(max_digits=10,decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20,choices=status_choice, default='pending')
    buyer_name = models.CharField(max_length=100)
    buyer_phone = models.CharField(max_length=20)

    def complete_order(self):
        self.status = 'completed'
        self.save()

    def incomplete_order(self):
        self.status = 'processing'
        self.save()

    def cancel_order(self):
        self.status = 'cancelled'
        self.save()

    class Meta:
        ordering = ['-created_at']