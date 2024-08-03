from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("event/new/", views.event_create, name="event_create"),
    path("event/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("event/<int:pk>/delete/", views.event_delete, name="event_delete"),
]
