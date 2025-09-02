# books/views.py
import requests
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Review, Recommendation
from .serializers import BookSerializer, ReviewSerializer, RecommendationSerializer
from .permissions import AdminOrReadOnly  # ✅ make sure this file exists




class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["title", "author", "genre"]
    search_fields = ["title", "author", "genre"]
    permission_classes = [AdminOrReadOnly]

    # 🔹 Get book recommendations by genre
    @action(detail=True, methods=["get"])
    def recommendations(self, request, pk=None):
        book = self.get_object()
        recs = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:5]
        serializer = self.get_serializer(recs, many=True)
        return Response(serializer.data)

    # 🔹 Search books from Google Books API
    @action(detail=False, methods=["get"])
    def search_external(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)

        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch from Google Books"}, status=500)

        data = response.json()
        results = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            results.append({
                "external_id": item.get("id"),
                "title": volume_info.get("title"),
                "author": ", ".join(volume_info.get("authors", [])),
                "genre": ", ".join(volume_info.get("categories", [])) if "categories" in volume_info else "Unknown",
                "cover_image": volume_info.get("imageLinks", {}).get("thumbnail"),
            })
        return Response(results)

    # 🔹 Import external book into local DB (Admins only)
    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def import_external(self, request):
        external_id = request.data.get("external_id")
        if not external_id:
            return Response({"error": "external_id is required"}, status=400)

        url = f"https://www.googleapis.com/books/v1/volumes/{external_id}"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch book"}, status=500)

        item = response.json()
        volume_info = item.get("volumeInfo", {})

        book, created = Book.objects.get_or_create(
            external_id=external_id,
            defaults={
                "title": volume_info.get("title"),
                "author": ", ".join(volume_info.get("authors", [])),
                "genre": ", ".join(volume_info.get("categories", [])) if "categories" in volume_info else "Unknown",
                "cover_image": volume_info.get("imageLinks", {}).get("thumbnail"),
            },
        )

        return Response(BookSerializer(book).data, status=201 if created else 200)


# ✅ New Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically attach logged-in user to review
        serializer.save(user=self.request.user)

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
