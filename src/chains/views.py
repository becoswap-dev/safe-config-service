from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Chain
from .serializers import ChainSerializer


class ChainsListView(ListAPIView):
    serializer_class = ChainSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.max_limit = 100
    pagination_class.default_limit = 10
    queryset = Chain.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["relevance", "name"]
    ordering = [
        "relevance",
        "name",
    ]


class ChainsDetailView(RetrieveAPIView):
    serializer_class = ChainSerializer
    queryset = Chain.objects.all()

    @swagger_auto_schema(
        operation_id="Get chain by id"
    )  # type: ignore[misc] # Untyped decorator makes function "get" untyped
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)


class ChainsDetailViewByShortName(RetrieveAPIView):
    lookup_field = "short_name"
    serializer_class = ChainSerializer
    queryset = Chain.objects.all()

    @swagger_auto_schema(
        operation_id="Get chain by shortName",
        operation_description="Warning: `shortNames` may contain characters that need to be URL encoded (i.e.: whitespaces)",  # noqa E501
    )  # type: ignore[misc] # Untyped decorator makes function "get" untyped
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
