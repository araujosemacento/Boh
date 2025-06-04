from django.urls import path
from dialogue import views

urlpatterns = [
    path("", views.dialogue, name="dialogue"),
]
