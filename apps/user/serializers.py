from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer that adds user data to the token response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "image",
            "_id",
            "isAdmin",
            "is_active",
            "date_joined",
            "last_login",
        ]

    def get__id(self, obj: User):
        return obj.id

    def get_isAdmin(self, obj: User):
        return obj.is_staff

    def get_name(self, obj: User):
        name = f"{obj.first_name} {obj.last_name}"
        if name.strip() == "":
            name = obj.email
        return name.strip()


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "_id",
            "username",
            "email",
            "name",
            "isAdmin",
            "image",
            "token",
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class UserSerializerWithNames(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    groups = GroupSerializer(read_only=True, many=True)
    permissions = PermissionSerializer(
        read_only=True, many=True, source="user_permissions"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "name",
            "_id",
            "isAdmin",
            "is_active",
            "date_joined",
            "last_login",
            "image",
            "groups",
            "permissions",
        ]

    def get__id(self, obj: User):
        return obj.id

    def get_isAdmin(self, obj: User):
        return obj.is_staff

    def get_name(self, obj: User):
        name = f"{obj.first_name} {obj.last_name}"
        if name.strip() == "":
            name = obj.email
        return name.strip()

    # def get_image(self, obj: User):
    #     if obj.image:
    #         return obj.image.url
    #     return None
