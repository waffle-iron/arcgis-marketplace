from rest_framework import pagination
from rest_framework.settings import api_settings


class ArcgisOffsetPagination(api_settings.DEFAULT_PAGINATION_CLASS):
    page_size = api_settings.PAGE_SIZE

    def get_page_size(self, request):
        if isinstance(self, pagination.LimitOffsetPagination):
            return self.get_limit(request)
        return super().get_page_size(request)

    def get_offset(self, request):
        if isinstance(self, pagination.PageNumberPagination):
            page_number = request.query_params.get(self.page_query_param, 1)

            try:
                page_number = int(page_number)
            except (TypeError, ValueError):
                page_number = 1

            return (page_number - 1) * self.page_size

        elif isinstance(self, pagination.LimitOffsetPagination):
            return self.get_offset(request)

        elif isinstance(self, pagination.CursorPagination):
            cursor = self.decode_cursor(request)

            if cursor is not None:
                return cursor[0]

        return 0
