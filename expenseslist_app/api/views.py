# from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from expenseslist_app.api.pagination import ExpensesPagination
from expenseslist_app.api.serializers import ExpenceSerializer
from expenseslist_app.models import Expense
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from expenseslist_app.api.permission import IsRecordUserOrReadOnly

# from django.http import Http404
# from expenseslist_app.api.permission import RecordUserOrReadOnly


# Usando APIView
class ExpenseList(APIView):

    permission_classes = ([IsRecordUserOrReadOnly])
    #pagination_class = ExpensesPagination

    def get(self, request):
        # user = request.user
        # expenses = Expense.objects.filter(created_by=user, status=True)
        expenses = Expense.objects.filter(status=True)
        serializer = ExpenceSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        de_serializer = ExpenceSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetails(APIView):
    permission_classes = ([IsRecordUserOrReadOnly])

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return None

    def get(self, request, pk):
        details = self.get_object(pk)
        if details is None:
            return Response(
                {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExpenceSerializer(details)
        return Response(serializer.data)

    def put(self, request, pk):
        details = self.get_object(pk)
        if details is None:
            return Response(
                {"error": "Finance record not found"}, status=status.HTTP_404_NOT_FOUND
            )
        de_serializer = ExpenceSerializer(details, data=request.data)
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
