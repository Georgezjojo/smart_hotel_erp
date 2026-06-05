from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)  # ingredient, beverage, cleaning
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='pcs')
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class PurchaseOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    received = models.BooleanField(default=False)