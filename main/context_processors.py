from typing import Any

from blog.settings.base import CACHE_TTL_FCH, CACHE_TTL_NFCH

from django.http import HttpRequest

from .utils import menu


def get_menu(request: HttpRequest) -> dict[str, Any]:
    return {'menu': menu}


def get_cache_ttl(request: HttpRequest) -> dict[str, Any]:
    return {'cache_ttl_fch': CACHE_TTL_FCH, 'cache_ttl_nfch': CACHE_TTL_NFCH}
