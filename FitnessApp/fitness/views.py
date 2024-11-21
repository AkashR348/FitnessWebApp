from datetime import datetime, timedelta
from http.client import HTTPResponse
from tempfile import template

from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages

from .models import Exercise, FoodEntry, WeeklySummary
from .forms import ExerciseForm, FoodEntryForm  # Assuming you have forms for these models
from django.contrib.auth import login, update_session_auth_hash
from .forms import SignUpForm
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST






# Publicly accessible pages
def exercise_page(request):
    # Get today's date and the current week's dates
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]
    
    # Dictionary to hold exercises and summaries for each day
    week_data = {}
    for day_date in dates_of_week:
        exercises = Exercise.objects.filter(user=request.user, date=day_date)
        total_time = sum(exercise.duration for exercise in exercises)
        total_calories = sum(exercise.calories_burned for exercise in exercises)
        week_data[day_date] = {
            'exercises': exercises,
            'total_time': total_time,
            'total_calories': total_calories,
        }

    return render(request, 'fitness_app/exercise.html', {'week_data': week_data})

def food_page(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday as start of the week
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]
    
    week_food_data = {}
    for day_date in dates_of_week:
        food_entries = FoodEntry.objects.filter(user=request.user, date=day_date)
        meal_totals = {
            'breakfast': sum(entry.calories for entry in food_entries.filter(meal_type='breakfast')),
            'lunch': sum(entry.calories for entry in food_entries.filter(meal_type='lunch')),
            'dinner': sum(entry.calories for entry in food_entries.filter(meal_type='dinner')),
            'snack': sum(entry.calories for entry in food_entries.filter(meal_type='snack')),
        }
        total_calories = sum(meal_totals.values())
        week_food_data[day_date] = {
            'food_entries': food_entries,
            'meal_totals': meal_totals,
            'total_calories': total_calories,
        }

    return render(request, 'fitness_app/food.html', {'week_food_data': week_food_data})

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
            # Return JSON with the new exercise data
            return JsonResponse({
                'success': True,
                'exercise': {
                    'name': exercise.name,
                    'duration': exercise.duration,
                    'calories_burned': exercise.calories_burned,
                    'start_time': exercise.start_time.strftime('%H:%M') if exercise.start_time else "N/A",
                    'date': exercise.date.strftime('%Y-%m-%d')
                }
            })
    # Return error if form is invalid
    exercise = Exercise(form.fields[0],form.fields[1],form.fields[2],form.fields[3],form.fields[4],form.fields[5], form.fields[5]+form.fields[3], datetime.today())
    #context = exercise
    #return render(request, "exercise.html", exercise)
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

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

@login_required
def view_exercise(request):
    date_str = request.GET.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)
    
    # Query exercises for the specified date
    exercises = Exercise.objects.filter(user=request.user, date=date)
    
    # Prepare exercise data as a list of dictionaries
    exercise_data = [
        {
            'name': exercise.name,
            'duration': exercise.duration,
            'calories_burned': exercise.calories_burned,
            'start_time': exercise.start_time.strftime('%H:%M') if exercise.start_time else "N/A",
            'date': exercise.date.strftime('%Y-%m-%d')
        }
        for exercise in exercises
    ]
    
    return JsonResponse({'success': True, 'exercises': exercise_data})


@login_required
def profile(request):
    return render(request, 'fitness_app/profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  #Don't log user out
            #messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'fitness_app/change_password.html', {
        'form': form
    })