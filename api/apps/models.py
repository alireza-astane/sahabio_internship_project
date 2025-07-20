from django.db import models


class App(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
