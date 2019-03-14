from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit
from django.forms import ModelForm, NumberInput, Form
from django import forms


class EventPinForm(Form):
    event_field = forms.IntegerField()
