import random
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Like, Post
from .serializers import UserSerializer, UserInfoSerializer, PostSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def get_users_activity(self, request):
        max_likes = request.GET.get('max_likes')
        users = get_user_model().objects.exclude(id=request.user.id).annotate(
            posts_count=Count('posts'),
            likes_count=Count('posts__likes')
            ).order_by('-posts_count')
        if max_likes:
            users = users.filter(likes_count__lte=max_likes)

        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def make_like(self, request):
        id = request.data.get("id")
        user = get_object_or_404(self.queryset, pk=id)

        posts_uresrs = Post.objects.get_users_with_zero_like_posts(user.id)

        posts = Post.objects.get_zero_likes_posts(user.id, posts_uresrs)

        if posts:
            post_id = random.choice(posts)['id']
            Like(post_id=post_id, user=user).save()
            return Response({'updated': post_id}, status=200)

        return Response({'not_updated': "Can not find posts to like"}, status=304)

    @action(methods=['post'], detail=False)
    def sign_up(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            new_user = user_serializer.create(user_serializer.validated_data)
            return Response({'id': new_user.pk}, status=201)
        return Response({'detail': user_serializer.errors}, status=400)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
