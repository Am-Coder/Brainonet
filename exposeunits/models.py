from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

def upload_location_backgroundimage(instance, filename, **kwargs):
  file_path = 'exposeunits/backgroundimage/{name}-{filename}'.format(name=str(instance.name), filename=filename)
  return file_path

def upload_location_avatarimage(instance, filename, **kwargs):
  file_path = 'exposeunits/avatarimage/{name}-{filename}'.format(name=str(instance.name), filename=filename)
  return file_path

class Exposeunits(models.Model):
  name = models.CharField(max_length=100, null=False, blank=True)
  description = models.TextField(max_length=5000, null=False, blank=False)
  backgroundimage = models.ImageField(upload_to=upload_location_backgroundimage, null=False, blank=False)
  avatarimage = models.ImageField(upload_to=upload_location_avatarimage, null=False, blank=False)
  date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
  date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
  slug = models.SlugField(blank=True, unique=True)

  def __str__(self):
    return self.name

@receiver(post_delete, sender=Exposeunits)
def submission_delete(sender, instance, **kwargs):
  instance.backgroundimage.delete(False)
  instance.avatarimage.delete(False)


def pre_save_exposeunit_post_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = slugify(instance.name)

pre_save.connect(pre_save_exposeunit_post_receiver, sender=Exposeunits)
