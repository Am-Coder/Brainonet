from django.urls import re_path, path, include
from .views import *

app_name = "personal"

urlpatterns = [

    re_path(r"^$", stafflogin, name="staff_login"),
    re_path(r"^staffhome/$", staffhome, name="staff_home"),
    re_path(r"^staffhome/addblog/$", uploadblog, name="add_blog"),
    re_path(r"^staffhome/addreferences/$", uploadreferences, name="add_references"),
    re_path(r"^staffhome/addcommunity/$", uploadcommunity, name="add_community"),
    re_path(r"^staffhome/showblogs/$", BlogHomeView.as_view(), name="show_blog"),
    re_path(r"^staffhome/showaccounts/$", UserListView.as_view(), name="show_account"),
    re_path(r"staffhome/editblog/(?P<slug>[\w-]+)/", BlogUpdateView.as_view(), name="edit_blog"),
    re_path(r"staffhome/deleteblog/(?P<slug>[\w-]+)/", BlogDeleteView.as_view(), name="delete_blog"),
    re_path(r"staffhome/logout", stafflogout, name="staff_logout"),
    re_path(r"^home/users_autocomplete/$", UsersAutocomplete.as_view(), name="users_autocomplete"),
    re_path(r"^home/references_autocomplete/$", ReferencesAutocomplete.as_view(create_field='refers'),
            name="references_autocomplete"),
    re_path(r"^staffhome/faketoolkit/", fakenews_home, name="fake_toolkit"),
    re_path(r"^staffhome/imagefaketool$", fakenews_image_search, name="fake_image_search"),
    re_path(r"^staffhome/imagedataset", fakenews_image_dataset, name="fake_image_dataset"),

]
