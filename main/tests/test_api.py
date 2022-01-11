from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.api.serializers import FilmDetailSerializer, CommentCreateSerializer
from main.tests.factories import FilmFactory, GenreFactory, CommentFactory, CustomUserFactory


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


class CommentCreateAPITestCase(APITestCase):
    def test_post_create_comment(self):
        comment = CommentFactory()
        comment_dict = {
            'film': comment.film_id,
            'author': comment.author_id,
            'text': comment.text,
        }
        url = reverse('comment', kwargs={'film_id': comment.film_id})
        expected_data = CommentCreateSerializer(comment).data

        response = self.client.post(url, comment_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)
