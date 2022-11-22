from django import forms

class MailForm(forms.Form):
    first_name = forms.CharField(
        label='First name', 
        max_length=100)
    last_name = forms.CharField(
        label='Last name',
         max_length=100)
    email = forms.CharField(
        label='Your email',
         max_length=100)

class FreshersForm(forms.Form):
    email = forms.CharField(
        label='Your email',
        max_length=100, 
        widget=forms.TextInput(attrs={
        'autocomplete':'off'
    }))
    