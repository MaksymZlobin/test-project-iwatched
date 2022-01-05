from unittest import TestCase

from main.api.serializers import FilmDetailSerializer
from main.constants import FIVE
from main.models import Film, CustomUser, Rate


class FilmDetailSerializerTestCase(TestCase):
    def test_get_rating_no_rates(self):
        film_1 = Film.objects.create(name='Test film 1', synopsis='testing 1')

        rating = FilmDetailSerializer(film_1).get_rating(film_1)

        self.assertEqual(rating, None)

    def test_get_rating_with_rates(self):
        user = CustomUser.objects.create(username='test', email='test@test.com', password='12345')
        film = Film.objects.create(name='Test film', synopsis='testing')
        Rate.objects.create(user=user, film=film, value=FIVE)

        rating = FilmDetailSerializer(film).get_rating(film)

        self.assertEqual(rating, FIVE)
