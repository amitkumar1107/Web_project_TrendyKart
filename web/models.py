from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator

class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.IntegerField()

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICE=(
    ('M','Mens'),
    ('W','Women'),
    ('B','Boys'),
    ('G','Girls'),

)

class Product(models.Model):
    titile=models.CharField(max_length=100)
    product_name=models.CharField(max_length=100)
    price=models.IntegerField()
    dec=models.CharField(max_length=500)
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=100)
    product_img=models.ImageField(upload_to='productimg')
    
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
status_choise=(
        ('Accepted','Accepted'),
        ('Shiped','Shiped'),
        ('Out for delivery','Out for delivery'),
        ('Deliverd','Deleverd'),
    )
class orderplaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=status_choise,default='panding')




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link order to a user
    total_price = models.IntegerField()  # Store total price of all products in cart
    created_at = models.DateTimeField(auto_now_add=True)  # Order timestamp

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} (Order {self.order.id})"
    
class profile(models.Model):
    name_update=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='productimg')