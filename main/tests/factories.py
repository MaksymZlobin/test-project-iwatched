import factory
from faker import Factory

from main.constants import FIVE

faker = Factory.create()


class FilmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Film'

    name = factory.Faker('word')
    synopsis = factory.Faker('sentence', nb_words=10)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.CustomUser'

    username = factory.Faker('first_name')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username.lower())
    password = factory.Faker('password')


class RateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Rate'

    user = factory.SubFactory(CustomUserFactory)
    film = factory.SubFactory(FilmFactory)
    value = FIVE


