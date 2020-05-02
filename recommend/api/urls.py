from django.urls import re_path, path
from recommend.api.views import *

app_name = "recommend"

urlpatterns = [

    re_path(r"^make-dataset/$", create_dataset_view, name="make_recommendation_dataset"),
    re_path(r"^train-model/$", train_model_view, name="train_knn_model")
    # re_path(r"^recommend-blogs/$", train_model_view, name="train_knn_model")
    # re_path(r"^recommend-views/$", train_model_view, name="train_knn_model")

]