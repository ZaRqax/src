from django_filters.rest_framework import DjangoFilterBackend


class FilterAPIMixin:
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)  # type: ignore
        return queryset
