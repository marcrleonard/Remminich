from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            # 'user_job': "Please choose your current job.",
        }
        # This is how you exclude a field
        exclude = ('subscription_level',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'password1',
            # 'password2',
        ]
        help_texts = {
            # 'user_job': "Please choose your current job.",
        }
        # This is how you exclude a field
        exclude = ('subscription_level',)

    # def save(self, commit=True):
    #     user = super(UserChangeForm, self).save(commit=False)
    #     # user.set_password(self.cleaned_data["password1"])
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user

