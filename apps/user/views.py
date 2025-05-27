from django.contrib.auth.models import Group, Permission, PermissionsMixin
from rest_framework import (
    permissions,
    serializers,
    viewsets,
)
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.permissions import CustomPermission
from apps.user.validators import (
    validate_admin_update_user,
    validate_create_user_form,
)

from .models import User
from .serializers import (
    GroupSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithNames,
    PermissionSerializer,
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

    @permission_classes([CustomPermission])
    def list(self, request, *args, **kwargs):
        """
        List all users.
        """
        user = request.user
        if not user.is_superuser:
            queryset = User.objects.filter(is_superuser=False)
        else:
            queryset = self.get_queryset()
        serialized_data = UserSerializerWithNames(
            queryset, many=True, context={"request": request}
        ).data
        return Response(serialized_data)

    @permission_classes([CustomPermission])
    def retrieve(self, request, *args, **kwargs):
        current_user = super().get_object()
        serialized_data = UserSerializerWithNames(
            current_user, many=False, context={"request": request}
        ).data
        return Response(serialized_data)

    @permission_classes([CustomPermission])
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
        serialized_user = UserSerializerWithNames(new_user, many=False)
        return Response(serialized_user.data)

    @permission_classes([CustomPermission])
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


class GroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing group instances.
    """

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    http_method_names = ["get", "post", "put"]
    permission_classes = [CustomPermission]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing permission instances.
    """

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    http_method_names = ["get", "post", "put"]
    permission_classes = [CustomPermission]

    def update(self, request, pk=None):
        """
        Update user permissions.
        """
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"detail": "User not found."}, status=404)
        permissions = request.data.get("permissions", [])
        if not permissions:
            return Response({"detail": "No permissions provided."}, status=400)

        # Clear existing permissions
        user.user_permissions.clear()

        # Assign new permissions
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            user.user_permissions.add(permission)

        return Response({"detail": "Permissions updated successfully."})


class UserPermissionViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing user permission instances.
    """

    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.get_all_permissions()

    def list(self, request):
        """
        List all permissions for the authenticated user.
        """
        user = request.user
        permissions = user.get_all_permissions()
        permission_list = [
            permission_item.split(".")[1] for permission_item in permissions
        ]
        return Response(permission_list)


class UserGroupViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing user group instances.
    """

    serializer_class = GroupSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        user = self.request.user
        return user.groups.all()

    def update(self, request, pk=None):
        """
        Update user groups.
        """
        user = User.objects.get(pk=pk)
        if not user:
            return Response({"detail": "User not found."}, status=404)
        groups = request.data.get("groups", [])
        if not groups:
            return Response({"detail": "No groups provided."}, status=400)

        # Clear existing permissions
        if not isinstance(groups, list):
            return Response({"detail": "Groups must be a list."}, status=400)
        # Validate that all provided groups exist
        for group_name in groups:
            if not Group.objects.filter(name=group_name).exists():
                return Response(
                    {"detail": f"Group '{group_name}' does not exist."}, status=400
                )
        # Clear existing groups
        user.groups.clear()

        # Assign new groups
        for group_name in groups:
            group_instance = Group.objects.get(name=group_name)
            user.groups.add(group_instance)

        return Response({"detail": "Groups updated successfully."})
