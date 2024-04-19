from django.views.generic import TemplateView

from .models import Main, About, FAQ
from .utils import DataMixin


class HomePageView(DataMixin, TemplateView):
    template_name = 'main/index.html'
    model = Main
    title_page = 'YourBlog'
    context_object_name = 'main'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main = Main.objects.first()
        context.update(
            {
                'main': main
            }
        )
        return context


class AboutPageView(DataMixin, TemplateView):
    template_name = 'main/about.html'
    model = About
    title_page = 'О сайте'
    context_object_name = 'about'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about = About.objects.first()
        context.update(
            {
                'about': about
            }
        )
        return context


class FAQPageView(DataMixin, TemplateView):
    template_name = 'main/faq.html'
    model = FAQ
    title_page = 'FAQs'
    context_object_name = 'faq'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faq = FAQ.objects.first()
        context.update(
            {
                'faq': faq
            }
        )
        return context
