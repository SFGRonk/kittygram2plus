
from rest_framework.pagination import PageNumberPagination

class CatsPagination(PageNumberPagination):
    page_size = 20
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'response': data
        })