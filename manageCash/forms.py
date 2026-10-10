from django import forms
from django.contrib.auth.forms import UserCreationForm
from manageCash.models import *
class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username','full_name','email','password1','password2']


class AddCashForm(forms.ModelForm):
    class Meta:
        model = AddCashModel
        fields = ['source', 'amount', 'description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseModel
        fields = ['description', 'amount']