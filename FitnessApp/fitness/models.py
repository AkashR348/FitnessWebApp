from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)  # Ex: "Monday", "Tuesday"
    title = models.CharField(max_length=100, blank=True, null=True)  # Optional title for the day (e.g., "Leg Day")
    name = models.CharField(max_length=100)  # Exercise name (e.g., "Running")
    duration = models.PositiveIntegerField()  # Duration in minutes
    calories_burned = models.PositiveIntegerField()  # Calories burned
    start_time = models.TimeField()  # Time the exercise started
    end_time = models.TimeField(blank=True, null=True)  # Calculated end time based on duration
    date = models.DateField(auto_now_add=True)  # Automatically stores the date when the entry was created

    def save(self, *args, **kwargs):
        # Automatically calculate end time based on start time and duration
        if self.start_time:
            end_time = (datetime.combine(datetime.today(), self.start_time) + timedelta(minutes=self.duration)).time()
            self.end_time = end_time
        super(Exercise, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.day} - {self.name} ({self.calories_burned} kcal)"

class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)  # Ex: "Monday", "Tuesday"
    meal_type = models.CharField(max_length=50)  # Meal type (e.g., "Breakfast", "Lunch")
    calories = models.PositiveIntegerField()  # Calories for the meal
    time_eaten = models.TimeField()  # Time the meal was eaten
    date = models.DateField(auto_now_add=True)  # Automatically stores the date when the entry was created

    def __str__(self):
        return f"{self.day} - {self.meal_type} ({self.calories} kcal)"

class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()  # The starting date of the week for this summary
    total_calories_burned = models.PositiveIntegerField(default=0)  # Total calories burned over the week
    total_time_spent = models.PositiveIntegerField(default=0)  # Total time spent exercising over the week (in minutes)
    total_calories_eaten = models.PositiveIntegerField(default=0)  # Total calories consumed over the week

    def __str__(self):
        return f"Week of {self.week_start_date} Summary for {self.user.username}"

