from rest_framework import serializers
from django.contrib.auth.models import User
from user_app.models import Account
from django.contrib import auth


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Account
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "password doesnt match"})

        if Account.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "email. already registered"})

        account = Account.objects.create_user(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            password=self.validated_data["password"],
        )
        account.set_password = self.validated_data["password"]
        account.phone_number = self.validated_data["phone_number"]

        # account.set_password(password)
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "date_joined",
            "last_login",
            "is_admin",
            "is_staff",
            "is_active",
            "is_superadmin",
        ]
