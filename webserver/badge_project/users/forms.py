from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Submit, HTML
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, EmailField, BooleanField
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from django.urls import reverse_lazy

from .models import CustomUser


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


class CustomUserCreationForm(UserCreationForm):
    email = EmailField()
    condition = BooleanField()

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['condition'].label = 'We need to store your email address to restore your password'
        self.fields['condition'].help_text = 'Please make sure to <i>check</i> the checkbox before you continue...'

        for fieldname in []:
            self.fields[fieldname].help_text = None

        for fieldname in ['username', 'password1', 'password2', 'condition', 'email']:
            self.fields[fieldname].required = True

        self.helper.layout = Layout(
            Column(
                HTML(
                    """
                    <h2>Create account</h2>
                    """
                ),
                'username',
                'email',
                'password1',
                'password2',
                HTML(
                    """
                    <h4>Read the conditions before continuation</h4>
                    """
                ),
                'condition',
                Submit('submit', 'Sign up', css_class="btn btn-primary btn-block"),
                css_class='col-lg-5 mx-auto mb-4 mt-4',
            )
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
