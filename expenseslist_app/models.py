from django.db import models
from user_app.models import Account

# from django.contrib.auth.models import User

# Create your models here.


class Finance(models.Model):
    INCOME = "IN"
    EXPENSE = "EX"
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    CREDITCARD = "CC"
    DEBITCARD = "DC"
    CASH = "CH"
    CREDIT = "C"
    PAYMENT_METHOD_CHOICES = [
        (CREDITCARD, "Credit Card"),
        (DEBITCARD, "Debit Card"),
        (CASH, "Cash"),
        (CREDIT, "Credit"),
    ]

    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    execution_date = models.DateField()
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES)
    support_document = models.FileField(upload_to="documents/", blank=True, null=True)
    status = models.BooleanField(default=True)  # True for "Saved", False for "Void"
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    # date_registered = models.DataTimeField(auto_add_now = true)
    # anulado
    class Meta:
        verbose_name = "Finance Record"
        verbose_name_plural = "Finance Records"

    def __str__(self):
        return f"{self.description} - {self.get_transaction_type_display()} - {self.amount}"
