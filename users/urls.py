from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogOutView, UpdateProfileView

app_name = "users"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', UpdateProfileView.as_view(), name='profile_edit'),
]