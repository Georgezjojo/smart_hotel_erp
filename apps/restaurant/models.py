from django.db import models

class MenuCategory(models.Model):
    name = models.CharField(max_length=50)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
    available = models.BooleanField(default=True)

class Table(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    room = models.CharField(max_length=20, blank=True)  # for room service
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('preparing','Preparing'),('ready','Ready'),('served','Served')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)