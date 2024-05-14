from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.validators import validate_admin_update_user, validate_create_user_form

from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithNames,
)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    A custom view that extends TokenObtainPairView to add
    user data to the token response.
    """

    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post"]

    @permission_classes([permissions.IsAuthenticated])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        current_user = super().get_object()
        serialized_data = UserSerializerWithNames(current_user, many=False).data
        return Response(serialized_data)

    @permission_classes([permissions.IsAdminUser])
    def create(self, request, *args, **kwargs):
        data = request.data
        errors = validate_create_user_form(data)
        if errors:
            return Response({"detail": errors}, status=400)
        new_user = User()

        new_user.first_name = data.get("first_name")
        new_user.last_name = data.get("last_name")
        new_user.email = data.get("email")
        new_user.username = data.get("username")
        new_user.password = data.get("password")
        new_user.image = data.get("image")
        new_user.set_password(new_user.password)
        try:
            new_user.save()
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})
        return Response(data)

    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = request.data
        errors = validate_admin_update_user(data)
        if errors:
            return Response({"detail": errors}, status=400)
        current_user = super().get_object()
        current_user.first_name = data.get("first_name", current_user.first_name)
        current_user.last_name = data.get("last_name", current_user.last_name)
        current_user.image = data.get("image", current_user.image)
        current_user.save()
        serialized_data = UserSerializerWithNames(current_user, many=False).data
        return Response(serialized_data)

    @action(
        detail=False, methods=["POST"], permission_classes=[permissions.IsAuthenticated]
    )
    def logout(self, request):
        data = {"detail": "User was logged out."}
        return Response(data)

    @action(detail=False, methods=["POST"], permission_classes=[permissions.AllowAny])
    def session(self, request):
        user = request.user
        serialized_user = UserSerializer(user, many=False).data
        return Response(serialized_user)
