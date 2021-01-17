from django import forms

class TickerForm(forms.Form):
	ticker = forms.CharField(label = 'Find a ticker', max_length=100)