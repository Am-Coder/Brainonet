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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from personal.api import views as personal_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info = openapi.Info(
      title="Brainonet API",
      default_version='v1',
      description="Application API's",
      terms_of_service="https://www.brainonet.com/policies/terms/",
      contact=openapi.Contact(email="contact@brainonet.com"),
      license=openapi.License(name="BSD License"),
   )
schema_view = get_schema_view(
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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
    path('api/recommend/', include('recommend.api.urls', 'recommendation_api')),
    path('api/commons/', include('commons.api.urls', 'commons_api')),

    # path('api/', schema_view),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # AutoComplete
    # re_path(r'^select2/', include('django_select2.urls')),

]

handler400 = personal_views.error_400
handler404 = personal_views.error_404
handler403 = personal_views.error_403
handler500 = personal_views.error_500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
