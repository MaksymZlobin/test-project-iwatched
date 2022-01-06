from unittest import TestCase

from main.api.serializers import FilmDetailSerializer
from main.constants import FIVE
from main.tests.factories import FilmFactory, RateFactory


class FilmDetailSerializerTestCase(TestCase):
    def test_get_rating_no_rates(self):
        film_1 = FilmFactory()

        rating = FilmDetailSerializer(film_1).get_rating(film_1)

        self.assertEqual(rating, None)

    def test_get_rating_with_rates(self):
        rate = RateFactory()

        rating = FilmDetailSerializer(rate.film).get_rating(rate.film)

        self.assertEqual(rating, FIVE)

