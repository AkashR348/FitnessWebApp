from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercise, FoodEntry, WeeklySummary
from .forms import ExerciseForm, FoodEntryForm  # Assuming you have forms for these models
from django.contrib.auth import login
from .forms import SignUpForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST






# Publicly accessible pages
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

def weekly_summary_page(request):
    summaries = WeeklySummary.objects.all()
    return render(request, 'fitness_app/summary.html', {'summaries': summaries})







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



def view_exercise(request):
    print("work")
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