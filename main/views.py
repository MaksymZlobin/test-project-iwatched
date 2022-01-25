from django.views.generic import ListView, TemplateView

from main.models import Film


class FilmsListView(ListView):
    template_name = 'main/films_list.html'
    model = Film
    queryset = Film.objects.order_by('-id')


class AboutView(TemplateView):
    template_name = 'main/about.html'
