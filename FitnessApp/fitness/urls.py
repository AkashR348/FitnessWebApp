from django.urls import path
from . import views

app_name = 'fitness_app'

urlpatterns = [
    path("", views.weekly_summary_page, name="index"),
    path('exercises/', views.exercise_page, name='exercise_page'),
    path('food/', views.food_entry_page, name='food_entry_page'),
    path('summary/', views.weekly_summary_page, name='summary_page'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('create_food_entry/', views.create_food_entry, name='create_food_entry'),
    path('signup/', views.signup, name='signup'),
    
]
