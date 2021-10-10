from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.http import JsonResponse

DEFAULT_PAGE=1
DEFAULT_PAGE_SIZE=5


class CustomPagination(PageNumberPagination):
    page= DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self,data):
        return JsonResponse({
            data[0]: data[1],
            'meta': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
             }

            },status=200)
            

        

