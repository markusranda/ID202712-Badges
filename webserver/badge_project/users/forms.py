from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Submit
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ChangeProfilePageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                'about_me',
                'showcase_badge',
                Submit('submit', 'Update'),
                css_class='col-lg-6 mx-auto',
            )
        )

    class Meta:
        model = CustomUser
        fields = ('about_me', 'showcase_badge')
        labels = {
            'about_me': 'About me',
            'showcase_badge': 'Choose badges to showcase'
        }
        widgets = {
            'about_me': Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Write something about yourself...'}),
            'showcase_badge': CheckboxSelectMultiple(attrs={'cols': 40, 'rows': 5, 'placeholder': ''})
        }

