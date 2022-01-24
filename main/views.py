from django.http import HttpResponse
from django.views.generic import ListView

from main.models import Film


class FilmsListView(ListView):
    template_name = 'main/films_list.html'
    model = Film
    queryset = Film.objects.order_by('-id')
