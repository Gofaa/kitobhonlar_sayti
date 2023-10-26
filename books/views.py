from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from users.models import CustomUser
from django.views.decorators.http import require_POST

import users.views
from .models import Book, BookReview, BookAuthor
from .forms import BookReviewForm
from django.contrib import messages


# Create your views here.


class ListView(View):
    def get(self, request):
        books = Book.objects.all().order_by("id")
        search_query = request.GET.get("q", "")
        if search_query:
            books = books.filter(title__icontains=search_query)
        paginator = Paginator(books, 4)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        context = {"page_obj": page_obj, "search_query": search_query}
        return render(request, "books/list.html", context)


class DetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        reviews = book.bookreview_set.all().order_by("-created_at")
        book_review = BookReviewForm()
        context = {"book_review": book_review, "book": book, "reviews": reviews}
        return render(request, "books/detail.html", context)


class AuthorDetailView(View):
    def get(self, request, author_id):
        author = BookAuthor.objects.get(id=author_id)
        context = {
            'author': author
        }
        return render(request, "books/author_detail.html", context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data["stars_given"],
                comment=review_form.cleaned_data["comment"],
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))
        context = {"review_form": review_form, "book": book}
        return render(request, "books/detail.html", context)


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        context = {"book": book, "review": review, "review_form": review_form}

        return render(request, "books/edit_review.html", context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(
            request,
            "books/edit_review.html",
            {"book": book, "review": review, "review_form": review_form},
        )


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        context = {"book": book, "review": review}
        return render(request, "books/delete_review.html", context)


class DeleteView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        messages.success(request, "Izohingiz o'chirildi!")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))


# def like(request, review_id, book_id):
#     book = Book.objects.get(id=book_id)
#     user = request.user
#     review = BookReview.objects.get(id=review_id)
#     current_likes = review.likes
#     liked = Likes.objects.filter(user=user, review=review).count()
#     if not liked:
#         liked = Likes.objects.create(user=user, review=review)
#         current_likes = current_likes + 1
#     else:
#         liked = Likes.objects.filter(user=user, review=review).delete()
#         current_likes = current_likes - 1
#
#     review.likes = current_likes
#     review.save()
#     return HttpResponseRedirect(reverse('books:detail', kwargs={"id":book.id}))


class UserDetailView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        context = {
            'user': user
        }
        return render(request, 'user_profile.html', context)
