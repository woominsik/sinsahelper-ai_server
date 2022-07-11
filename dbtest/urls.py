from django.urls import path, include
from .views import connect2, helloAPI,item_view,connect

urlpatterns = [
    path("hello/", helloAPI),
    path("items/", item_view),
    path("connect/",connect),
    path("connect2/",connect2),
]