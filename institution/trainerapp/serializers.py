from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    trainer_username = serializers.CharField(source='trainer.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'student',
            'student_username',
            'trainer',
            'trainer_username',
            'status',
            'created_at',
            'submission'
        ]
        read_only_fields = ['trainer', 'status']
