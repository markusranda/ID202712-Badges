from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit
from django.forms import ModelForm, NumberInput, Form
from django import forms

from events.models import Events


class EventPinForm(Form):
    event_field = forms.IntegerField()

    def is_valid(self):
        valid = super(EventPinForm, self).is_valid()
        if valid:
            cd = self.cleaned_data
            event_pin = cd.pop('event_field')
            try:
                Events.objects.filter(pin=event_pin).get()
                return True
            except:
                print("")

        else:
            return False