from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#the user may have many bidders and a listitng may have many bids from many users so it's many to many relationship
class listing(models.Model):
    name = models.CharField(max_length=64)
    lister_name = models.ForeignKey(User, related_name="lister", on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    price = models.IntegerField()
    date = models.DateTimeField()
    category = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

class comment(models.Model):
    list_name = models.ForeignKey(listing,blank=False, on_delete=models.CASCADE, related_name="list_comment")
    list_comment = models.TextField(max_length=256)
    commenter_name = models.ForeignKey(User,blank=False, related_name="commenter_name", on_delete=models.CASCADE)

class Bid(models.Model):
    listing_name = models.ForeignKey(listing,blank=False ,  on_delete=models.CASCADE, related_name="list")
    bid_price = models.IntegerField()
    user_name = models.ForeignKey(User, blank=False,on_delete=models.CASCADE ,  related_name="bidder_name")
