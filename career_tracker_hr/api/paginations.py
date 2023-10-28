from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6


class StudentPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return data