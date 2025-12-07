from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_TRAINER = "trainer"
    ROLE_STUDENT = "student"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_TRAINER, "Trainer"),
        (ROLE_STUDENT, "Student"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

