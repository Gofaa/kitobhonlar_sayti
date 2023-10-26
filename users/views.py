from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from users.models import CustomUser

from .forms import UserCreationForm, UserLoginForm, UserUpdateForm


# Create your views
class RegisterView(View):
    def get(self, request):
        create_form = UserCreationForm()
        context = {
            "form": create_form
        }
        return render(request, 'register.html', context)

    def post(self, request):
        create_form = UserCreationForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect("users:login")
        else:
            context = {
                "form": create_form
            }
            return render(request, 'register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = UserLoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        context = {
            'login_form': login_form
        }
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "Siz profilingizga muvaffaqiyatli kirdingiz")
            return redirect('books:list')
        else:
            return render(request, 'login.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        #if not request.user.is_authenticated:
        #    return redirect("users:login")
        context = {
            'login_user': request.user
        }
        return render(request, 'profile.html', context)


class LogOutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        messages.info(request, "Siz profilingizdan muvaffaqiyatli chiqdingiz")
        return redirect('landing_page')


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = UserUpdateForm(instance=request.user)
        context = {
            'update_form': update_form
        }
        return render(request, 'profile_edit.html', context)

    def post(self, request):
        update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        context = {
            "update_form": update_form
        }

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Profil ma'lumotlaringiz muvaffaqiyatli o'zgartirildi")
            return redirect('users:profile')
        return render(request, 'profile_edit.html', context)


