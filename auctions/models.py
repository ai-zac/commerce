from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction")
    pass


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    img = models.URLField(null=True)
    categories = models.ManyToManyField(Category)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"'{self.title}' auction by {self.username}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} comment on {self.auction}"


class Bid(models.Model):
    price = models.DecimalField(max_digits=11, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} bid at {self.auction}"
