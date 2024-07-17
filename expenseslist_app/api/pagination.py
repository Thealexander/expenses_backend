from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ExpensesPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "p"
    page_size_query_param = "size"
    max_page_size = 10
    last_page_strings = "end"


class ExpensesLOPagination(LimitOffsetPagination):
    default_limit = 1
