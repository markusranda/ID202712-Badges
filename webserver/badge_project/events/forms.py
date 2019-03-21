from django.\
    forms import ModelForm, Textarea, NumberInput, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Row, Column, HTML, submit
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user
from django import forms
import urllib.request

from events.models import Events


class CreateEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                'name',
                'description',
                Submit('submit', 'Create'),
                css_class='col-lg-6 mx-auto',
            )
        )

    class Meta:
        model = Events
        fields = ('name', 'description')
        labels = {
            'name': 'Name',
            'description': 'Description'
        }
        help_texts = {
            'name': 'Enter a name for the event'
        }
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the event here...'})
        }


class EventPinForm(Form):
    event_field = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "Please enter the event's pin"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                'event_field',
                Submit('submit', 'Enter'),
                css_class='col-lg-4 mx-auto formTextStyling',
            )
        )

    def clean(self):
        cd = self.cleaned_data
        event_pin = cd.get('event_field')
        try:
            Events.objects.filter(pin=event_pin).get()

        except ObjectDoesNotExist:
            self.add_error('event_field', 'Entered pin is not valid!')

        finally:
            return cd

