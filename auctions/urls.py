from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("auction/<id_auction>", views.listing_page, name="auction_page"),
    path("watchlis/add/<id_auction>", views.add_auction_watchlist, name="add_auction_to_watchlist"),
    path("watchlis/delete/<id_auction>", views.delete_auction_watchlist, name="delete_auction_to_watchlist"),
    path("watchlist", views.show_watchlist, name="watchlist"),
]
