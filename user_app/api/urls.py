from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration_view, logout_view, login_view, session_view, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("login-app/", login_view, name="login-app"),
    path("register/", registration_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("session/", session_view, name="session"),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
