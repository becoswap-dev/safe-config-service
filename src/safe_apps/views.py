from typing import Any

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import SafeApp
from .serializers import SafeAppsResponseSerializer


class SafeAppsListView(ListAPIView):
    serializer_class = SafeAppsResponseSerializer
    pagination_class = None

    _swagger_network_id_param = openapi.Parameter(
        "chainId",
        openapi.IN_QUERY,
        description="Used to filter Safe Apps that are available on `chainId`",
        type=openapi.TYPE_INTEGER,
    )

    @method_decorator(cache_page(60 * 10, cache="safe-apps"))  # Cache 10 minutes
    @swagger_auto_schema(manual_parameters=[_swagger_network_id_param])  # type: ignore[misc]
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns a collection of Safe Apps (across different chains).
        Each Safe App can optionally include the information about the `Provider`
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[SafeApp]:
        queryset = SafeApp.objects.filter(visible=True)

        network_id = self.request.query_params.get("chainId")
        if network_id is not None and network_id.isdigit():
            queryset = queryset.filter(chain_ids__contains=[network_id])

        return queryset
