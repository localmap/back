from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    offset_query_param = 'offset'
    max_limit = 100

    def get_offset(self, request):
        offset = super().get_offset(request)
        return offset - 1 if offset > 0 else 0

    def get_paginated_response(self, data):
        current_page = int(self.offset) + 1
        limit = int(self.limit)
        total = int(self.count)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'currentPage': current_page,
            'totalPages': total // limit + (1 if total % limit > 0 else 0),
            'results': data
        })