# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Django imports
from django.contrib.auth import get_user_model

# Your serializers
from trainerapp.serializers import TaskSerializer

# Your models
from trainerapp.models import Task

# Get your custom User model
User = get_user_model()

class StudentTaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.role != 'student':
            raise PermissionDenied("Only students can access their tasks")

    # View all tasks
    def get(self, request):
        tasks = Task.objects.filter(student=request.user)
        serializer = TaskSerializer(tasks, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        })

    # Submit task
    def post(self, request):
        task_id = request.data.get("task_id")
        submission = request.data.get("submission")

        if not task_id or not submission:
            return Response(
                {"message": "task_id and submission are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id, student=request.user)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=404)

        task.submission = submission
        task.status = 'submitted'
        task.save()

        return Response({
            "status": "success",
            "message": "Task submitted successfully"
        })

