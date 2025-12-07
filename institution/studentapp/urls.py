from django.urls import path
from .views import StudentTaskListView

urlpatterns = [
    path('student/tasks/', StudentTaskListView.as_view()),
]
