from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.api.serializers import FilmDetailSerializer
from main.tests.factories import FilmFactory, GenreFactory


class FilmsListAPITestCase(APITestCase):
    def test_get(self):
        film_1 = FilmFactory()
        film_2 = FilmFactory()
        url = reverse('films')
        expected_data = FilmDetailSerializer([film_1, film_2], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_filter_genre(self):
        genre_name = 'action'
        film_1 = FilmFactory()
        film_2 = FilmFactory()
        film_1.genre.add(GenreFactory(name=genre_name))
        url = reverse('films') + f'?genre={genre_name}'
        expected_data = FilmDetailSerializer([film_1, ], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class RegisterAPITestCase(APITestCase):
    # TODO def test_create
    pass


class ProfileAPITestCase(APITestCase):
    # TODO IsCurrentUserByUserId
    pass


class CommentCreateAPITestCase(APITestCase):
    # TODO def create
    pass


class CreateUpdateRateAPITestCase(APITestCase):
    # TODO def post
    pass


class AddFilmToListAPITestCase(APITestCase):
    # TODO def post
    # TODO def delete
    pass


class PrivateStatusAPITestCase(APITestCase):
    # TODO IsCurrentUserByFilmsListId
    pass
