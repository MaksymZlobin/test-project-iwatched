from django.urls import path
from main import views

urlpatterns = [
    path('films/', views.FilmsListView.as_view(), name='films'),
]