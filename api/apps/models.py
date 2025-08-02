"""
Models for managing applications, their statistics, and user reviews.

Classes:
    App:
        Represents an application with its package name, category, status, and timestamps.
        Fields:
            package_name (str): Unique package identifier for the app.
            category (str): Category of the app.
            is_active (bool): Indicates if the app is active.
            created_at (datetime): Timestamp when the app was created.
            updated_at (datetime): Timestamp when the app was last updated.

    AppStat:
        Stores statistical data for an app at a specific timestamp.
        Fields:
            app (App): Reference to the associated app.
            timestamp (datetime): Time of the statistics record.
            min_installs (int): Minimum number of installs.
            score (float): App score/rating.
            ratings (int): Number of ratings.
            reviews (int): Number of reviews.
            updated (int): Last updated timestamp (epoch).
            version (str): App version.
            ad_supported (bool): Indicates if the app supports ads.
        Meta:
            unique_together: Ensures unique statistics per app and timestamp.
            ordering: Orders by descending timestamp.

    AppReview:
        Represents a user review for an app.
        Fields:
            review_id (str): Unique identifier for the review.
            app (App): Reference to the reviewed app.
            timestamp (datetime): Time of the review.
            user_name (str): Name of the reviewer.
            score (int): Review score.
            content (str): Review content.
            thumbs_up (int): Number of thumbs up for the review.
            sentiment (str, optional): Sentiment analysis result ("positive", "neutral", "negative").
        Meta:
            ordering: Orders by descending timestamp.

Swagger Documentation:
    These models are used for API schema generation with Django REST Framework and drf-yasg/swagger.
    Each field is automatically documented for API endpoints, including type, description, and choices.
    Use serializers to expose these models in your API for interactive documentation and validation.
"""

from django.db import models


class App(models.Model):
    """
    Represents an application.

    Swagger Schema:
        package_name (str): Unique package identifier for the app.
        category (str): Category of the app.
        is_active (bool): Indicates if the app is active.
        created_at (datetime): Timestamp when the app was created.
        updated_at (datetime): Timestamp when the app was last updated.
    """

    package_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AppStat(models.Model):
    """
    Swagger Schema:
        app (App): Reference to the associated app.
        timestamp (datetime): Time of the statistics record.
        min_installs (int): Minimum number of installs.
        score (float): App score/rating.
        ratings (int): Number of ratings.
        reviews (int): Number of reviews.
        updated (int): Last updated timestamp (epoch).
        version (str): App version.
        ad_supported (bool): Indicates if the app supports ads.
    """

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
        """
        Meta class for model configuration.
        Attributes:
            unique_together (tuple): Ensures that the combination of 'app' and 'timestamp' fields is unique across records.
            ordering (list): Specifies default ordering of records by descending 'timestamp'.
        Swagger Documentation:
            - unique_together: Enforces uniqueness constraint for ('app', 'timestamp') pairs.
            - ordering: Default sort order for API responses is by most recent 'timestamp' first.
        """

        unique_together = ("app", "timestamp")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.app.package_name} stats at {self.timestamp}"


class AppReview(models.Model):
    """
    Represents a review for an app.
    Attributes:
        review_id (str): Unique identifier for the review.
        app (App): The app being reviewed.
        timestamp (datetime): Date and time when the review was posted.
        user_name (str): Name of the user who posted the review.
        score (int): Numerical score given by the user.
        content (str): Text content of the review.
        thumbs_up (int): Number of thumbs up received by the review.
        sentiment (str, optional): Sentiment analysis result for the review. Choices are "positive", "neutral", or "negative".
    Swagger Schema:
        - review_id: string, required, unique identifier for the review
        - app: integer, required, ID of the app being reviewed
        - timestamp: string (date-time), required, time of review
        - user_name: string, required, name of the reviewer
        - score: integer, required, score given by the reviewer
        - content: string, required, review text
        - thumbs_up: integer, required, number of thumbs up
        - sentiment: string, optional, sentiment analysis result ("positive", "neutral", "negative")
    """

    review_id = models.CharField(max_length=255, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="reviews")
    timestamp = models.DateTimeField()
    user_name = models.CharField(max_length=255)
    score = models.IntegerField()
    content = models.TextField()
    thumbs_up = models.PositiveIntegerField()

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
        """
        Meta class for Django model configuration.
        Attributes:
            ordering (list): Specifies the default ordering for querysets of this model.
                In this case, objects are ordered by 'timestamp' in descending order.
        Swagger:
            This configuration affects the default ordering of model instances in API responses.
            When using Django REST Framework with Swagger/OpenAPI documentation, the ordering
            will be reflected in list endpoints unless overridden by query parameters.
        """

        ordering = ["-timestamp"]

    def __str__(self):
        return f"Review {self.review_id} for {self.app.package_name}"
