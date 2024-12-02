import calendar
from datetime import datetime, timedelta
from time import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import OneToOneField, SET_NULL
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercise, FoodEntry
from django.contrib.auth import login
from .forms import SignUpForm, ExerciseForm
from .models import UserProfile, Exercise, FoodEntry
from .forms import GoalForm
from django.contrib.auth import login, update_session_auth_hash
import logging


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

    return render(request, 'fitness_app/exercise.html', { 'week_data': week_data })

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

    return render(request, 'fitness_app/food.html', { 'week_food_data':week_food_data})

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
def summary_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('fitness_app:summary_view')  # Redirect to avoid re-posting on refresh
    else:
        form = GoalForm(instance=user_profile)

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
        'user_profile': user_profile,
        'form': form
    }
    return render(request, 'fitness_app/summary.html', context)

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

def create_exercise(request):
    if request.method == 'POST':
        print(f"Received date in create_exercise: {request.POST['date']}")
        date = datetime.strptime(request.POST["date"],"%Y-%m-%d")
        day = calendar.weekday(date.year,date.month,date.day)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        Exercise.objects.create(user = request.user,
                                date= date.date(),
                                day= days[day],
                                name=request.POST["name"],
                                duration=request.POST["duration"],
                                calories_burned=request.POST["calories_burned"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def create_foodentry(request):
    if request.method == 'POST':
        date = datetime.strptime(request.POST["date"],"%Y-%m-%d")
        day = calendar.weekday(date.year,date.month,date.day)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        FoodEntry.objects.create(user = request.user,
                                date= request.POST["date"],
                                day= days[day],
                                meal_type=request.POST["meal_type"],
                                calories=request.POST["calories"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def fetch_exercise(request):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        print(f"Received date in fetch_exercise: {date_str}")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            exercises = Exercise.objects.filter(user=request.user, date=date)
            data = []
            for exercise in exercises:
                data.append({
                    'name': exercise.name,
                    'duration': exercise.duration,
                    'date': exercise.date,
                    'calories_burned': exercise.calories_burned
                })
            return JsonResponse({'exercises': data})
        except (ValueError, TypeError):
            return JsonResponse({'exercises': []})
    return HttpResponseBadRequest('Invalid request method')

@login_required
def fetch_food(request):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        print(f"Received date in fetch_food: {date_str}")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            food_entries = FoodEntry.objects.filter(user=request.user, date=date)
            data = []
            for entry in food_entries:
                data.append({
                    'name': entry.name,
                    'calories': entry.calories,
                    'date': entry.date,
                    'meal_type': entry.meal_type
                })
            return JsonResponse({'food_entries': data})
        except (ValueError, TypeError):
            return JsonResponse({'food_entries': []})
    return HttpResponseBadRequest('Invalid request method')


#     if request.method == 'POST':
#         UserProfile.objects.create(user = OneToOneField(request.user,on_delete=SET_NULL),
#                                    goal_calories_burned = request.POST["goal_calories_burned"],
#                                    goal_calories_eaten = request.POST["goal_calories_eaten"],
#                                    goal_workout_duration = request.POST["goal_workout_duration"])
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
