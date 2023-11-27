from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # User registration 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # Listing pages
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/close/<id_auction>", views.close_listing, name="close_listing"),
    path("listing/details/<id_auction>", views.listing_page, name="listing_details"),
    # Watchlist  pages
    path("watchlist/add/<id_auction>", views.add_auction_watchlist, name="add_auction_to_watchlist"),
    path("watchlist/delete/<id_auction>", views.delete_auction_watchlist, name="delete_auction_to_watchlist"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    # Bids
    path("listing/bid/add/auction/<id_auction>", views.bid_add, name="bid_add"),
    # Comments
    path("listing/comment/add/auction/<id_auction>", views.comment_add, name="comment_add"),
]
