from django import forms
from django.core.mail import send_mail

from users.models import CustomUser


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # send email
        if user.email:
            send_mail(
                "welcome to Goodreads clone",
                f"Hi {user.username}. Welcome to Goodreads clone. Enjoy the books ans reviews.",
                "asadovgofa@gmail.com",
                [user.email],
            )

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
