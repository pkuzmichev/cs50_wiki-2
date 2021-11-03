from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article>", views.article, name="article"),
    path("create", views.new_page, name="create_new_page"),
    path("edit/<str:article>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
