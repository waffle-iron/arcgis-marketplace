from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response

from ... import models

from .. import mixins
from .. import permissions

from ..decorators import offset_pagination

from . import filters
from . import serializers


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'
    queryset = models.Account.objects.active()
    permission_classes = (
        permissions.IsStaffList,
        permissions.IsStaffOrSelf,
        permissions.Signed)

    serializer_class = serializers.AccountSerializer


class MeViewSet(mixins.ArcgisAPIMixin,
                mixins.ArcgisPaginationMixin,
                viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    def list(self, request, *args, **kwargs):
        return Response(self.account.me())

    @list_route(methods=['get'])
    def groups(self, request, *args, **kwargs):
        return Response(self.account.groups)

    @list_route(methods=['get'])
    @offset_pagination
    def items(self, request, *args, **kwargs):
        data = self.account.api.user_items(
            self.account.username,
            **request.pagination_params
        )
        return self.get_paginated_response(data, request)


class SelfViewSet(mixins.ArcgisAPIMixin,
                  mixins.ArcgisPaginationMixin,
                  viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    def list(self, request, *args, **kwargs):
        return Response(self.account.self())

    def get_self_response(self, resource, request, *args, **kwargs):
        data = getattr(self.account.api, "self_{}".format(resource))(
            **request.pagination_params
        )
        return self.get_paginated_response(data, request)

    @list_route(methods=['get'])
    @offset_pagination
    def roles(self, request, *args, **kwargs):
        return self.get_self_response('roles', request, *args, **kwargs)

    @list_route(methods=['get'])
    @offset_pagination
    def users(self, request, *args, **kwargs):
        return self.get_self_response('users', request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'
    queryset = models.Item.objects.active()
    permission_classes = (permissions.OwnItem, permissions.ReadOnlyOrSigned)
    serializer_class = serializers.ItemSerializer

    filter_class = filters.ItemFilter
    search_fields = ('title', 'description')
    ordering_fields = ('title', 'price', 'created')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.account)


class GroupViewSet(mixins.ArcgisAPIMixin,
                   mixins.ArcgisPaginationMixin,
                   viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    @offset_pagination
    def list(self, request, *args, **kwargs):
        data = self.account.api.groups(**request.pagination_params)
        return self.get_paginated_response(data, request)

    def create(self, request, *args, **kwargs):
        return Response(
            self.account.api.create_group(**request.data),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        return Response(self.account.api.group_detail(pk))

    def update(self, request, pk=None):
        return Response(self.account.api.update_group(pk, **request.data))

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.account.api.delete_group(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def add(self, request, pk=None):
        users = request.data.get('users')
        return Response(self.account.api.add_to_group(pk, users=users))

    @detail_route(methods=['post'])
    def invite(self, request, pk=None):
        return Response(self.account.api.invite_to_group(pk, **request.data))

    @detail_route(methods=['get'])
    @offset_pagination
    def items(self, request, pk=None):
        data = self.account.api.group_items(pk, **request.pagination_params)
        return self.get_paginated_response(data, request)

    @detail_route(methods=['post'])
    def config_map(self, request, pk=None):
        return Response(
            self.account.api.update_group(
                pk,
                sortField='title',
                sortOrder='asc'
            )
        )


class ItemViewSet(mixins.ArcgisAPIMixin,
                  mixins.ArcgisPaginationMixin,
                  viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    def create(self, request, *args, **kwargs):
        return Response(
            self.account.api.add_item(
                self.account.username,
                **request.data
            ),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        return Response(self.account.api.item_detail(pk))

    @detail_route(methods=['post'])
    def share(self, request, pk=None):
        groups = request.data.get('groups')
        return Response(self.account.api.share_item(pk, groups))
