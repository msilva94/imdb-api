from rest_framework import filters


class MovieOrderingFilter(filters.OrderingFilter):
    def get_default_ordering(self, view):
        q = view.request.query_params.get('q', None)
        if q:
            return ['-year', 'title']
        return super().get_default_ordering(view)
