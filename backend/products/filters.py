from rest_framework.filters import BaseFilterBackend

class UserProductsFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)