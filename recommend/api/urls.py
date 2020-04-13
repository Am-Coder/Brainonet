from django.urls import re_path, path
from recommend.api.views import *

app_name = "recommend"

urlpatterns = [

    re_path(r"^make-dataset/$", create_dataset_view, name="make_recommendation_dataset")

]