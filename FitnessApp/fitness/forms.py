from django import forms
from .models import Exercise, FoodEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['day', 'title', 'name', 'duration', 'calories_burned', 'start_time']

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['day', 'meal_type', 'calories', 'time_eaten']
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
