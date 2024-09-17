from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 2  # Количество элементов на одной странице
    page_size_query_param = 'page_size'  # Параметр для изменения количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице
