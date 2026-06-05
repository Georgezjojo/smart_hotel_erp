from django.db import models

class PredictionCache(models.Model):
    prediction_type = models.CharField(max_length=50)
    input_hash = models.CharField(max_length=64, unique=True)
    result = models.TextField()  # JSON
    created_at = models.DateTimeField(auto_now_add=True)