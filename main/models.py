from django.contrib.auth.models import AbstractUser
from django.db import models

from main.constants import VALUES_CHOICES, FILM_LIST_TYPES


class Franchise(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=200)
    synopsis = models.TextField()
    genre = models.ManyToManyField(Genre, blank=True, related_name='films')
    poster = models.ImageField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.SET_NULL, related_name='films')

    def __str__(self):
        return f'{self.name} (object ID {self.id})'

    @property
    def rating(self):
        return self.rates.all().aggregate(models.Avg('value'))['value__avg']


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.email}'


class FilmsList(models.Model):
    type = models.IntegerField(choices=FILM_LIST_TYPES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='films_lists')
    film = models.ManyToManyField(Film, blank=True, related_name='films_lists')
    private = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'type']

    def __str__(self):
        return f'Films list by - {self.user}. Type: {self.type}'


class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment object ID {self.id}'


class Rate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rates')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='rates')
    value = models.IntegerField(choices=VALUES_CHOICES)

    class Meta:
        unique_together = ['user', 'film']

    def __str__(self):
        return f'{self.value} star(s) rate by {self.user} for {self.film}'
