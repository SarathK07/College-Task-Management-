from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from .serializers import UserReadSerializer, TrainerSerializer, StudentSerializer


User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Expected payload:
        {
          "username": "user1",
          "password": "strongpass123",
          "role": "trainer"    # or "student"  (admin NOT allowed)
        }
        All validation happens here.
        """
        data = request.data

        # Required fields
        username = data.get("username", "")
        password = data.get("password", "")
        role = data.get("role", "")

        errors = {}

        # username validation
        if not username or not isinstance(username, str) or username.strip() == "":
            errors["username"] = ["Username is required."]
        else:
            username = username.strip()
            if User.objects.filter(username__iexact=username).exists():
                errors.setdefault("username", []).append("Username already exists.")

        # password validation (example: min length 8)
        if not password or not isinstance(password, str):
            errors["password"] = ["Password is required."]
        else:
            if len(password) < 8:
                errors.setdefault("password", []).append("Password must be at least 8 characters long.")

        # role validation
        allowed_roles = {User.ROLE_TRAINER, User.ROLE_STUDENT}
        if not role or not isinstance(role, str):
            errors["role"] = ["Role is required."]
        else:
            role = role.strip().lower()
            if role not in allowed_roles:
                errors["role"] = [f"Role must be one of: {', '.join(sorted(allowed_roles))}."]
        # Disallow creating admin via this endpoint
        if role == User.ROLE_ADMIN:
            errors.setdefault("role", []).append("Cannot register as admin via this endpoint.")

        # If any errors, return them
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User(username=username, role=role)
        user.set_password(password)
        user.save()

        serializer = UserReadSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Expected payload:
        {
           "username": "user1",
           "password": "strongpass123"
        }
        All validation in view. Returns access and refresh tokens with role claim.
        """
        data = request.data
        username = data.get("username", "")
        password = data.get("password", "")

        errors = {}
        if not username or not isinstance(username, str) or username.strip() == "":
            errors["username"] = ["Username is required."]
        if not password or not isinstance(password, str):
            errors["password"] = ["Password is required."]

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        username = username.strip()
        user = authenticate(request, username=username, password=password)
        if user is None:
            # do not reveal whether username exists
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Create tokens and add role claim
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        refresh["username"] = user.username  # optional

        access = str(refresh.access_token)
        refresh_token = str(refresh)

        serializer = UserReadSerializer(user)
        return Response({
            "user": serializer.data,
            "tokens": {
                "access": access,
                "refresh": refresh_token
            }
        }, status=status.HTTP_200_OK)


class TrainerView(APIView):
    permission_classes = [IsAuthenticated]

    # ✅ correct place for role check
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not (request.user.is_superuser or request.user.role == 'admin'):
            raise PermissionDenied("Only admin users can access this API")

    def get(self, request):
        trainer_data = User.objects.filter(role='trainer')
        serializer = UserReadSerializer(trainer_data, many=True)
        return Response({
            "status": "success",
            "message": "fetched successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "trainer added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=400)



class TrainerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not (request.user.is_superuser or request.user.role == 'admin'):
            raise PermissionDenied("Only admin users can access this API")
    def get(self, request, pk):
        try:
            trainer = User.objects.get(id=pk, role='trainer')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Trainer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserReadSerializer(trainer)
        return Response({
            "status": "success",
            "message": "trainer fetched successfully",
            "data": serializer.data
        })

    def put(self, request, pk):
        try:
            trainer = User.objects.get(id=pk, role='trainer')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Trainer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TrainerSerializer(trainer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "trainer updated successfully",
                "data": serializer.data
            })

        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def patch(self, request, pk):
        try:
            trainer = User.objects.get(id=pk, role='trainer')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Trainer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TrainerSerializer(trainer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "trainer partially updated successfully",
                "data": serializer.data
            })

        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk):
        try:
            trainer = User.objects.get(id=pk, role='trainer')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Trainer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        trainer.delete()
        return Response(
            {"status": "success", "message": "trainer deleted successfully"},
            status=status.HTTP_200_OK
        )

class StudentView(APIView):
    permission_classes = [IsAuthenticated]

    # ✅ correct place for role check
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not (request.user.is_superuser or request.user.role == 'admin'):
            raise PermissionDenied("Only admin users can access this API")

    def get(self, request):
        student_data = User.objects.filter(role='student')
        serializer = UserReadSerializer(student_data, many=True)
        return Response({
            "status": "success",
            "message": "fetched successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "student added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=400)



class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not (request.user.is_superuser or request.user.role == 'admin'):
            raise PermissionDenied("Only admin users can access this API")
    def get(self, request, pk):
        try:
            student = User.objects.get(id=pk, role='student')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserReadSerializer(student)
        return Response({
            "status": "success",
            "message": "student fetched successfully",
            "data": serializer.data
        })

    def put(self, request, pk):
        try:
            student = User.objects.get(id=pk, role='trainer')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "student updated successfully",
                "data": serializer.data
            })

        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def patch(self, request, pk):
        try:
            student = User.objects.get(id=pk, role='student')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Trainer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "student partially updated successfully",
                "data": serializer.data
            })

        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk):
        try:
            student = User.objects.get(id=pk, role='student')
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()
        return Response(
            {"status": "success", "message": "student deleted successfully"},
            status=status.HTTP_200_OK
        )
