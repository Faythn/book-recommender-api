from django.core.management.base import BaseCommand
from books.models import Book, Review
from django.contrib.auth.models import User
import random
import requests

class Command(BaseCommand):
    help = "Seed database with books from Google Books API and reviews"

    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

    def handle(self, *args, **kwargs):
        # 1. Create sample users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f"user{i+1}",
                defaults={'email': f"user{i+1}@example.com"}
            )
            user.set_password("password123")
            user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS("✅ Sample users created."))

        # 2. Fetch books from Google Books API
        search_terms = ["programming", "self-help", "fiction", "fantasy", "business"]
        books = []

        for term in search_terms:
            params = {"q": term, "maxResults": 5}  # fetch 5 books per term
            response = requests.get(self.GOOGLE_BOOKS_API_URL, params=params)
            data = response.json()

            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                title = volume_info.get("title", "No Title")
                authors = ", ".join(volume_info.get("authors", ["Unknown Author"]))
                genre = ", ".join(volume_info.get("categories", ["Uncategorized"]))
                external_id = item.get("id")
                cover_image = volume_info.get("imageLinks", {}).get("thumbnail", "")

                book, created = Book.objects.get_or_create(
                    external_id=external_id,
                    defaults={
                        "title": title,
                        "author": authors,
                        "genre": genre,
                        "cover_image": cover_image,
                    },
                )
                if created:
                    books.append(book)
                    self.stdout.write(self.style.SUCCESS(f"Added book: {title}"))


        # 3. Create random reviews for all books and users
        for book in books:
            for user in users:
                Review.objects.get_or_create(
                    book=book,
                    user=user,
                    rating=random.randint(1, 5),
                    comment=f"Review by {user.username} for {book.title}"
                )

        self.stdout.write(self.style.SUCCESS("✅ Sample reviews added!"))
        self.stdout.write(self.style.SUCCESS("🎉 Database seeding complete!"))


