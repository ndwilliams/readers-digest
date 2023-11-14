from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_reviews_created")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews_created")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    comment = models.CharField(max_length=300)
                             