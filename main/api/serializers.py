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


class FilmDetailSerializer(serializers.ModelSerializer):
    franchise = FranchiseSerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()
    franchise_films = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'name', 'synopsis', 'genre', 'poster', 'release_date', 'franchise', 'franchise_films', 'rating']

    def get_rating(self, film):
        if film.rating:
            return round(film.rating, 1)

    def get_franchise_films(self, obj):
        if obj.franchise:
            franchise_films = {}
            for film in obj.franchise.films.all():
                franchise_films[film.id] = film.name
            return franchise_films


class UserFilmsListSerializer(serializers.ModelSerializer):
    film = FilmDetailSerializer(many=True, required=False)

    class Meta:
        model = FilmsList
        fields = ['id', 'type', 'user', 'film', 'private']


class UserFilmsListUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmsList
        fields = ['id', 'type', 'user', 'private']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['film', 'author', 'text']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['user', 'film', 'value']


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


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    films_lists = UserFilmsListSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'films_lists']
