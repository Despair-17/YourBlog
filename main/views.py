from django.db.models.functions import RowNumber
from django.db.models import F, Window

from django.views.generic import TemplateView

from posts.models import Post, Category

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
