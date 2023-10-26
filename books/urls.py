from django.urls import path
from .views import ListView, DetailView, AddReviewView, EditReviewView, DeleteReviewView, DeleteView, AuthorDetailView, UserDetailView
app_name = 'books'
urlpatterns = [
    path('', ListView.as_view(), name='list'),
    path('<int:id>/', DetailView.as_view(), name='detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='review'),
    path('<int:book_id>/reviews/<int:review_id>/edit/', EditReviewView.as_view(), name='edit-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/confirm/', DeleteReviewView.as_view(), name='delete-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', DeleteView.as_view(), name='delete'),
    path('author/<int:author_id>/', AuthorDetailView.as_view(), name='about_author'),
    path('user/<str:username>', UserDetailView.as_view(), name='user_detail')
#    path('<int:book_id>/reviews/<int:review_id>/like/', like, name='review_like'),
]
