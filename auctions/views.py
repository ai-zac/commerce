from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CreateAuctionForm
from .models import Auction, Category, User


def index(request):
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
    if request.method == "POST":
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = Auction.objects.create(
                title=data["title"],
                description=data["description"],
                current_price=data["current_price"],
                img=data["img"],
                user=request.user,
                active=True,
            )

            if "categories" in data:
                for item in data["categories"]:
                    a.categories.add(item)
            return redirect(reverse("index"))

    form = CreateAuctionForm()
    context = {"form": form}
    return render(request, "auctions/create_listing.html", context)
