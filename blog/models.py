from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from communities.models import Communities
from account.models import Account


def upload_location(instance, filename, **kwargs):
    file_path = 'blog/{community_name}-{community_id}/{title}-{filename}'.format(
        community_name=str(instance.community.name), community_id=str(instance.community.id), title=str(instance.title),
        filename=filename
    )
    return file_path


class References(models.Model):
    refers = models.CharField(max_length=300, null=False, blank=True, unique=True)

    class Meta:
        ordering = ['refers']

    def __str__(self):
        return self.refers


class Blog(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    body = models.TextField(max_length=5000, null=False, blank=True)
    description = models.CharField(max_length=200, null=False, blank=True)
    image = models.ImageField(upload_to=upload_location, null=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    community = models.ForeignKey(Communities, on_delete=models.CASCADE)
    references = models.ManyToManyField(References)
    vote_count = models.PositiveIntegerField(default=0, verbose_name="vote count")
    slug = models.SlugField(blank=True, unique=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=300, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Vote(models.Model):
    # vote = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


@receiver(post_delete, sender=Blog)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.community.name + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=Blog)
