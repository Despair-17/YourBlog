from typing import Any

from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.core.mail import send_mail

from .forms import ContactForm
from .models import Main, About, FAQ
from .utils import DataMixin
from blog.settings.base import DEFAULT_FROM_EMAIL, CONTACT_EMAIL


class HomePageView(DataMixin, TemplateView):
    template_name = 'main/index.html'
    model = Main
    title_page = 'YourBlog'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        main = Main.objects.first()
        context['main'] = main
        return context


class AboutPageView(DataMixin, TemplateView):
    template_name = 'main/about.html'
    model = About
    title_page = 'О сайте'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        about = About.objects.first()
        context['about'] = about
        return context


class FAQPageView(DataMixin, TemplateView):
    template_name = 'main/faq.html'
    model = FAQ
    title_page = 'FAQs'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        faq = FAQ.objects.first()
        context['faq'] = faq
        return context


class ContactView(DataMixin, FormView):
    template_name = 'main/contact.html'
    title_page = 'Обратная связь'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        send_mail(
            subject='Новое сообщение обратной связи',
            message=f'Имя: {form.cleaned_data["name"]}\n'
                    f'Email: {form.cleaned_data["email"]}\n'
                    f'Сообщение: {form.cleaned_data["message"]}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[CONTACT_EMAIL],
        )
        return super().form_valid(form)
