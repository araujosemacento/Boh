from django.urls import path
from dialogue import views

urlpatterns = [
    path("", views.dialogue, name="dialogue"),
    path("api/dialogue/", views.api_dialogue_state, name="api_dialogue_state"),
    path("test-pause/", views.test_pause, name="test_pause"),
    path("debug/", views.debug, name="debug"),
]
