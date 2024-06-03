from typing import Any

from blog.settings.base import CACHE_TTL_FCH

from django.core.cache import cache
from django.forms import Form
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm
from .models import About, FAQ, Main
from .tasks import send_feedback_email
from .utils import DataMixin


class HomePageView(DataMixin, TemplateView):
    template_name = 'main/index.html'
    model = Main
    title_page = 'YourBlog'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cache_key = 'main_obj'
        main = cache.get(cache_key)

        if not main:
            main = Main.objects.first()
            cache.set(cache_key, main, CACHE_TTL_FCH)

        context['main'] = main
        return context


class AboutPageView(DataMixin, TemplateView):
    template_name = 'main/about.html'
    model = About
    title_page = 'О сайте'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cache_key = 'about_obj'
        about = cache.get(cache_key)

        if not about:
            about = About.objects.first()
            cache.set(cache_key, about, CACHE_TTL_FCH)

        context['about'] = about
        return context


class FAQPageView(DataMixin, TemplateView):
    template_name = 'main/faq.html'
    model = FAQ
    title_page = 'FAQs'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cache_key = 'faq'
        faq = cache.get(cache_key)

        if not faq:
            faq = FAQ.objects.first()
            cache.set(cache_key, faq, CACHE_TTL_FCH)

        context['faq'] = faq
        return context


class ContactView(DataMixin, FormView):
    template_name = 'main/contact.html'
    title_page = 'Обратная связь'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form: Form) -> HttpResponse:
        send_feedback_email.delay(
            form.cleaned_data['name'],
            form.cleaned_data['email'],
            form.cleaned_data['message'],
        )
        return super().form_valid(form)


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'status': 'OK'})
