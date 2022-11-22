from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course
from dal import autocomplete 

from django_select2.forms import ModelSelect2Widget
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Row, Submit, Column
from crispy_forms.bootstrap import FormActions

class BootstrapModelSelect2Widget(ModelSelect2Widget):
    def build_attrs(self, *args, **kwargs):
        attrs = super(BootstrapModelSelect2Widget, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-theme', 'bootstrap')
        return attrs

    @property
    def media(self):
        return super(BootstrapModelSelect2Widget, self).media + forms.Media(css={
            'screen': ('//cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-theme/'
                       '0.1.0-beta.10/select2-bootstrap.min.css',)})


class CourseWidget(BootstrapModelSelect2Widget):
    def get_queryset(self):
        return Course.objects.all()

    search_fields = [
        'name__icontains'
    ]


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "gender",
            "course",
            "stage",
            "year",
            "cv",
            "aggregate_consent",
            )
        widgets = {
            "course" : autocomplete.ModelSelect2(url='course-autocomplete')
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password can't be too similar to your other personal information. <br>Your password must contain at least 8 characters. <br>Your password can't be a commonly used password. <br>Your password can't be entirely numeric."

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'email',
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0'),
                Column('second_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'gender',
            'course',
            'year',
            'stage',
            'cv',
            'aggregate_consent',
            Submit('submit', 'Sign in')
        )

                                              
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

