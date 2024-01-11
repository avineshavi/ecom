from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.contrib.auth.models import User 

class SellerRegistrationForm(UserCreationForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProductForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control' 
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'image', 'status']