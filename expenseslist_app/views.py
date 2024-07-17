""" from django.shortcuts import render
from expenseslist_app.models import Finance
from django.http import JsonResponse

# Create your views here.


def expensive_list(request):
    expensives = Finance.objects.all()
    data = {"expensives": list(expensives.values())}

    return JsonResponse(data)


def finance_details(request, pk):
    details = Finance.objects.get(pk=pk)
    data = {
        "description": details.description,
        "transaction_type": details.transaction_type,
        "amount": details.amount,
        "execution_date": details.execution_date,
        "payment_method": details.payment_method,
        "support_document": details.support_document,
    }
    return JsonResponse(data)
"""