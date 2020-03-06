from django.urls import path

from . import views

app_name = "groupchat"
urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.room, name='room'),
    path('getchats/<room_name>/<page_num>/', views.getchat, name='get_chats')
]