from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Submit, HTML, Field, MultiField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm, Textarea, EmailField, BooleanField, CharField, forms

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ChangeProfilePageForm(ModelForm):
    badge_id = CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                HTML(
                    """
                    <h2>Edit profile</h2>
                    """,
                ),
                Field('about_me'),
                MultiField(
                    'badge_id',
                    template='users/widgets/multipleCheckboxes.html'
                ),
                MultiField(
                    'color_value',
                    template='users/widgets/colorPicker.html',
                    css_class='p-0 m-0'
                ),
                Submit(
                    'submit', 'Update',
                    css_class="mb-4"
                ),
                css_class='col-lg-8 mx-auto profileBoxes bg-white pt-2',
            )
        )

    class Meta:
        model = CustomUser
        fields = ('about_me',)
        labels = {
            'about_me': 'About me',
        }
        widgets = {
            'about_me': Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Write something about yourself...'}),
        }

    def clean(self):
        cd = super().clean()
        userbadge_list = self.data.getlist('badge_id')
        color_value = "#" + self.data.get('color_value')
        cd['userbadge_list'] = userbadge_list
        cd['color_value'] = color_value
        if len(self.cleaned_data['userbadge_list']) > 4: # Make sure the user does not select more than 4 badges.
            raise forms.ValidationError('Select no more than 4.')

        return cd


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


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].required = True

        self.helper.layout = Layout(
            Column(
                HTML(
                    """
                    <h2>Login</h2>
                    """
                ),
                'username',
                'password',
                Submit('login', 'Login', css_class="btn btn-primary btn-block"),
            )
        )
