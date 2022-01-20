from django.contrib.auth import login, authenticate
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.api.permissions import IsAnonymousUser, IsCurrentUserByUserId, IsCurrentUserByFilmsListId
from main.api.serializers import (
    FilmDetailSerializer,
    RegisterSerializer,
    ProfileSerializer,
    CommentCreateSerializer,
    RateSerializer,
    UserFilmsListUpdateSerializer,
)
from main.models import Film, FilmsList, CustomUser, Comment, Rate


class FilmsListAPIView(ListAPIView):
    queryset = Film.objects.all().annotate(film_rating=Avg('rates__value'))
    serializer_class = FilmDetailSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['film_rating', ]

    def get_queryset(self):
        qs = self.queryset.all()
        genre = self.request.query_params.get('genre')
        if genre:
            for genre_name in genre.split(','):
                qs = qs.filter(genre__name=genre_name)
                if not qs:
                    break
        return qs


class FilmDetailAPIView(RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_url_kwarg = 'film_id'


class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        token, created = Token.objects.get_or_create(user=user)
        if user:
            login(request, user)
        return Response(data={'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'User Logged out successfully!'}, status=status.HTTP_200_OK)


class ProfileAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'user_id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        return [IsCurrentUserByUserId(), ]


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.is_authenticated:
            data['author'] = request.user.id
        data['film'] = self.kwargs.get('film_id')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUpdateRateAPIView(APIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        data['film'] = self.kwargs.get('film_id')
        serializer = self.serializer_class(data=data)
        rates_list = self.queryset.filter(user=data['user'], film=data['film'])
        if rates_list.count() > 1:
            return Response(data={'message': 'More than one value!'}, status=status.HTTP_400_BAD_REQUEST)
        if rates_list:
            rate = rates_list.first()
            serializer = self.serializer_class(rate, data={'value': data['value']}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFilmToListAPIView(APIView):
    queryset = Film.objects.all()
    permission_classes = [IsCurrentUserByFilmsListId, ]

    def get_film_and_list(self, **kwargs):
        film_id = kwargs.get('film_id')
        films_list_id = kwargs.get('films_list_id')
        film = get_object_or_404(self.queryset, id=film_id)
        films_list = get_object_or_404(FilmsList, id=films_list_id)
        return film, films_list

    def post(self, request, *args, **kwargs):
        film, films_list = self.get_film_and_list(**kwargs)
        films_list.film.add(film)
        user_lists = request.user.films_lists.all().exclude(id=films_list.id)
        for user_list in user_lists:
            user_list.film.remove(film)
        return Response(
            data={'message': f'Film {film.id} added to list {films_list.id} successfully!'},
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        film, films_list = self.get_film_and_list(**kwargs)
        if film in films_list.film.all():
            films_list.film.remove(film)
            return Response(
                data={'message': f'Film {film.id} removed from list {films_list.id} successfully!'},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'message': f'Film {film.id} not found in list {films_list.id}!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class PrivateStatusAPIView(UpdateAPIView):
    queryset = FilmsList.objects.all()
    permission_classes = [IsCurrentUserByFilmsListId, ]
    serializer_class = UserFilmsListUpdateSerializer
    lookup_url_kwarg = 'films_list_id'
