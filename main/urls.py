from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    path('films/', views.FilmsListView.as_view(), name='films'),
]