from typing import Any

from django.http import HttpRequest

from .utils import menu


def get_menu(request: HttpRequest) -> dict[str, Any]:
    return {'menu': menu}
