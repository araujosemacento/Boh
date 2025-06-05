from django.urls import path
from dialogue import views

urlpatterns = [
    path("", views.main, name="main"),
    path("dialogue/", views.dialogue, name="dialogue"),
    path("index/", views.index, name="index"),
    path("api/dialogue/", views.api_dialogue, name="api_dialogue"),
]
