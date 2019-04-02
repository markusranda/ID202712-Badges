import os

from django import forms
from django.conf import settings
from django.forms import ModelForm, Textarea, Form, CheckboxSelectMultiple, Select, RadioSelect

from badges.models import Images


class CreateBadgeForm(Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the badge here...'}))
    image = forms.ModelChoiceField(queryset=Images.objects.values_list(), widget=forms.RadioSelect())
    RadioSelect.template_name = 'badges/widgets/select.html'
    RadioSelect.option_template_name = 'badges/widgets/select_option.html'
