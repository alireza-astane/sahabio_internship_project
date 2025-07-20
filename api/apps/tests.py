from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import App


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
