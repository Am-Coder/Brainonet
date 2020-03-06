from django.urls import path
from blog.api.views import(
  add_comment,
  toggle_blog_vote,
  has_voted,
  delete_comment,
  api_delete_blog_view,
  api_create_blog_view,
  api_detail_blog_view,
  api_update_blog_view,
  ApiBlogListView

)

app_name = 'blog'

urlpatterns = [
  path('<slug>/', api_detail_blog_view, name="detail"),
  path('<slug>/update', api_update_blog_view, name="update"),
  path('<slug>/delete', api_delete_blog_view, name="delete"),
  path('create', api_create_blog_view, name="create"),
  path('list', ApiBlogListView.as_view(), name="list"),
  path('<slug>/addcomment', add_comment, name="add_comment"),
  path('<slug>/<commentid>/deletecomment', delete_comment, name="delete_comment"),
  path('<slug>/vote', toggle_blog_vote, name="blog_vote"),
  path('<slug>/has_voted', has_voted, name="has_voted"),
]