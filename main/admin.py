from django.contrib import admin
from main.models import Film, CustomUser, Comment, Franchise, Genre, FilmsList, Rate
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'synopsis', 'franchise', 'release_date')


@admin.register(FilmsList)
class FilmsListAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'private')


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'film', 'value')


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email', 'id')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'film', 'author', 'text')


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
