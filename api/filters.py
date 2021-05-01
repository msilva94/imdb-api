from rest_framework import filters


class MinLengthSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        if all(len(term) < 3 for term in search_terms):
            return queryset.none()
        return super().filter_queryset(request, queryset, view)


class MovieOrderingFilter(filters.OrderingFilter):
    def get_default_ordering(self, view):
        search = view.request.query_params.get('search', None)
        if search:
            return ['-year', 'title']
        return super().get_default_ordering(view)
