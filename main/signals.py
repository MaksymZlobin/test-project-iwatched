from django.db.models.signals import post_save
from django.dispatch import receiver

from main.constants import FILM_LIST_TYPES
from main.models import CustomUser, FilmsList


@receiver(post_save, sender=CustomUser)
def create_list_post_save(sender, instance, created, **kwargs):
    if created:
        for list_type in FILM_LIST_TYPES:
            FilmsList.objects.create(type=list_type[0], user=instance)
