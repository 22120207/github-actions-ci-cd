from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import User, Category, Listing, Watch_List, Comment, Bid_Infor



def index(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            watch_list = Watch_List.objects.get(owner=user)
            watch_list_count = watch_list.lists.count()
        except Watch_List.DoesNotExist:
            watch_list_count = 0

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "watch_list_count": watch_list_count
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    user = request.user
    watch_list = Watch_List.objects.get(owner=user)
    watch_list_count = watch_list.lists.count()

    if request.method == "GET":
        return render(request, "auctions/create_list.html", {
            "categories": Category.objects.all(),
            "watch_list_count": watch_list_count
        })
    elif request.method == "POST":
        owner = request.user
        category = get_object_or_404(Category, category_name=request.POST['category'])

        new_listing = Listing.objects.create(
            title=request.POST['title'], 
            description=request.POST['description'],
            image_url=request.POST['image_url'], 
            price=request.POST['price'], 
            owner=owner,
            category=category
        )
        
        return HttpResponseRedirect(reverse("index")) 
    
def categories(request):
    user = request.user
    watch_list = Watch_List.objects.get(owner=user)
    watch_list_count = watch_list.lists.count()

    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            "categories": Category.objects.all(),
            "watch_list_count": watch_list_count
        })
    elif request.method == "POST":
        new_category = Category.objects.create(category_name=request.POST['category_name'])

        return render(request, "auctions/categories.html", {
            "categories": Category.objects.all(),
            "watch_list_count": watch_list_count
        })
    
def listing_page(request, title):
    user = request.user

    watch_list = Watch_List.objects.get(owner=user)
    watch_list_count = watch_list.lists.count()

    list = Listing.objects.get(title=title)
    on_watchlist = False

    comments = Comment.objects.filter(listing=list)

    message = f"There are {list.bids} right now!"

    if watch_list:
        on_watchlist = list in watch_list.lists.all()

    if request.method == "GET":
        return render(request, "auctions/listing_page.html", {
            "title": title,
            "listing": list,
            "watch_list_count": watch_list_count,
            "on_watchlist": on_watchlist,
            "comments": comments,
            "message": message,
        })
    if request.method == "POST": 
        if 'submit_bid' in request.POST:
            bid_value = float(request.POST['bid_value'])
            if bid_value > list.price:
                bids = list.bids + 1
                list.price = bid_value
                list.bids = bids
                list.save()
        elif 'add_to_watch_list' in request.POST:
            if not on_watchlist:
                watch_list.lists.add(list)
                on_watchlist = True
        elif 'remove_from_watch_list' in request.POST:
            if on_watchlist:
                watch_list.lists.remove(list)
                on_watchlist = False
        elif 'close_auction' in request.POST:
            list.objects.update(isActive=False)
        elif 'submit_comment' in request.POST:
            comment_content = request.POST['content']
            if user.is_authenticated:
                new_comment = Comment.objects.create(
                owner=user,
                content=comment_content,
                listing=list,
                )
            comments = Comment.objects.filter(listing=list),
        
        return HttpResponseRedirect(reverse("listing_page", args=[title]))
    
@login_required
def watch_list(request, username):
    user = request.user
    watch_list = Watch_List.objects.get(owner=user)
    watch_list_count = watch_list.lists.count()

    if request.method == "GET":
        return render(request, "auctions/watch_list.html", {
            "watch_list": Watch_List.objects.get(owner=user),
            "watch_list_count": watch_list_count
        })
    if request.method == "POST":
        return HttpResponse(request)