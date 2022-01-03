from rest_framework.permissions import BasePermission

from main.models import FilmsList


class IsAnonymousUser(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsCurrentUserByUserId(BasePermission):

    def has_permission(self, request, view):
        is_current_user_by_user_id = view.kwargs.get('user_id') == request.user.id
        return request.user.is_authenticated and is_current_user_by_user_id


class IsCurrentUserByFilmsListId(BasePermission):

    def has_permission(self, request, view):
        films_list_user = FilmsList.objects.get(id=view.kwargs.get('films_list_id')).user
        is_current_user_by_films_list_id = films_list_user == request.user
        return request.user.is_authenticated and is_current_user_by_films_list_id
