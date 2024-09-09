from django.db import models
from products.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=False, null=False)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id

    class Meta:
        db_table = 'cartid_table'    
    

class CartItem(models.Model):
    product   = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart      = models.ForeignKey(Cart,on_delete=models.CASCADE) 
    quantity  = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product
    

    def sub_total(self):
        return self.product.price * self.quantity
    
    class Meta:
        db_table = 'cart_table'


    

