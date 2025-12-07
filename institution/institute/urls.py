from django.urls import path
from .views import (
    RegisterAPIView, LoginAPIView,
    TrainerView, TrainerDetailView, StudentDetailView, StudentView
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path('TrainerView/',TrainerView.as_view()),
    path('trainer/<int:pk>/', TrainerDetailView.as_view(), name='trainer-detail'),
    path('StudentView/', StudentView.as_view(), name='student-detail'),
    path('StudentDetailView/<int:pk>/', StudentDetailView.as_view(), name='Studentdetailview'),

]
