from django import forms

ACTION_CHOICES = [
    ('start', 'Start'),
    ('stop', 'Stop'),
]

class ActionForm(forms.Form):
    action = forms.ChoiceField(widget=forms.RadioSelect, choices=ACTION_CHOICES)
