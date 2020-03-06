from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import rest_framework.authtoken.models
from django.utils.translation import gettext_lazy as _
import rest_framework.authentication


class MyAccountManager(BaseUserManager):

    def create_user(self, mobile_number, password=None):
        if not mobile_number:
            raise ValueError('User must have a mobile number')

        user = self.model(
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        user = self.create_user(
            password=password,
            mobile_number=mobile_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(verbose_name="first name", max_length=30, null=True)
    last_name = models.CharField(verbose_name="last name", max_length=30, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'mobile_number'
    # REQUIRED_FIELDS = ['']

    objects = MyAccountManager()

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Authi(models.Model):
    mobile_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=20, null=True)


class Token(rest_framework.authtoken.models.Token):
    # key is no longer primary key, but still indexed and unique
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    # name = models.CharField(_("Name"), max_length=64)

    class Meta:
        unique_together = (('user', 'key'),)


class TokenAuthentication(rest_framework.authentication.TokenAuthentication):
    model = Token

    def authenticate(self, request):
        if 'Authorization' in request.COOKIES:
            # print(request.COOKIES['Authorization'].encode("utf-8"))
            token = request.COOKIES.get("Authorization")
            print(token)
            if token:
                token = token.replace("Token%20", "")
            print(token)
            return self.authenticate_credentials(token)

        return super().authenticate(request)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
