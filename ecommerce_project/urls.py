"""URL configuration for ecommerce_project project.

This is the real URLconf living at the repository top-level. It routes
requests to the `shop` application and includes media serving during
development.
"""

from typing import List, Union

from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from django.contrib import admin  # type: ignore
from django.urls import include, path  # type: ignore

# Import URL types used for typing the `urlpatterns` variable so mypy
# understands that the list can contain both resolvers and patterns.
from django.urls.resolvers import URLPattern, URLResolver

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
