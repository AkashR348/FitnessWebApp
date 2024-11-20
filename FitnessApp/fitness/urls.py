from django.template.defaulttags import url
from django.urls import path, include
from . import views

app_name = 'fitness_app'

urlpatterns = [
    path("", views.weekly_summary_page, name="index"),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('exercise/create/', views.create_exercise, name='create_exercise'),  # Use the correct path here
    path('exercise/view/', views.view_exercise, name='view_exercise'), # For viewing exercises
    path('exercise/', views.exercise_page, name='exercise_page'),
    path('food/', views.food_page, name='food_page'),
    path('summary/', views.weekly_summary_page, name='summary_page'),
    path('create_food_entry/', views.create_food_entry, name='create_food_entry'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/change_password/', views.change_password, name='change_password'),
]
