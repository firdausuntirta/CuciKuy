from django import forms
from .models import Transaction,UserCuciKuy, Price
from django.contrib.auth.forms import UserCreationForm

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_date', 'pelanggan', 'jeniskendaraan']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'class': 'p-2 border rounded w-full', 'type': 'date'}),
            'pelanggan': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'jeniskendaraan': forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
        }


class UserCuciKuyCreationForm(forms.ModelForm):
    class Meta:
        model = UserCuciKuy
        fields = ['username', 'nama', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'nama': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'password': forms.TextInput(attrs={'class': 'p-2 border rounded w-full', "type": "password"}),
        }

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['jeniskendaraan', 'harga']