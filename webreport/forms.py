from django import forms

class WebreportForm(forms.Form):
    url = forms.CharField(label='Enter a url', max_length=255)