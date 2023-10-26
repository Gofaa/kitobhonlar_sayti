from django.urls import path
from .views import BookReviewDetailApiView, BookReviewListApiView
app_name = 'api'
urlpatterns = [
    path('reviews/<int:id>/', BookReviewDetailApiView.as_view(), name='review-detail'),
    path('reviews/', BookReviewListApiView.as_view(), name='reviews')
]