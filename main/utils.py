from typing import Any

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'FAQ', 'url_name': 'faq'},
    {'title': 'Посты по категориям', 'url_name': 'all_categories'}
]


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'memu' not in self.extra_context:
            self.extra_context['menu'] = menu

    @staticmethod
    def get_context_mixin(context: dict[str, Any], **kwargs) -> dict[str, Any]:
        context.update(kwargs)
        return context
