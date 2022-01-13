import factory

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.api.serializers import (
    FilmDetailSerializer,
    RateSerializer,
    UserFilmsListSerializer,
    CommentCreateSerializer,
)
from main.models import Comment
from main.tests.factories import (
    FilmFactory,
    GenreFactory,
    CommentFactory,
    CustomUserFactory,
    RateFactory,
    FilmsListFactory,
)


class FilmsListAPITestCase(APITestCase):
    def setUp(self):
        self.film_1 = FilmFactory()
        self.film_2 = FilmFactory()
        self.genre_name = 'action'

    def test_get(self):
        url = reverse('films')
        expected_data = FilmDetailSerializer([self.film_1, self.film_2], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_filter_genre(self):
        self.film_1.genre.add(GenreFactory(name=self.genre_name))
        url = reverse('films') + f'?genre={self.genre_name}'
        expected_data = FilmDetailSerializer([self.film_1, ], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class CommentCreateAPITestCase(APITestCase):
    def setUp(self):
        self.film = FilmFactory()
        self.user = CustomUserFactory()

    def test_user_create_comment(self):
        url = reverse('comment', args=(self.film.id,))
        created_data = {
            'film': self.film.id,
            'author': self.user.id,
            'text': 'test_text',
        }
        expected_data = CommentCreateSerializer(data=created_data).initial_data

        response = self.client.post(url, created_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_anonymous_user_create_comment(self):
        url = reverse('comment', args=(self.film.id,))
        created_data = {
            'film': self.film.id,
            'text': 'test_text',
        }
        expected_data = CommentCreateSerializer().data

        response = self.client.post(url, created_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], expected_data['author'])

# class CreateUpdateRateAPITestCase(APITestCase):
#     def test_create_rate(self):
#         url = reverse('rate', kwargs={'film_id': self.rate_1.film_id})
#         expected_data = RateSerializer(self.rate_dict_1).data
#
#         response = self.client.post(url, self.rate_dict_1)
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, expected_data)
#
#
# class AddFilmToListAPITestCase(APITestCase):
#     def setUp(self):
#         self.films_list = FilmsListFactory()
#
#     def test_get_film_and_list(self):
#         url = reverse('add_to_list', kwargs={'film_id': self.films_list.film_id, 'films_list_id': self.films_list.id})
#         expected_data = UserFilmsListSerializer([self.films_list, ], many=True).data
#
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, expected_data)
#
# TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use film.set() instead.


