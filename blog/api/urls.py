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
  ApiBlogListView,
  ApiReferenceListView,
  ApiCommentByUserListView,
  api_check_blog_personal_collection,
  api_add_personal_collection,
  api_delete_from_personal_collection,
  api_get_personal_collection,
)

app_name = 'blog'

urlpatterns = [
  path('<slug>/', api_detail_blog_view, name="detail"),
  path('<slug>/update', api_update_blog_view, name="update"),
  path('<slug>/delete', api_delete_blog_view, name="delete"),
  path('create', api_create_blog_view, name="create"),
  path('blog-list', ApiBlogListView.as_view(), name="blog-list"),
  path('reference-list', ApiReferenceListView.as_view(), name="reference-list"),
  path('comment-list', ApiCommentByUserListView.as_view(), name="comment-list-user"),
  path('<slug>/addcomment', add_comment, name="add_comment"),
  path('<slug>/<commentid>/deletecomment', delete_comment, name="delete_comment"),
  path('<slug>/vote', toggle_blog_vote, name="blog_vote"),
  path('<slug>/has_voted', has_voted, name="has_voted"),
  path('get_personal_collection', api_get_personal_collection, name="get_personal_collection"),
  path('<slug>/add_to_collection', api_add_personal_collection, name="add_to_collection"),
  path('<slug>/remove_from_collection', api_delete_from_personal_collection, name="remove_from_collection"),
  path('<slug>/check_in_collection', api_check_blog_personal_collection, name="check_in_collection"),
]
