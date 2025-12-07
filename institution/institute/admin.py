# from django.contrib import admin
# from .models import User

# # Register your models her


# class UserAdmin(admin.ModelAdmin):
#         list_display = ["id", "username", "email", "role", "first_name", "last_name"]


# admin.site.register(User)


from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ("id","username", "email", "first_name", "last_name", "role", "is_staff")
    

