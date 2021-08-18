from rest_framework import filters, mixins, viewsets

from .permissions import IsAdmin, IsReadOnly


class MixinsViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdmin | IsReadOnly,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
