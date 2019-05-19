from django.contrib.auth.models import User

from rest_framework import serializers

from developer.models import Developer
from genre.models import Genre
from tag.models import Tag
from game.models import Game


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:users-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class DeveloperSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:developers-detail")

    class Meta:
        model = Developer
        fields = ('url', 'name')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:genres-detail")

    class Meta:
        model = Genre
        fields = ('url', 'name')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:tags-detail")

    class Meta:
        model = Tag
        fields = ('url', 'name')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:games-detail")
    developer = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest_api:developers-detail'
    )
    genre = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest_api:genres-detail'
    )
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='rest_api:tags-detail'
    )

    class Meta:
        model = Game
        fields = ('url', 'title', 'year', 'developer', 'genre', 'tags', 'image', 'to_be_rated')
