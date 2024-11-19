from django import forms
from .models import Exercise, FoodEntry, UserProfile
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



class GoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['goal_calories_burned', 'goal_calories_eaten', 'goal_workout_duration']
        labels = {
            'goal_calories_burned': 'Calories Burned Goal',
            'goal_calories_eaten': 'Calories Eaten Goal',
            'goal_workout_duration': 'Workout Duration Goal (minutes)',
        }
        widgets = {
            'goal_calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal_calories_eaten': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal_workout_duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
