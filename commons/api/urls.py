from django.urls import path
from commons.api.views import ApiRelatedContentView

app_name = 'commons'

urlpatterns = [
    path('related-content', ApiRelatedContentView.as_view(), name='related_content')
]
