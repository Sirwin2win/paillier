from django.db import models

class EncryptedNumber(models.Model):
    encrypted_value = models.TextField()
    exponent = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)