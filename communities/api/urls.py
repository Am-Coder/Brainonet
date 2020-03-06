from django.urls import path
from communities.api.views import(
  api_delete_community_view,
  api_create_community_view,
  api_detail_community_view,
  api_update_community_view,
  ApiCommunityListView
)

app_name = 'communities'

urlpatterns = [
  path('<slug>/', api_detail_community_view, name="detail"),
  path('<slug>/update', api_update_community_view, name='update'),
  path('<slug>/delete', api_delete_community_view, name="delete"),
  path('create', api_create_community_view, name="create"),
  path('list', ApiCommunityListView.as_view(), name="list"),
]