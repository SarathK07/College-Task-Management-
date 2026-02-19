from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ("id","username","role")
    

