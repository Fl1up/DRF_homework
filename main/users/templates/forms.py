from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from main.users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirmation = cleaned_data.get('verification_email')
        if email and email_confirmation and email != email_confirmation:
            raise forms.ValidationError("Почты не существует")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.email_confirmed = False
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

