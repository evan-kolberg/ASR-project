from django.db import models

class data(models.Model):
    encrypted_hash = models.TextField()
    number = models.DateTimeField(auto_now_add=True)
