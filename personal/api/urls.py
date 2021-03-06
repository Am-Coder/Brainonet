from django.urls import re_path, path, include
from .views import *
from blog.api.views import ApiReferenceListView, ApiBlogListView
from communities.api.views import ApiCommunityListView

app_name = "personal"

urlpatterns = [

    re_path(r"^$", stafflogin_view, name="staff_login"),
    re_path(r"^staffhome/$", staffhome_view, name="staff_home"),

    re_path(r"^staffhome/blog-manager/$", blog_manager_view, name="blog_manager"),
    re_path(r"^staffhome/community-manager/$", community_manager_view, name="community_manager"),
    re_path(r"^staffhome/reference-manager/$", reference_manager_view, name="reference_manager"),

    re_path(r"^staffhome/addblog/$", uploadblog, name="add_blog"),
    re_path(r"^staffhome/addreferences/$", uploadreferences, name="add_references"),
    re_path(r"^staffhome/addcommunity/$", uploadcommunity, name="add_community"),

    # re_path(r"^staffhome/showblogs/$", BlogHomeView.as_view(), name="show_blog"),
    # re_path(r"^staffhome/showcommunity/$", CommunityHomeView.as_view(), name="show_community"),
    re_path(r"^staffhome/showaccounts/$", UserListView.as_view(), name="show_account"),

    re_path(r"staffhome/editblog/(?P<slug>[\w-]+)/", BlogUpdateView.as_view(), name="edit_blog"),
    re_path(r"staffhome/deleteblog/(?P<slug>[\w-]+)/", BlogDeleteView.as_view(), name="delete_blog"),
    re_path(r"staffhome/editcommunity/(?P<slug>[\w-]+)/", CommunityUpdateView.as_view(), name="edit_community"),
    re_path(r"staffhome/deletecommunity/(?P<slug>[\w-]+)/", CommunityDeleteView.as_view(), name="delete_community"),
    re_path(r"staffhome/editreference/(?P<pk>[\w-]+)/", ReferenceUpdateView.as_view(), name="edit_reference"),
    re_path(r"staffhome/deletereference/(?P<pk>[\w-]+)/", ReferenceDeleteView.as_view(), name="delete_reference"),

    re_path(r"staffhome/communityhistory/(?P<slug>[\w-]+)/", CommunityHistoryView.as_view(), name="community_history"),
    re_path(r"staffhome/bloghistory/(?P<slug>[\w-]+)/", BlogHistoryView.as_view(), name="blog_history"),
    re_path(r"staffhome/referencehistory/(?P<pk>[\w-]+)/", ReferenceHistoryView.as_view(), name="reference_history"),

    re_path(r"staffhome/logout", stafflogout, name="staff_logout"),
    re_path(r"^staffhome/users_autocomplete/$", UsersAutocomplete.as_view(), name="users_autocomplete"),
    re_path(r"^staffhome/references_autocomplete/$", ReferencesAutocomplete.as_view(create_field='refers'),
            name="references_autocomplete"),

    re_path(r"^staffhome/imagefaketool$", fakenews_home, name="fake_toolkit"),
    re_path(r"^staffhome/imagefakesearch$", fakenews_image_search, name="fake_image_search"),
    re_path(r"^staffhome/imagedataset$", fakenews_image_dataset, name="fake_image_dataset"),

    re_path(r"^staffhome/staff-manager/$", staff_manager_view, name="staff_manager"),
    re_path(r"^staffhome/addstaff/$", addstaff, name="add_staff"),
    re_path(r"^staffhome/staff_autocomplete_mobile/$", StaffAutocompleteMobile.as_view(), name="staff_autocomplete_mobile"),
    re_path(r"^staffhome/staff_autocomplete_fname/$", StaffAutocompleteFname.as_view(), name="staff_autocomplete_fname"),
    re_path(r"^staffhome/staff_autocomplete_lname/$", StaffAutocompleteLname.as_view(), name="staff_autocomplete_lname"),
    re_path(r"^staffhome/staff-remove/(?P<pk>[\w-]+)$", staff_delete_view, name="staff_remove"),
    re_path(r"^staffhome/staff-list/$", ApiStaffListView.as_view(), name="staff-list"),

    # CORS not working, this is a hack so that cookie is passed to same domain for ajax
    re_path(r"^staffhome/blog-list$", ApiBlogListView.as_view(), name="blog-list"),
    re_path(r"^staffhome/reference-list$", ApiReferenceListView.as_view(), name="reference-list"),
    re_path(r"^staffhome/community-list$", ApiCommunityListView.as_view(), name="community-list"),

]
