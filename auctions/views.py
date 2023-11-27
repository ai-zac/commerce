from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from .forms import BidForm, CreateAuctionForm
from .models import Auction, Category, User, Bid


def index(request):
    """
    The default route of your web application should let 
    users view all of the currently active auction listings. 
    """
    active_auctions = Auction.objects.filter(active=True)
    context = {"active_auctions": active_auctions}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@require_http_methods(["GET", "POST"])
def create_listing(request):
    """
    Create an auction if the method is post, if get returns an empty form
    """
    context = {}
    if request.method == "POST":
        form = CreateAuctionForm(request.POST)
        if not form.is_valid():
            context["form"] = form
            return render(request, "auctions/create_listing.html", context)

        data = form.cleaned_data
        a = Auction.objects.create(
            title=data["title"],
            description=data["description"],
            current_price=data["current_price"],
            img=data["img"],
            username=request.user,
            active=True,
        )

        if "categories" in data:
            for item in data["categories"]:
                a.categories.add(item)
        return redirect(reverse("index"))

    form = CreateAuctionForm()
    context["form"] = form
    return render(request, "auctions/create_listing.html", context)


@require_http_methods(["GET", "POST"])
def listing_page(request, id_auction):
    a = Auction.objects.get(pk=id_auction)
    context = {
        "auction": a,
        "bid_form": BidForm,
    }
    return render(request, "auctions/auction.html", context)


@require_GET
def add_auction_watchlist(request, id_auction):
    a = Auction.objects.get(pk=id_auction)
    request.user.watchlist.add(a)
    return redirect(reverse("watchlist"))


@require_GET
def delete_auction_watchlist(request, id_auction):
    a = Auction.objects.get(pk=id_auction)
    request.user.watchlist.remove(a)
    return redirect(reverse("watchlist"))


@require_http_methods(["GET", "POST"])
def watchlist_page(request):
    return render(request, "auctions/watchlist.html")


@require_POST
def bid_add(request, id_auction):
    a = Auction.objects.get(pk=id_auction)
    f = BidForm(request.POST or None)
    context = { 
        "auction": a,
        "bid_form": f,
    }
    if not f.is_valid() or not f.validate_bid(request.POST):
        return render(request, "auctions/auction.html", context)

    a.current_price = float(f.cleaned_data["price"])
    b = Bid(price=float(f.cleaned_data["price"]), user=request.user, auction=a)
    b.save()
    a.save()
    return redirect(reverse("listing_details", args=(id_auction,)))
