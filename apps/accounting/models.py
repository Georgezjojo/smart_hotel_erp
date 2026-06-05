from django.db import models

class FinancialEntry(models.Model):
    ENTRY_TYPE = [('income','Income'), ('expense','Expense')]
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    category = models.CharField(max_length=50, blank=True)