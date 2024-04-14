from django.db.models.functions import RowNumber
from django.db.models import F, Window

from django.views.generic import TemplateView

from posts.models import Post

from .models import About, FAQ

from .utils import DataMixin


class HomePageView(DataMixin, TemplateView):
    template_name = 'main/index.html'
    title_page = 'YourBlog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        window = Window(
            expression=RowNumber(),
            partition_by=[F('category__name')],
            order_by=[F('time_update').desc()]
        )
        posts = Post.published.annotate(row_number=window).order_by('category__name')
        posts = posts.filter(row_number__lte=4).select_related('category', 'author')

        posts_by_category = {}
        for post in posts:
            posts_by_category.setdefault(post.category, []).append(post)

        context.update(
            {
                'posts_by_category': posts_by_category,
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
    title_page = 'FAQ'
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
