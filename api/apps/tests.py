from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import App
from django.db import connection


class AppAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app_data = {
            "package_name": "com.example.test",
            "category": "Tools",
            "is_active": True,
        }
        self.app = App.objects.create(**self.app_data)

    def test_create_app(self):
        url = reverse("app-list")
        data = {
            "package_name": "com.example.new",
            "category": "Productivity",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_apps(self):
        url = reverse("app-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_app(self):
        url = reverse("app-detail", args=[self.app.id])
        data = {"category": "Updated"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.app.refresh_from_db()
        self.assertEqual(self.app.category, "Updated")

    def test_delete_app(self):
        url = reverse("app-detail", args=[self.app.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Database direct test ---
    def test_database_connection(self):
        """Test direct database connection and query."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM apps_app")
            count = cursor.fetchone()[0]
        self.assertTrue(count >= 1)

    # --- Crawler simulation test ---
    def test_crawler_simulation(self):
        """Simulate a crawler result (mocked)."""
        data = {
            "package_name": "com.example.crawler",
            "category": "Crawler",
            "is_active": True,
        }
        response = self.client.post(reverse("app-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["package_name"], "com.example.crawler")

    # --- Consumer simulation test ---
    def test_consumer_simulation(self):
        """Simulate consumer inserting a review (mocked)."""
        from apps.models import AppReview

        app = self.app
        review = AppReview.objects.create(
            review_id="test-review-1",
            app=app,
            timestamp="2025-07-24T00:00:00Z",
            content="Great app!",
            score=5,
            thumbs_up=10,
            user_name="tester",
        )
        self.assertEqual(AppReview.objects.filter(app=app).count(), 1)
        self.assertEqual(review.content, "Great app!")
