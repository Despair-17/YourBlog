from django.shortcuts import render

menu = [
    {'title': 'О сайте', 'slug': '#'},
    {'title': 'FAQ', 'slug': '#'},
    {'title': 'Начни свой блог', 'slug': '#'},
]


def index(request):
    context = {
        'title': 'YourBlog',
        'menu': menu,
    }
    return render(request, 'posts/index.html', context)
