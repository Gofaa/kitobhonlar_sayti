from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import landing_page, home_page

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home', home_page, name='home_page'),
    path("admin/", admin.site.urls),
    path('users/', include("users.urls")),
    path('books/',include('books.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
