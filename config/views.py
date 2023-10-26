from django.shortcuts import render

from books.models import BookReview


def landing_page(request):
    return render(request, 'landing.html')


def home_page(request):
    books_review = BookReview.objects.all().order_by('-created_at')
    context = {
        'books_review': books_review
    }
    return render(request, 'home.html', context)