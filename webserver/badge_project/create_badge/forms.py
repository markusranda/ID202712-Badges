from django.forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Row, Column
from badges.models import Badges


class CreateBadgeForm(ModelForm):
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
        model = Badges
        fields = ('name', 'description')
        labels = {
            'name': 'Name',
            'description': 'Description'
        }
        help_texts = {
            'name': 'Enter a name for the badge'
        }
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Describe the badge here...'})
        }
