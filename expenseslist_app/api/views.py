# from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from expenseslist_app.api.pagination import ExpensesPagination
from expenseslist_app.api.serializers import FinanceSerializer
from expenseslist_app.models import Finance
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from expenseslist_app.api.permission import IsRecordUserOrReadOnly

# from django.http import Http404
# from expenseslist_app.api.permission import RecordUserOrReadOnly


# Usando APIView
class ExpensiveList(APIView):

    permission_classes = [IsRecordUserOrReadOnly, IsAuthenticated]
    pagination_class = ExpensesPagination

    def get(self, request):
        expensives = Finance.objects.all()
        serializer = FinanceSerializer(expensives, many=True)
        return Response(serializer.data)

    def post(self, request):
        de_serializer = FinanceSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceDetails(APIView):
    # permission_classes = [permissions.IsAuthenticated, RecordUserOrReadOnly]

    def get_object(self, pk):
        try:
            return Finance.objects.get(pk=pk)
        except Finance.DoesNotExist:
            return None

    def get(self, request, pk):
        details = self.get_object(pk)
        if details is None:
            return Response(
                {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = FinanceSerializer(details)
        return Response(serializer.data)

    def put(self, request, pk):
        details = self.get_object(pk)
        if details is None:
            return Response(
                {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
            )
        de_serializer = FinanceSerializer(details, data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        details = self.get_object(pk)
        if details is None:
            return Response(
                {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            details.delete()
            return Response({"resultado": True}, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response(
                {"error": "You do not have permission to delete this resource"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


##aca abajo es usando metodos sin APIView
""" @api_view(["GET", "POST"])
def expensive_list(request):
    if request.method == "GET":
        expensives = Finance.objects.all()
        serializer = FinanceSerializer(expensives, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        de_serializer = FinanceSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def finance_details(request, pk):
    try:
        details = Finance.objects.get(pk=pk)
    except Finance.DoesNotExist:
        return Response(
            {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = FinanceSerializer(details)
        return Response(serializer.data)

    if request.method == "PUT":
        de_serializer = FinanceSerializer(details, data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        try:
            details.delete()
            return Response({"resultado": True}, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response(
                {"error": "You do not have permission to delete this resource"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ) """
