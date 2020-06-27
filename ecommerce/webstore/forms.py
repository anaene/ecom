from django import forms

from webstore.models import Address


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email','street', 'city', 'postcode']
