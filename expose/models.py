from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from exposeunits.models import Exposeunits

def upload_location(instance, filename, **kwargs):
  file_path = 'expose/{exposeunit_name}-{exposeunit_id}/{title}-{filename}'.format(
    exposeunit_name = str(instance.exposeunit.name),
    exposeunit_id = str(instance.exposeunit.id),
    title = str(instance.title), filename=filename
  )
  return file_path


class Expose(models.Model):
  title = models.CharField(max_length=100, null=False, blank=False)
  body = models.TextField(max_length=5000, null=False, blank=True)
  image = models.ImageField(upload_to=upload_location, null=False, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
  date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
  exposeunit = models.ForeignKey(Exposeunits, on_delete=models.CASCADE)
  slug = models.SlugField(blank=True, unique=True)

def __str__(self):
  return self.title

@receiver(post_delete, sender=Expose)
def submission_delete(sender, instance, **kwargs):
  instance.image.delete(False)


def pre_save_expose_post_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = slugify(instance.exposeunit.name + "-" + instance.title)

pre_save.connect(pre_save_expose_post_receiver, sender=Expose)