from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    
    class Meta:
        model = Offer
        fields = ['offer_name','discount_amount', 'start_date','end_date']