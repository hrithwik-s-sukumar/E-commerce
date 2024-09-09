from django.db import models
from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=200,unique=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    image        = models.ImageField(upload_to="products/")
    stock        = models.IntegerField()
    category     = models.ForeignKey(Category,on_delete = models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def _str_(self):
        return self.product_name
    

    def save(self, *args, **kwargs):
        # Example check: If stock is greater than 0, set is_available to True
        if self.stock > 0:
            self.is_available = True
        else:
            self.is_available = False
        super().save(*args, **kwargs)

    class Meta:
       db_table = 'product_table'
