import factory
from faker import Factory

from main.constants import ONE, FIVE
from main.models import Film, CustomUser, Rate, Genre, Comment

faker = Factory.create()


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker('word')


class FilmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Film

    name = factory.Faker('word')
    synopsis = factory.Faker('sentence', nb_words=10)


# class FilmWithGenreFactory(FilmFactory):
#     genre = factory.SubFactory(GenreFactory)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('first_name')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username.lower())
    password = factory.Faker('password')


class RateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rate

    value = factory.Faker('random_int', min=ONE, max=FIVE)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('sentence', nb_words=5)
