from typing import Any

from django.core.paginator import Page
from django.views.generic import ListView


class PaginatedListView(ListView):
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        return context
