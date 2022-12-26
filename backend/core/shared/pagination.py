from typing import Type

from rest_framework.pagination import PageNumberPagination


def page_number_pagination_factory(
    page_size: int = None,
    max_page_size: int = None,
    page_size_query_param: str = "page_size"
) -> Type[PageNumberPagination]:
    class PaginationClass(PageNumberPagination):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.page_size = page_size
            self.max_page_size = max_page_size
            self.page_size_query_param = page_size_query_param

    return PaginationClass


def limit_offset_pagination_factory(
    default_limit: int = None,
    max_limit: int = None,
    limit_query_param: str = "limit",
    offset_query_param: str = "offset"
) -> Type[PageNumberPagination]:
    class PaginationClass(PageNumberPagination):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.default_limit = default_limit
            self.max_limit = max_limit
            self.limit_query_param = limit_query_param
            self.offset_query_param = offset_query_param

    return PaginationClass
