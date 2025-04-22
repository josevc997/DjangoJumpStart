from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

router = routers.SimpleRouter()
router.register(r"group", views.GroupViewSet, basename="group")
router.register(r"permission", views.PermissionViewSet, basename="permission")
router.register(r"", views.UserViewSet, basename="custom-auth")


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
