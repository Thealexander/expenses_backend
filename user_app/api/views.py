from django.contrib import auth
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.fields import NOT_READ_ONLY_REQUIRED
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer, AccountSerializer
from user_app.models import Account
from rest_framework.views import APIView


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def session_view(request):
    user = request.user
    try:
        account = Account.objects.get(email=user.email)
        serializer = AccountSerializer(account)
        data = serializer.data
        refresh = RefreshToken.for_user(account)
        data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(data)
    except Account.DoesNotExist:
        data = {"error": "User does not exist"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(
    [
        "POST",
    ]
)
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "Registration successfully"
            data["username"] = account.username
            data["email"] = account.email
            data["first_name"] = account.first_name
            data["last_name"] = account.last_name
            data["phone_number"] = account.phone_number

            # token = Token.objects.get(user=account).key
            # data['token'] = token

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data)

        else:
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["POST"])
def login_view(request):
    data = {}
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        account = auth.authenticate(email=email, password=password)
        if account is not None:
            data["response"] = "Login successfully"
            data["username"] = account.username
            data["email"] = account.email
            data["first_name"] = account.first_name
            data["last_name"] = account.last_name
            data["phone_number"] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data)
        else:
            data["error"] = "Wrong credentials"
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": getattr(user, 'phone_number', 'N/A')  # Ajusta según tus modelos
        }
        return Response(data)
