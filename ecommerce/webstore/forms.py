from django import forms

from webstore.models import Address


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'street', 'city', 'postcode']


class QuantityForm(forms.Form):
    CHOICES = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    )
    quantity = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
