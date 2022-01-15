import factory
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from main.api.serializers import FilmDetailSerializer
from main.constants import FIVE, TWO
from main.models import Rate
from main.tests.factories import (
    FilmFactory,
    GenreFactory,
    CustomUserFactory,
    RateFactory,
)


class FilmsListAPITestCase(APITestCase):
    def setUp(self):
        self.film_1 = FilmFactory()
        self.film_2 = FilmFactory()
        self.user = CustomUserFactory()
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

    def test_get_films_order_by_rating(self):
        RateFactory(user=self.user, film=self.film_1, value=FIVE)
        RateFactory(user=self.user, film=self.film_2, value=TWO)
        url = reverse('films') + f'?ordering=-film_rating'
        expected_data = FilmDetailSerializer([self.film_1, self.film_2, ], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class CommentCreateAPITestCase(APITestCase):
    def setUp(self):
        self.film = FilmFactory()
        self.user = CustomUserFactory()
        self.comment = 'test text'
        self.token = Token.objects.create(user=self.user)
        self.invalid_comment = None

    def test_logged_in_user_create_comment(self):
        payload_data = {
            'text': self.comment,
        }
        url = reverse('comment', kwargs={'film_id': self.film.id, })
        expected_data = {'film': self.film.id, 'author': self.user.id, 'text': self.comment}
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_anonymous_user_create_comment(self):
        payload_data = {
            'text': self.comment,
        }
        url = reverse('comment', kwargs={'film_id': self.film.id, })
        expected_data = {'film': self.film.id, 'author': None, 'text': self.comment}

        response = self.client.post(url, payload_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_logged_in_user_create_comment_invalid_data(self):
        url = reverse('comment', kwargs={'film_id': self.film.id, })
        self.client.force_login(self.user)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
        url = reverse('rate', kwargs={'film_id': self.film.id, })
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
        url = reverse('rate', kwargs={'film_id': self.film.id, })
        self.client.force_login(self.user)

        response = self.client.post(url, payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        existing_rate.refresh_from_db()
        self.assertEqual(existing_rate.value, self.value)


class AddFilmToListAPITestCase(APITestCase):
    def setUp(self):
        self.film = FilmFactory()
        self.user_1 = CustomUserFactory()
        self.user_2 = CustomUserFactory()
        self.token_1 = Token.objects.create(user=self.user_1)
        self.token_2 = Token.objects.create(user=self.user_2)

    def test_post_add_film_to_list(self):
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        expected_data = {
            'message': f'Film {self.film.id} added to list {self.user_1.films_lists.first().id} successfully!',
        }
        self.client.force_login(self.user_1)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertTrue(self.film in self.user_1.films_lists.first().film.all())

    def test_post_add_film_to_list_invalid_film_data(self):
        url = reverse('add_to_list', kwargs={
            'film_id': 999999999,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        self.client.force_login(self.user_1)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_move_film_from_list_to_another_list(self):
        self.user_1.films_lists.get(id=2).film.add(self.film)
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        self.client.force_login(self.user_1)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.film in self.user_1.films_lists.first().film.all())
        self.assertFalse(self.film in self.user_1.films_lists.get(id=2).film.all())

    def test_post_add_film_to_user_films_list_with_another_user(self):
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        self.client.force_login(self.user_2)

        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_add_film_to_list_with_anonymous_user(self):
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_film_from_list(self):
        self.user_1.films_lists.first().film.add(self.film)
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        expected_data = {
            'message': f'Film {self.film.id} removed from list {self.user_1.films_lists.first().id} successfully!',
        }
        self.client.force_login(self.user_1)

        response = self.client.delete(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertFalse(self.film in self.user_1.films_lists.first().film.all())

    def test_delete_film_from_list_without_film(self):
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        expected_data = {
            'message': f'Film {self.film.id} not found in list {self.user_1.films_lists.first().id}!',
        }
        self.client.force_login(self.user_1)

        response = self.client.delete(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)
        self.assertFalse(self.film in self.user_1.films_lists.first().film.all())

    def test_delete_film_from_users_films_list_with_another_user(self):
        self.user_1.films_lists.first().film.add(self.film)
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        self.client.force_login(self.user_2)

        response = self.client.delete(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.film in self.user_1.films_lists.first().film.all())

    def test_delete_film_from_users_films_list_with_anonymous_user(self):
        self.user_1.films_lists.first().film.add(self.film)
        url = reverse('add_to_list', kwargs={
            'film_id': self.film.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(self.film in self.user_1.films_lists.first().film.all())


class UserFilmsListsPrivateStatusAPITestCase(APITestCase):
    def setUp(self):
        self.user_1 = CustomUserFactory()
        self.user_2 = CustomUserFactory()
        self.token_1 = Token.objects.create(user=self.user_1)
        self.token_2 = Token.objects.create(user=self.user_2)
        self.payload_data = {'private': False}

    def test_get_user_films_list_with_another_user(self):
        url = reverse('private', kwargs={
            'user_id': self.user_1.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })
        self.client.force_login(self.user_2)

        response = self.client.get(url, HTTP_AUTHORIZATION='Token {}'.format(self.token_2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_films_list_with_anonymous_user(self):
        url = reverse('private', kwargs={
            'user_id': self.user_1.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_films_list_private_status_update(self):
        url = reverse('private', kwargs={
            'user_id': self.user_1.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        self.client.force_login(self.user_1)

        response = self.client.patch(url, self.payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token_1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['private'], False)

    def test_patch_user_films_list_private_status_update_with_another_user(self):
        url = reverse('private', kwargs={
            'user_id': self.user_1.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        self.client.force_login(self.user_2)

        response = self.client.patch(url, self.payload_data, HTTP_AUTHORIZATION='Token {}'.format(self.token_2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user_1.films_lists.first().private, True)

    def test_patch_user_films_list_private_status_update_with_anonymous_user(self):
        payload_data = {'private': False}
        url = reverse('private', kwargs={
            'user_id': self.user_1.id,
            'films_list_id': self.user_1.films_lists.first().id,
        })

        response = self.client.patch(url, payload_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.user_1.films_lists.first().private, True)

