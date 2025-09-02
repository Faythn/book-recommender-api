# Book Recommender API

## Project Overview
Django-based API for searching books, adding reviews, and getting recommendations using Google Books API.

## Features
- User Authentication (Sign up, Login, Logout)
- Book Search
- Reviews and Ratings
- Recommendations
- Save favorite books

## Setup
1. Clone the repo
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Seed database: `python manage.py seed_data`
6. Run server: `python manage.py runserver`

## API Endpoints
- `/api/users/register/`
- `/api/users/login/`
- `/api/books/search/?q=title`
- `/api/books/<id>/`
- `/api/reviews/create/`
- `/api/recommendations/`
