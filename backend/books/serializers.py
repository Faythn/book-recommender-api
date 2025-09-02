from rest_framework import serializers
from .models import Book, Review, Recommendation

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")  # ✅ shows username but not editable

    class Meta:
        model = Review
        fields = "__all__"  # or list explicitly: ["id", "book", "rating", "comment", "user", "created_at"]
        read_only_fields = ["user"]  # ✅ prevents clients from posting user manually

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = "__all__"
