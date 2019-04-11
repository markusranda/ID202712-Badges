import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit, Div, Field, HTML
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, Textarea, Form, CheckboxSelectMultiple, Select, RadioSelect

from badges.models import Images

from .models import Badges


class CreateBadgeForm(ModelForm):
    def clean(self):
        cd = super().clean()
        image_id = self.data['image']
        try:
            Images.objects.filter(id=image_id).get()

        except ObjectDoesNotExist:
            self.add_error('image_id', 'Image does not exist in database!')

        finally:
            cd['image_id'] = image_id
            return cd

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                Field(
                    'name', placeholder='Enter a badge name',
                ),
                'description',
                HTML(
                    "<h4>Choose the image that you wish use!</h4>"
                ),
                Field(
                    'image',
                    template='badges/widgets/radioList.html',
                ),
                Submit(
                    'submit', 'Create'
                ),
                css_class='col-lg-6 mx-auto text-white',
            )
        )

    class Meta:
        model = Badges
        fields = ('name', 'description', 'image')
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the badge here...'}),
            'image': RadioSelect(),
        }
