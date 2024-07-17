from rest_framework import serializers
from expenseslist_app.models import Finance
from datetime import datetime
from django.core.exceptions import ValidationError


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = [
            "id",
            "description",
            "transaction_type",
            "amount",
            "execution_date",
            "payment_method",
            "support_document",
            "status",
            "created_by",
        ]

    def validate_description(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Description must be at least 5 characters long."
            )
        return value

    def validate_execution_date(self, value):
        if value < datetime(2024, 1, 1).date():
            raise serializers.ValidationError(
                "Execution date cannot be before January 1, 2024."
            )
        return value

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        # Redondear a dos decimales
        return round(value, 2)

    def validate_support_document(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB
        allowed_formats = ["application/pdf", "image/jpeg", "image/jpg", "image/png"]

        if value.size > max_size:
            raise serializers.ValidationError("Support document must not exceed 5 MB.")

        if value.content_type not in allowed_formats:
            raise serializers.ValidationError(
                "Support document must be in PDF, JPEG, JPG, or PNG format."
            )

        return value

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.transaction_type = validated_data.get(
            "transaction_type", instance.transaction_type
        )
        instance.amount = validated_data.get("amount", instance.amount)
        instance.execution_date = validated_data.get(
            "execution_date", instance.execution_date
        )
        instance.payment_method = validated_data.get(
            "payment_method", instance.payment_method
        )
        instance.support_document = validated_data.get(
            "support_document", instance.support_document
        )
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


# serilializer mode
""" 
class FinanceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=255)
    transaction_type = serializers.CharField(max_length=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    execution_date = serializers.DateField()
    payment_method = serializers.CharField(max_length=2)
    support_document = serializers.FileField(required=False)
    status = serializers.BooleanField()
"""


##aca termina comentario
