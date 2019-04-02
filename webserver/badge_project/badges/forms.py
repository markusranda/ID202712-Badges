import os

from django import forms
from django.conf import settings
from django.forms import ModelForm, Textarea, Form, CheckboxSelectMultiple, Select


class CreateBadgeForm(Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the badge here...'}))
    image = forms.ChoiceField()
    Select.template_name = 'templates/badges/select.html'
    Select.option_template_name = 'templates/badges/select_option.html'

    def __init__(self, *args, **kwargs):
        super(CreateBadgeForm, self).__init__(*args, **kwargs)

        path = settings.MEDIA_ROOT
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))

        self.fields['image'] = forms.MultipleChoiceField(
            choices=[(o, str(o)) for o in files],
            widget = CheckboxSelectMultiple()
        )


    def clean_badges(self):
        cd = super().clean()
        badges = {}
        badges = self.data['badges']

    def clean(self):
        cd = self.cleaned_data

        # try:
        #     Events.objects.filter(pin=1).get()
        #
        # except ObjectDoesNotExist:
        #     self.add_error('event_field', 'Entered pin is not valid!')
        #
        # finally:

        return cd
