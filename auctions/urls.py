from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listingg, name="listingg"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("add_to_watchlist <int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories, name="categories"),
    path("close_bet <int:listing_id>", views.close_bet, name="close_bet"),
    path("create", views.create, name="create")
]
