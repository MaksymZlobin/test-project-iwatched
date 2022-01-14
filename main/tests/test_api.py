import factory
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from main.api.serializers import (
    FilmDetailSerializer,
    RateSerializer,
    UserFilmsListSerializer,
    CommentCreateSerializer,
)
from main.constants import FIVE, TWO
from main.models import Comment, Rate
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

    def test_logged_in_user_create_comment(self):
        payload_data = {
            'film': self.film.id,
            'author': self.user.id,
            'text': 'test_text',
        }
        url = reverse('comment', args=(self.film.id,))

        response = self.client.post(url, payload_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, payload_data)

    def test_anonymous_user_create_comment(self):
        created_data = {
            'film': self.film.id,
            'text': 'test_text',
        }
        url = reverse('comment', args=(self.film.id,))
        expected_data = CommentCreateSerializer().data

        response = self.client.post(url, created_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], expected_data['author'])


class CreateUpdateRateAPITestCase(APITestCase):
    def setUp(self):
        self.film = FilmFactory()
        self.user = CustomUserFactory()
        self.token = Token.objects.create(user=self.user)
        self.value = FIVE
        self.new_value = TWO

    def test_create_film_rate_logged_in_user(self):
        payload_data = {
            'value': self.value,
        }
        url = reverse('rate', kwargs={'film_id': self.film.id, })
        expected_data = {'user': self.user.id, 'film': self.film.id, 'value': self.value}
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Rate.objects.filter(user=self.user, film=self.film, value=self.value).count(), 1)

    def test_create_film_rate_anonymous_user(self):
        payload_data = {
            'value': self.value,
        }
        url = reverse('rate', kwargs={'film_id': self.film.id, })

        response = self.client.post(url, payload_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_film_rate_logged_in_user_invalid_data(self):
        payload_data = {
            'value': factory.Faker('word'),
        }
        url = reverse('rate', kwargs={'film_id': self.film.id, })
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_film_rate_logged_in_user(self):
        existing_rate = RateFactory(user=self.user, film=self.film, value=self.value)
        payload_data = {
            'value': self.new_value,
        }
        url = reverse('rate', args=(self.film.id,))
        expected_data = {'user': self.user.id, 'film': self.film.id, 'value': self.new_value}
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        existing_rate.refresh_from_db()
        self.assertEqual(existing_rate.value, self.new_value)

    def test_update_film_rate_logged_in_user_invalid_data(self):
        existing_rate = RateFactory(user=self.user, film=self.film, value=self.value)
        payload_data = {
            'value': factory.Faker('word'),
        }
        url = reverse('rate', args=(self.film.id,))
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        existing_rate.refresh_from_db()
        self.assertEqual(existing_rate.value, self.value)


class AddFilmToListAPITestCase(APITestCase):
    def test_post_add_film_to_list(self):
        user = CustomUserFactory()
        print(user.films_lists.all())
        film = FilmFactory()
        token = Token.objects.create(user=user)
        url = reverse('add_to_list', args=(film.id, user.films_lists.first().id))
        self.client.force_login(user)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(token))
        print(user.films_lists.first().film.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(film in user.films_lists.first().film.all())