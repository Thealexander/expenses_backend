from django.urls import path
from expenseslist_app.api.views import ExpensiveList, FinanceDetails

urlpatterns = [
    path("list/", ExpensiveList.as_view(), name="expensives-list"),
    path("<int:pk>", FinanceDetails.as_view(), name="finance-details"),
]
