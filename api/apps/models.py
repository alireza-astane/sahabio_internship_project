from django.db import models


class App(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class App(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AppStatSnapshot(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    score = models.FloatField()
    ratings = models.FloatField()
    installs = models.IntegerField()
    reviews = models.IntegerField()


class AppReview(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    reviewId = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField()
    content = models.TextField()
    score = models.FloatField()
    thumbsUpCount = models.IntegerField()
    username = models.CharField(max_length=255)
