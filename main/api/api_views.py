from django.contrib.auth import login, authenticate
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

from main.api.permissions import IsAnonymousUser, IsCurrentUser
from main.api.serializers import (
    FilmDetailSerializer,
    RegisterSerializer,
    ProfileSerializer,
    CommentCreateSerializer,
    RateSerializer,
)
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


class ProfileAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsCurrentUser, ]
    lookup_url_kwarg = 'user_id'


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
            rate.value = data['value']
            rate.save()
            return Response(data=self.serializer_class(instance=rate).data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
