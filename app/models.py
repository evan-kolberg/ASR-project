from django.db import models

class data(models.Model):
    number = models.IntegerField()
    encrypted_hash = models.CharField(max_length=256)
