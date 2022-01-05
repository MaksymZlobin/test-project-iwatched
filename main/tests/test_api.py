from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.api.serializers import FilmDetailSerializer
from main.models import Film


class FilmsListAPITestCase(APITestCase):
    def test_get(self):
        film_1 = Film.objects.create(name='Test film 1', synopsis='testing 1')
        film_2 = Film.objects.create(name='Test film 2', synopsis='testing 2')
        url = reverse('films')
        expected_data = FilmDetailSerializer([film_1, film_2], many=True).data

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

