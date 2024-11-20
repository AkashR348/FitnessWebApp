from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercise, FoodEntry, WeeklySummary
from django.contrib.auth import login
from .forms import SignUpForm
from django.http import JsonResponse
from .models import UserProfile, Exercise, FoodEntry
<<<<<<< HEAD
from django.contrib.auth.models import AnonymousUser
=======
>>>>>>> parent of 8442e54 (created the basic goal submission form)









# Publicly accessible 
@login_required
def exercise_page(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    week_data = {}

    if request.user.is_authenticated:
        # Fetch exercises for the logged-in user
        for day_date in dates_of_week:
            exercises = Exercise.objects.filter(user=request.user, date=day_date)
            total_time = sum(exercise.duration for exercise in exercises)
            total_calories = sum(exercise.calories_burned for exercise in exercises)
            week_data[day_date] = {
                'exercises': exercises,
                'total_time': total_time,
                'total_calories': total_calories,
            }
    else:
        # For anonymous users, provide empty data or a placeholder message
        for day_date in dates_of_week:
            week_data[day_date] = {
                'exercises': [],  # No exercises to show
                'total_time': 0,
                'total_calories': 0,
            }

    return render(request, 'fitness_app/exercise.html', {'week_data': week_data})

@login_required
def food_page(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    week_food_data = {}

    if request.user.is_authenticated:
        # Fetch food entries for each day of the week for the logged-in user
        for day_date in dates_of_week:
            food_entries = FoodEntry.objects.filter(user=request.user, date=day_date)

            # Calculate total calories per meal type and overall total
            meal_totals = {
                'breakfast': sum(entry.calories for entry in food_entries if entry.meal_type == 'breakfast'),
                'lunch': sum(entry.calories for entry in food_entries if entry.meal_type == 'lunch'),
                'dinner': sum(entry.calories for entry in food_entries if entry.meal_type == 'dinner'),
                'snack': sum(entry.calories for entry in food_entries if entry.meal_type == 'snack'),
            }
            total_calories = sum(meal_totals.values())

            week_food_data[day_date] = {
                'food_entries': food_entries,
                'meal_totals': meal_totals,
                'total_calories': total_calories,
            }
    else:
        # For anonymous users, provide placeholder data
        for day_date in dates_of_week:
            week_food_data[day_date] = {
                'food_entries': [],  # No food entries to show
                'meal_totals': {
                    'breakfast': 0,
                    'lunch': 0,
                    'dinner': 0,
                    'snack': 0,
                },
                'total_calories': 0,
            }

    return render(request, 'fitness_app/food.html', {'week_food_data': week_food_data})





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








<<<<<<< HEAD
@login_required
def summary_view(request):
    if not request.user.is_authenticated:
        # For unauthenticated users, show a placeholder message or redirect to login
        return render(request, 'fitness_app/summary.html', {
            'summaries': [],
            'error': 'Please log in to view your summary.',
        })

    # Proceed for authenticated users
=======
def summary_view(request):
    # Ensure user profile exists or create one with default goals
>>>>>>> parent of 8442e54 (created the basic goal submission form)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    summaries = []
    for day in dates_of_week:
        exercises = Exercise.objects.filter(user=request.user, date=day)
        foods = FoodEntry.objects.filter(user=request.user, date=day)

        total_calories_burned = sum(exercise.calories_burned for exercise in exercises)
        total_time_spent = sum(exercise.duration for exercise in exercises)
        total_calories_eaten = sum(food.calories for food in foods)

        # Calculate progress as percentages of the user's goals
        progress_burned = min(100, (total_calories_burned / user_profile.goal_calories_burned) * 100)
        progress_time = min(100, (total_time_spent / user_profile.goal_workout_duration) * 100)
        progress_eaten = min(100, (total_calories_eaten / user_profile.goal_calories_eaten) * 100)

        summaries.append({
            'date': day,
            'total_calories_burned': total_calories_burned,
            'total_time_spent': total_time_spent,
            'total_calories_eaten': total_calories_eaten,
            'progress_burned': progress_burned,
            'progress_time': progress_time,
            'progress_eaten': progress_eaten,
        })

    context = {
        'summaries': summaries,
        'user_profile': user_profile
    }
    return render(request, 'fitness_app/summary.html', context)



@login_required
def profile(request):
    return render(request, 'fitness_app/profile.html')