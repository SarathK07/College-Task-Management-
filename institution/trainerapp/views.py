from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

# Your serializers
from institute.serializers import UserReadSerializer 
from .serializers import TaskSerializer

# Your models
from .models import Task


User = get_user_model()


class TrainerStudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.role != 'trainer':
            raise PermissionDenied("Only trainers can access student list")

    def get(self, request):
        students = User.objects.filter(role='student')
        serializer = UserReadSerializer(students, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        })

class AssignTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.role != 'trainer':
            raise PermissionDenied("Only trainers can assign tasks")

    def post(self, request):
        data = request.data
        student_id = data.get("student_id")
        title = data.get("title")
        description = data.get("description", "")

        if not student_id or not title:
            return Response(
                {"message": "student_id and title are required"},
                status=400
            )

        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({"message": "Student not found"}, status=404)

        task = Task.objects.create(
            title=title,
            description=description,
            student=student,
            trainer=request.user
        )

        serializer = TaskSerializer(task)
        return Response({
            "status": "success",
            "message": "Task assigned",
            "data": serializer.data
        }, status=201)



class StudentTaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.role != 'trainer':
            raise PermissionDenied("Only trainers can view tasks")

    def get(self, request, student_id):
        tasks = Task.objects.filter(student_id=student_id)
        serializer = TaskSerializer(tasks, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        })



class MarkTaskCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.role != 'trainer':
            raise PermissionDenied("Only trainers can update task status")

    def patch(self, request, task_id):
        # Get the task assigned by this trainer
        try:
            task = Task.objects.get(id=task_id, trainer=request.user)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=404)

        # Get status from request body
        status_value = request.data.get("status")
        if status_value not in ["pending", "completed"]:
            return Response(
                {"message": "Invalid status. Must be 'pending' or 'completed'"},
                status=400
            )

        # Update task status
        task.status = status_value
        task.save()

        serializer = TaskSerializer(task)
        return Response({
            "status": "success",
            "message": f"Task status updated to '{status_value}'",
            "data": serializer.data
        })

