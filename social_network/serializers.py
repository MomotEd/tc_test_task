import clearbit
from django.contrib.auth import get_user_model
from pyhunter import PyHunter
from django.conf import settings
from rest_framework import serializers

from .models import Post, Like


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'additional_data')

    @staticmethod
    def validate_email(value):
        # Use​ emailhunter.co​ ​for​ verifying​ email​ existence​ ​on​ ​signup
        py_hunter = PyHunter(settings.HUNTER_API_KEY)
        if settings.HUNTER_ENABLED and settings.HUNTER_API_KEY:
            if py_hunter.email_verifier(value).get('result') != 'undeliverable':
                return value
            raise serializers.ValidationError('An issue with email verification occures​')
        return value

    @staticmethod
    def collect_additional_data(response):
        if isinstance(response, dict):
            return "".join(["{}: {}; ".format(key, value)
                            for key, value in response.items()])

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        if settings.CLEARBIT_ENABLED and settings.CLEARBIT_API_KEY:
            clearbit.key = settings.CLEARBIT_API_KEY
            response = clearbit.Enrichment.find(email=user.email, stream=True)
            if response:
                additional_data = self.collect_additional_data(response)
                user.additional_data = additional_data
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'posts_count', 'likes_count')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user','title', 'text', 'created_at')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post')
