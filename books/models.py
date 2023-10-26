from django.db import models
from django.utils import timezone

from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    book_image = models.ImageField(default='default_book.jpg', upload_to='media-files/books')

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"BOOK NAME: {self.book}\n " \
               f"BOOK AUTHOR: {self.author}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"STAR: {self.stars_given}  COMMENT: {self.comment}"


class Likes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_likes')
    book = models.ForeignKey(BookReview, on_delete=models.CASCADE, related_name='review_likes')