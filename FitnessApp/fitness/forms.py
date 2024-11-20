from django import forms
from .models import Exercise, FoodEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['day', 'name', 'duration', 'calories_burned', 'date']

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['day', 'meal_type', 'calories', 'time_eaten']
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class GoalForm(forms.Form):
    calories_burned_goal = forms.IntegerField()
    time_spent_goal = forms.IntegerField()
    calories_eaten_goal = forms.IntegerField()  
    class Meta:
        model = Goal
        fields = ['calories_burned_goal', 'time_spent_goal', 'calories _eaten_goal'] 
          
