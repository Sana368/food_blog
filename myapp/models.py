from django.db import models
from django.contrib.auth.models import User



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()

    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    







class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

    def get_total(self):
        total = sum(item.get_total_price() for item in self.cart_items.all())
        return total





from django.db import models
from django.contrib.auth.models import User  

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)  # New field for product description

    def __str__(self):
        return self.name

    def get_short_description(self):
        return self.description[:100]  # Optional: A method to return the first 100 characters of the description

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This links the cart item to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'

    


