from django.db import models
from django.contrib.auth.models import AbstractUser


class PostManager(models.Manager):
    def get_users_with_zero_like_posts(self, user_id):
        return super(PostManager, self).get_queryset().filter(
            likes__id__isnull=True).exclude(
            user_id=user_id).values('user_id').distinct()

    def get_zero_likes_posts(self, user_id, user_ids):
        return super(PostManager, self).get_queryset().exclude(
            likes__user_id=user_id).filter(
            user_id__in=user_ids).values('id')


class User(AbstractUser):
    additional_data = models.TextField(null=True, blank=True)
    email = models.EmailField(
        verbose_name='e-mail',
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=10000)
    title = models.CharField(max_length=255)
    objects = PostManager()

    def __str__(self):
        return "{}: {}".format(self.user, self.created_at)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = [('user', 'post')]

    def __str__(self):
        return "'{}' liked by {}".format( self.post.title, self.user.username)
