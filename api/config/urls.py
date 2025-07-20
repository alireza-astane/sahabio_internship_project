from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.views import AppViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = routers.DefaultRouter()
router.register(r"apps", AppViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
