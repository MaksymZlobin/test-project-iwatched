from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from main.models import Film, FilmsList, CustomUser, Comment, Franchise, Genre, Rate


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ['name', ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FilmDetailSerializer(serializers.ModelSerializer):
    franchise = FranchiseSerializer(required=False)
    genre = GenreSerializer(required=False, many=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'synopsis', 'genre', 'poster', 'release_date', 'franchise']


class FilmsListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=True)
    film = FilmDetailSerializer(required=True, many=True)

    class Meta:
        model = FilmsList
        fields = ['id', 'type', 'user', 'film', 'private']


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(required=False)
    film = FilmDetailSerializer(required=True)

    class Meta:
        model = Comment
        fields = ['id', 'film', 'author', 'text', 'date']


class RateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=True)
    film = FilmDetailSerializer(required=True)

    class Meta:
        model = Rate
        fields = ['id', 'user', 'film', 'value']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': "Password fields don't match!"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
