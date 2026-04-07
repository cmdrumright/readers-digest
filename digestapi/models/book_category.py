from django.db import models
from .book import Book
from .category import Category


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    # timestamp = models.DateTimeField()
