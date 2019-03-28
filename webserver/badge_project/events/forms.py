from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Row, Column, HTML
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, NumberInput, Form, Textarea
from django import forms

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


class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class BadgeRequestForm(MultipleForm):
    badge_id = forms.IntegerField(widget=forms.HiddenInput())


class BadgeApprovalForm(MultipleForm):
    badge_id_as_str = forms.CharField(max_length=60, widget=forms.HiddenInput())

