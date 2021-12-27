from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from main.api.api_views import (
    FilmsListAPIView,
    FilmDetailAPIView,
    RegisterAPIView,
    LogoutAPIView,
    ProfileAPIView,
    CommentCreateAPIView,
)

urlpatterns = [
    path('films/', FilmsListAPIView.as_view(), name='films'),
    path('films/<int:film_id>/', FilmDetailAPIView.as_view(), name='film'),
    path('films/<int:film_id>/create-comment', CommentCreateAPIView.as_view(), name='comment'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/<int:user_id>/', ProfileAPIView.as_view(), name='profile'),
]
