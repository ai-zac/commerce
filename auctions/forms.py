from django import forms
from django.core.exceptions import ValidationError

from .models import Auction, Bid, Category


class CreateAuctionForm(forms.ModelForm):
    img = forms.URLField(
        required = False,
        initial="https://curie.pnnl.gov/sites/default/files/default_images/default-image_0.jpeg"
    )
    categories = forms.ModelMultipleChoiceField(
        required = False,
        widget = forms.SelectMultiple(),
        queryset = Category.objects.all()
    )
    class Meta:
        model = Auction
        fields = ["title", "description", "current_price"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

    def validate_bid(self, data):
        cleaned_data = super().clean()
        new_bid = float(cleaned_data.get("price"))
        current_price = float(data["current_price"])
        
        if new_bid <= current_price:
            error = ValidationError("The offer you have made is less or equal to the current offer")
            self.add_error("price", error)
            return False
        return True 
