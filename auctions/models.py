from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image_url = models.CharField(max_length=1000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    bids = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_listing")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    def __str__(self):
        return self.title

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    content = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")

    def __str__(self):
        return f"{self.owner}_{self.listing.title}_comment"

class Bid_Infor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid_infor")
    bid_signed = models.FloatField(null=True)
    list_bidden = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True, related_name="listing_bid_infor")
    isWinner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}_bid_{self.list_bidden.title}"

class Watch_List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_watch_list")
    lists = models.ManyToManyField(Listing, blank=True, null=True, related_name="watch_list_listing")

    def __str__(self):
        return f"{self.owner}"