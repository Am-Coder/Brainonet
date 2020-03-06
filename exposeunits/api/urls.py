from django.urls import path
from exposeunits.api.views import(
  api_create_exposeunit_view,
  api_delete_exposeunit_view,
  api_detail_exposeunit_view,
  api_update_exposeunit_view,
  ApiExposeunitListView
)

app_name = 'exposeunits'

urlpatterns = [
  path('<slug>/', api_detail_exposeunit_view, name="detail"),
  path('<slug>/update', api_update_exposeunit_view, name='update'),
  path('<slug>/delete', api_delete_exposeunit_view, name="delete"),
  path('create', api_create_exposeunit_view, name='create'),
  path('list', ApiExposeunitListView.as_view(), name="list"),
]