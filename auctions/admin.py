from django.contrib import admin

from auctions.models import Auction, Bid, Category, Comment


# Register your models here.
class CommentAdminInline(admin.TabularInline):
    model = Comment
    extra = 0


class BidAdminInline(admin.StackedInline):
    model = Bid
    extra = 0


class AuctionAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "current_price", "active"]
    inlines = [BidAdminInline, CommentAdminInline]


class BidAndCommentAdmin(admin.ModelAdmin):
    list_display = ["user", "auction"]


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAndCommentAdmin)
admin.site.register(Comment, BidAndCommentAdmin)
admin.site.register(Category)
