from django.urls import path
from . import views

app_name = 'fitness_app'

urlpatterns = [
    path("", views.weekly_summary_page, name="index"),
    path('exercise/', views.exercise_page, name='exercise_page'),
    path('food/', views.food_page, name='food_page'),
    path('summary/', views.weekly_summary_page, name='summary_page'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    
]
