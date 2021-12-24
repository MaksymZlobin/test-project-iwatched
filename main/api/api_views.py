from django.contrib.auth import login, authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.api.permissions import IsAnonymousUser
from main.api.serializers import FilmDetailSerializer, RegisterSerializer
from main.models import Film, FilmsList, CustomUser, Comment, Franchise, Genre, Rate


class FilmsListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [AllowAny, ]

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
    lookup_url_kwarg = 'film_id'


class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        token, created = Token.objects.get_or_create(user=user)
        if user:
            login(request, user)
        return Response(data={'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'User Logged out successfully!'}, status=status.HTTP_200_OK)

