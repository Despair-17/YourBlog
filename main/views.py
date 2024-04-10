from django.views.generic import TemplateView
from posts.models import Posts

menu = [
    {'title': 'О сайте', 'slug': 'about'},
    {'title': 'FAQ', 'slug': 'faq'},
    {'title': 'Начни свой блог', 'slug': '#'},
]


class HomePageView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'YourBlog',
        'menu': menu,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
