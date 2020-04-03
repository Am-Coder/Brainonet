"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler400, handler403, handler404, handler500
from personal.api import views as personal_views



urlpatterns = [
    path('admin/', admin.site.urls),


    # REST
    path('api/account/', include('account.api.urls', 'account_api')),
    path('api/blog/', include('blog.api.urls', 'blog_api')),
    path('api/communities/', include('communities.api.urls', 'community_api')),
    path('api/expose/', include('expose.api.urls', 'expose_api')),
    path('api/exposeunits/', include('exposeunits.api.urls', 'exposeunit_api')),
    path('api/personal/', include('personal.api.urls', 'personal_api')),
    path('api/groupchat/', include('groupchat.api.urls', 'groupchat_api')),
        #AutoComplete
    # re_path(r'^select2/', include('django_select2.urls')),

]

handler400 = personal_views.error_400
handler404 = personal_views.error_404
handler403 = personal_views.error_403
handler500 = personal_views.error_500


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)