from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#the user may have many bidders and a listitng may have many bids from many users so it's many to many relationship
class listing(models.Model):
    name = models.CharField(max_length=64)
    lister_name = models.ForeignKey(User, related_name="lister", on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    starting_bid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    def __str__(self):
        return f"{self.id}: {self.name}"
    

class comment(models.Model):
    list_name = models.ForeignKey(listing,blank=False, on_delete=models.CASCADE, related_name="list_comment")
    list_comment = models.TextField(max_length=256)
    commenter_name = models.ForeignKey(User,blank=False, related_name="commenter_name", on_delete=models.CASCADE)

class Bid(models.Model):
    listing_name = models.ForeignKey(listing,blank=False ,  on_delete=models.CASCADE, related_name="list")
    bid_price = models.IntegerField()
    user_name = models.ForeignKey(User, blank=False,on_delete=models.CASCADE ,  related_name="bidder_name")

class watchlist(models.Model):
    user_id = models.ForeignKey(User, blank=False, on_delete=models.CASCADE ,  related_name="user_id")
    listing_name = models.ForeignKey(listing ,blank=False ,  on_delete=models.CASCADE, related_name="listing")
    def __str__(self):
        return f"{self.user_id}: {self.listing_name}"
