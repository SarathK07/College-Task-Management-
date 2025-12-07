from django.urls import path
from .views import (
    TrainerStudentListView,
    AssignTaskView,
    StudentTaskListView,
    MarkTaskCompleteView
)
#wfvdvd
urlpatterns = [
    path('trainer/students/', TrainerStudentListView.as_view()),
    path('trainer/assign-task/', AssignTaskView.as_view()),
    path('trainer/student/<int:student_id>/tasks/', StudentTaskListView.as_view()),
    path('trainer/task/<int:task_id>/', MarkTaskCompleteView.as_view()),
]
