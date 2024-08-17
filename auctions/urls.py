from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create")
]
