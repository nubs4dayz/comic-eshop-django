from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ComicShop.models import UserProfile


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity', min_value=1, max_value=100)


class CreditCardForm(forms.Form):
    card_holder = forms.CharField(label='Card Holder', max_length=255)
    card_number = forms.CharField(label='Card Number', max_length=16)
    cvv = forms.CharField(label='CVV', max_length=3)
    expiration_date = forms.DateField(label='Expiration Date')

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control container"

    class Meta:
        model = UserProfile
        fields = ['name', 'surname', 'city', 'phone', 'address']


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control container"

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
