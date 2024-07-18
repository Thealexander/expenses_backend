from django.urls import path
from expenseslist_app.api.views import ExpenseList, ExpenseDetails

urlpatterns = [
    path("list/", ExpenseList.as_view(), name="expenses-list"),
    path("<int:pk>/", ExpenseDetails.as_view(), name="expense-details"),
]
