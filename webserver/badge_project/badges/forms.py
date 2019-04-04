import os

from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, Textarea, Form, CheckboxSelectMultiple, Select, RadioSelect

from badges.models import Images


class CreateBadgeForm(Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the badge here...'}))
    image_radio_field = forms.ModelChoiceField(queryset=Images.objects.values_list(), widget=forms.RadioSelect())
    RadioSelect.template_name = 'badges/widgets/radioList.html'

    def clean(self):
        cd = super().clean()
        image_object = cd.get('image_radio_field')
        image_id = image_object[0]
        try:
            Images.objects.filter(id=image_id).get()

        except ObjectDoesNotExist:
            self.add_error('image_id', 'Image does not exist in database!')

        finally:
            cd['image_id'] = image_id
            return cd
