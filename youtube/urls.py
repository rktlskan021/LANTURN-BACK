from django.urls import path, include, re_path
from rest_framework import routers
from .views import LinkViewSet

router = routers.DefaultRouter()
router.register(r'link', LinkViewSet)

urlpatterns = [
    path('', include(router.urls))
]