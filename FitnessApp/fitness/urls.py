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
]
