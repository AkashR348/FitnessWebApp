from django.urls import path
from . import views

app_name = 'fitness_app'

urlpatterns = [
    path("", views.summary_view, name="summary_page"),
    path('exercise/', views.exercise_page, name='exercise_page'),
    path('food/', views.food_page, name='food_page'),
    path('summary/', views.summary_view,name='summary_page'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/change_password/', views.change_password, name='change_password'),
    path('create_exercise', views.create_exercise, name='create_exercise'),
    path('create_foodentry', views.create_foodentry, name='create_foodentry'),
    path('fetch_exercise', views.fetch_exercise, name='fetch_exercise'),  # Updated to match the method name
    path('fetch_food', views.fetch_food, name='fetch_food'),  # Add the new URL pattern

    #path('create_goal', views.create_goal, name='create_goal')
]
