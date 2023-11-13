from django.db import models
from user.models import Profile
import uuid
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    updated_time_stamp = models.DateTimeField(auto_now=True)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    # display products with full name in the database
    def __str__(self):
        return self.name

    # display new products first
    class Meta:
        ordering = ['-updated_time_stamp']
        indexes = [
        models.Index(fields=['id'])
    ]

    # image error solution
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Order(models.Model):
    customer = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True)

    # display order with transcation_id in the database
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])

        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])

        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    # display order item with product name in the database
    def __str__(self):
        return str(self.product)
    
    # display new order item first
    class Meta:
        ordering = ['-date_added']
        indexes = [
        models.Index(fields=['id'])
    ]

    # get total price for product
    @property
    def get_total(self):
        total = self.quantity * self.product.price

        return total
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=False)
    city = models.CharField(max_length=255, null=True, blank=False)
    zipcode = models.CharField(max_length=255, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    # display shipping address with address info in the database
    def __str__(self):
        return self.address
    

class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    reference = models.CharField(max_length=100, null=False)
        

    def __str__(self):
        return f"{self.customer.name}'s {self.product.name} Payment"
    
    class Meta:
        ordering = ['-date_paid']
