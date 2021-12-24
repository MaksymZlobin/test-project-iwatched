from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from main.api.api_views import FilmsListAPIView, FilmDetailAPIView, RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('films/', FilmsListAPIView.as_view(), name='films'),
    path('films/<int:film_id>/', FilmDetailAPIView.as_view(), name='film'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
