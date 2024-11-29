
from django.contrib import admin
from .models import Exercise, FoodEntry, WeeklySummary

# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {"fields": ["user"]}),
    (None, {"fields": ["day"]}),
    (None,{"fields": ["name"]}),
    #(None, {"fields": ["date"]}),
    (None, {"fields": ["duration"]}),
    (None, {"fields": ["calories_burned"]}),
    #(None, {"fields": ["total_time"]}),

]

class FoodEntryAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {"fields": ["user"]}),
    (None, {"fields": ["name"]}),
    (None, {"fields": ["date"]}),
    (None, {"fields": ["day"]}),
    (None, {"fields": ["calories"]}),
    (None, {"fields": ["meal_type"]}),
]
    

class WeeklySummaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user"]}),
        (None, {"fields": ["week_start_date"]}),
        (None, {"fields": ["total_calories_burned"]}),
        (None, {"fields": ["total_time_spent"]}),
        (None, {"fields": ["total_calories_eaten"]}),
        
    ]
    
        
    
    Sunday = [FoodEntryAdmin, ExerciseAdmin]
    Monday = [FoodEntryAdmin, ExerciseAdmin]
    Tuesday = [FoodEntryAdmin, ExerciseAdmin]
    Wednesday = [FoodEntryAdmin, ExerciseAdmin]
    Thursday = [FoodEntryAdmin, ExerciseAdmin]
    Friday = [FoodEntryAdmin, ExerciseAdmin]
    Saturday = [FoodEntryAdmin, ExerciseAdmin]

admin.site.register(FoodEntry, FoodEntryAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(WeeklySummary, WeeklySummaryAdmin)