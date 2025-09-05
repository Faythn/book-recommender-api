from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r"", BookViewSet, basename="book")   # no "books"
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("books/", include(router.urls)),   # prefix here instead
]

