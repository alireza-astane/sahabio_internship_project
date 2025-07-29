from django.db import models


class App(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AppStat(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="stats")
    timestamp = models.DateTimeField()
    min_installs = models.BigIntegerField()
    # installs = models.PositiveIntegerField()
    score = models.FloatField()
    ratings = models.PositiveIntegerField()
    reviews = models.BigIntegerField()
    updated = models.BigIntegerField()
    version = models.CharField(max_length=50)
    ad_supported = models.BooleanField()

    class Meta:
        unique_together = ("app", "timestamp")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.app.package_name} stats at {self.timestamp}"


class AppReview(models.Model):
    review_id = models.CharField(max_length=255, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="reviews")
    timestamp = models.DateTimeField()
    user_name = models.CharField(max_length=255)
    score = models.IntegerField()
    content = models.TextField()
    thumbs_up = models.PositiveIntegerField()

    # Optional field for later sentiment analysis
    sentiment = models.CharField(
        max_length=10,
        choices=[
            ("positive", "Positive"),
            ("neutral", "Neutral"),
            ("negative", "Negative"),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Review {self.review_id} for {self.app.package_name}"
