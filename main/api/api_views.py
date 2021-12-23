from django.contrib.auth import login, authenticate
from rest_framework import status, filters
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response

from main.api.permissions import IsAnonymousUser
from main.api.serializers import FilmDetailSerializer, RegisterSerializer
from main.models import Film, FilmsList, CustomUser, Comment, Franchise, Genre, Rate


class FilmsListAPIView(ListAPIView):
    """List of films"""
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer

    def get_queryset(self):
        qs = self.queryset.all()
        print(qs)
        genre = self.request.query_params.get('genre')
        print(genre)
        return qs.filter(genre__name=genre)


class FilmDetailAPIView(RetrieveAPIView):
    """Detail film"""
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    lookup_url_kwarg = 'film_id'


class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user:
            login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
