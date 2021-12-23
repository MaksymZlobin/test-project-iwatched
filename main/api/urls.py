from django.urls import path
from main.api.api_views import FilmsListAPIView, FilmDetailAPIView, RegisterAPIView

urlpatterns = [
    path('films/', FilmsListAPIView.as_view(), name='films'),
    path('films/<int:film_id>/', FilmDetailAPIView.as_view(), name='film'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
