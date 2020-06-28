from django.db import models
from account.models import Account
from blog.models import Blog, TaggedBlogs, Comment, Vote
from communities.models import Communities, CommunitySubscribers
import datetime
# Create your models here.


class ContentVisitStats(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    community = models.ForeignKey(Communities, on_delete=models.CASCADE)
    visits = models.BigIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ('date', 'blog')


class BlogCommentCountStats(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    community = models.ForeignKey(Communities, on_delete=models.CASCADE)
    comment_count = models.BigIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ('date', 'blog')


class UserVisitStats(models.Model):
    date = models.DateField(auto_now_add=True)
    visits = models.BigIntegerField(default=0)


class CommunitySubscriberStats(models.Model):
    date = models.DateField(auto_now_add=True)
    community = models.ForeignKey(to=Communities, on_delete=models.CASCADE)
    rise = models.BigIntegerField(default=0)
    fall = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'community')
