from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Default auth URLs (login, logout, etc.)
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Custom /login/ path
    path('', include('fitness.urls')),  # Include your app's URLs
]
