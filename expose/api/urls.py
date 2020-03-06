from django.urls import path
from expose.api.views import(
  api_create_expose_view,
  api_delete_expose_view,
  api_detail_expose_view,
  api_update_expose_view,
  ApiExposeListView
)

app_name = 'expose'

urlpatterns = [
  path('<slug>/', api_detail_expose_view, name="detail"),
  path('<slug>/update', api_update_expose_view, name="update"),
  path('<slug>/delete', api_delete_expose_view, name="delete"),
  path('create', api_create_expose_view, name="create"),
  path('list', ApiExposeListView.as_view(), name="list"),
]