from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import User , listing , comment , Bid, watchlist


class BidForm(forms.Form):
    bid = forms.IntegerField(max_value=10000000 ,widget=forms.NumberInput(attrs={'class': 'myfieldclass'}))

class CommentForm(forms.Form):
    comment2 = forms.CharField(widget=forms.Textarea(attrs={'class': 'myfieldclass'}))

class NewTaskForm(forms.Form):
    CHOICES =( 
    ('1', "Fashion"), 
    ('2', "Toys"), 
    ('3', "Electronics"),
    ('4', "Home"), 
    ('5', "Other") 
) 
    title = forms.CharField(max_length=100 , widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    starting_bid = forms.IntegerField(max_value=10000000, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Category = forms.ChoiceField(choices = CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    url = forms.URLField(label='Link', required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : listing.objects.all()
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
    
#if the user isn't logged in he will be directed to the login page
@login_required(login_url='login')
def watch_list(request):
    #render the watchlist page and passing all the list listings that the user added 
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist.objects.filter(user_id=request.user)
    })

#if the user isn't logged in he will be directed to the login page
@login_required(login_url='login')
def add_to_watchlist(request, listing_id):
    listing_details = listing.objects.get(id=listing_id)
    try:
        # delete the listing from the database if found
        delete_from_watchlist = watchlist.objects.get(user_id=request.user , listing_name=listing_details)
        delete_from_watchlist.delete()
        return HttpResponseRedirect(reverse("listingg", args=[listing_id]))
    except ObjectDoesNotExist:
        # if not found insert into the database
        insert_to_watchlist = watchlist(user_id=request.user , listing_name=listing_details)
        insert_to_watchlist.save()
        return HttpResponseRedirect(reverse("listingg", args=[listing_id]))

#if the user isn't logged in he will be directed to the login page
@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        #get the data from the form
        form = NewTaskForm(request.POST)

        #check if form data is valid
        if form.is_valid():

            # Isolate the data from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            bid = form.cleaned_data["starting_bid"]
            Category = form.cleaned_data["Category"]
            link = form.cleaned_data["url"]

            # Add the new task to our list of tasks
            new_listing = listing(name=title, lister_name=request.user ,current_bid = 0, url=link, starting_bid=bid , category = Category , description = desc)
            new_listing.save()
            
            
            return HttpResponseRedirect(reverse("index"))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/create.html", {
                "form": form
            })


    #if form isn't submitted
    return render(request, "auctions/create.html", {
        "form" : NewTaskForm()
    })

def categories(request):
    if request.method == "POST":
        # get the category selected
        selected_category = request.POST.get('c')
        return render(request, "auctions/categories.html",{
            "categories" : listing.objects.filter(category=selected_category)
        })
    
    else:
        return render(request, "auctions/categories.html", {
          "categories" : listing.objects.all()
        })

def listingg(request, listing_id):
    listing_details = listing.objects.get(id=listing_id)
    bid_details = Bid.objects.filter(listing_name=listing_details)
    comments = comment.objects.filter(list_name=listing_details)
    message2 = 0
    if request.user == listing_details.lister_name:
        message2 = 1
    if request.user.is_authenticated:
        if request.method == "POST":
            #get data
            comment_form = CommentForm(request.POST)
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                # Isolate the data from the 'cleaned' version of form data
                bid = bid_form.cleaned_data["bid"]
                if bid > listing_details.starting_bid and bid > listing_details.current_bid:
                    # if the bid is higher than the last bid and the bid specified by the user then add to the database and update the current bid in the listing to the new value
                    new_bid2 = Bid(listing_name=listing_details , bid_price=bid, user_name=request.user )
                    listing_details.current_bid = bid
                    new_bid2.save()
                    listing_details.save()
                    listing_details = listing.objects.get(id=listing_id)
                    bid_details = Bid.objects.filter(listing_name=listing_details)
            if comment_form.is_valid():
                #if the comment is valid then add to the database
                Comment = comment_form.cleaned_data["comment2"]
                new_comment = comment(list_name=listing_details, list_comment=Comment, commenter_name=request.user)
                new_comment.save()
        try:
            # check if the listing is in the watchlist pass the message
            watchlist.objects.get(user_id=request.user , listing_name=listing_details)
            return render(request, "auctions/listings.html", {
                "listing": listing_details,
                "message": 1,
                "bid_form" : BidForm(),
                "comment_form" : CommentForm(),
                "bids": bid_details,
                "comments": comments,
                "message2": message2
            })
        
            # if the listing isn't there 
        except ObjectDoesNotExist:
            return render(request, "auctions/listings.html", {
                "listing": listing_details,
                "message": 0,
                "bid_form" : BidForm(),
                "comment_form" : CommentForm(),
                "bids": bid_details,
                "comments": comments,
                "message2": message2
            })
    else:
        return render(request, "auctions/listings.html", {
                "listing": listing_details,
                "bids": bid_details,
                "comments": comments
            })
def close_bet(request, listing_id):
    listing_details = listing.objects.get(id=listing_id)
    listing_details.closed = True
    listing_details.save()
    winner_bid = Bid.objects.get(listing_name=listing_details, bid_price=listing_details.current_bid)
    winner_bid.closed = True
    winner_bid.save()
    return HttpResponseRedirect(reverse("listingg", args=[listing_id]))
