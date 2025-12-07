from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TrainerappModel(admin.ModelAdmin):
    list_display = ['id','title', 'description', 'student', 'trainer', 'status', 'created_at']


    