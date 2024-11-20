from django import forms
from .models import Exercise, FoodEntry
from .models import Exercise, FoodEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

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
        

class GoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['goal_calories_burned', 'goal_calories_eaten', 'goal_workout_duration']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['goal_calories_burned', 'goal_calories_eaten', 'goal_workout_duration']:
            if cleaned_data[field] < 0:
                raise forms.ValidationError(f"{field.replace('_', ' ').capitalize()} must be non-negative.")
        return cleaned_data