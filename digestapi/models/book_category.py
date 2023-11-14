from django.db import models

class BookCategory(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="categories_of_this_book")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="books_with_this_category")