from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    """
    A custom view that extends TokenObtainPairView to add
    user data to the token response.
    """

    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        data = {"detail": 'Method "POST" not allowed.'}
        return Response(data)

    def update(self, request, *args, **kwargs):
        data = {"detail": 'Method "POST" not allowed.'}
        return Response(data)

    @action(detail=False, methods=["POST"])
    def logout(self, request):
        data = {"detail": "User was logged out."}
        return Response(data)

    @action(detail=False, methods=["POST"])
    def session(self, request):
        user = request.user
        serialized_user = UserSerializer(user, many=False).data
        return Response(serialized_user)
