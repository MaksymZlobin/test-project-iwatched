# Constants for storing rate values

ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5

VALUES_CHOICES = (
    (ONE, 'one star'),
    (TWO, 'two stars'),
    (THREE, 'three stars'),
    (FOUR, 'four stars'),
    (FIVE, 'five stars'),
)

# Constants for storing film list types

PLANNED_TYPE = 1
WATCHED_TYPE = 2
DROPPED_TYPE = 3

FILM_LIST_TYPES = (
    (PLANNED_TYPE, 'planned'),
    (WATCHED_TYPE, 'watched'),
    (DROPPED_TYPE, 'dropped'),
)