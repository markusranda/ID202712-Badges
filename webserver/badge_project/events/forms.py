from django.\
    forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Row, Column
from django.contrib.auth import get_user
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


    # def hop(self, commit=True):
    #     new_event = form.save()
    #     event_profile = CreateEventForm.save(commit=False)
    #     if event_profile.current_user is None:
    #         event_profile.current_user = new_event.created_by_id
    #     event_profile.save()

