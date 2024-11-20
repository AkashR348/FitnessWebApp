from django.contrib import admin

from .models import Exercise, WeeklySummary, FoodEntry


# Register your models here.
class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user"]}),
        (None, {"fields": ["day"]}),
        (None, {"fields": ["title"]}),
        (None, {"fields": ["name"]}),
        (None, {"fields": ["duration"]}),
        (None, {"fields": ["calories_burned"]}),
        (None, {"fields": ["start_time"]}),
        (None, {"fields": ["end_time"]}),
        (None, {"fields": ["date"]})
    ]

class FoodEntryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user"]}),
        (None, {"fields": ["day"]}),
        (None, {"fields": ["meal_type"]}),
        (None, {"fields": ["calories"]}),
        (None, {"fields": ["time_eaten"]}),
        (None, {"fields": ["date"]})
    ]

class WeeklySummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user"]}),
        (None, {"fields": ["week_start_date"]}),
        (None, {"fields": ["total_calories_burned"]}),
        (None, {"fields": ["total_time_spent"]}),
        (None, {"fields": ["total_calories_eaten"]})
    ]
    Sunday = [FoodEntryAdmin, ExerciseAdmin]
    Monday = [FoodEntryAdmin, ExerciseAdmin]
    Tuesday = [FoodEntryAdmin, ExerciseAdmin]
    Wednesday = [FoodEntryAdmin, ExerciseAdmin]
    Thursday = [FoodEntryAdmin, ExerciseAdmin]
    Friday = [FoodEntryAdmin, ExerciseAdmin]
    Saturday = [FoodEntryAdmin, ExerciseAdmin]

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(FoodEntry,FoodEntryAdmin)
admin.site.register(WeeklySummary,WeeklySummaryAdmin)
