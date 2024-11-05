from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercise, FoodEntry, WeeklySummary
from .forms import ExerciseForm, FoodEntryForm  # Assuming you have forms for these models
from django.contrib.auth import login
from .forms import SignUpForm


# Publicly accessible pages
def exercise_page(request):
    exercises = Exercise.objects.all()
    return render(request, 'fitness_app/exercise.html', {'exercises': exercises})

def food_entry_page(request):
    food_entries = FoodEntry.objects.all()
    return render(request, 'fitness_app/food.html', {'food_entries': food_entries})

def weekly_summary_page(request):
    summaries = WeeklySummary.objects.all()
    return render(request, 'fitness_app/summary.html', {'summaries': summaries})

# Views requiring login for certain actions
@login_required
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('fitness_app:exercise_page')
    else:
        form = ExerciseForm()
    return render(request, 'fitness_app/create_exercise.html', {'form': form})

@login_required
def create_food_entry(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.save()
            return redirect('fitness_app:food_entry_page')
    else:
        form = FoodEntryForm()
    return render(request, 'fitness_app/create_food_entry.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after successful signup
            return redirect('fitness_app:exercise_page')  # Redirect to a page after signup
    else:
        form = SignUpForm()
    return render(request, 'fitness_app/signup.html', {'form': form})