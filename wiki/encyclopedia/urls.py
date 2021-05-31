from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.showEntry, name="showEntry"),
    path("search", views.searchForm, name="searchForm"),
    path("add", views.addEntry, name="addEntry"),
    path("edit", views.editEntry, name="editEntry"),
    path("random", views.randomEntry, name="randomEntry")
]
