from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission = models.TextField(blank=True, null=True)   # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
