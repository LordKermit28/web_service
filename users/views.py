import string
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, TemplateView
from django.core.mail import send_mail
from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserPassportResetForm
from users.models import User, VerificationToken

def message_view(request):
    return render(request, 'users/message.html')

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:message')
    def generate_random_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def form_valid(self, form):

        new_user = form.save()

        token = default_token_generator.make_token(new_user)
        token_object = VerificationToken(user=new_user, token=token)
        token_object.save()
        verify_url = self.request.build_absolute_uri(reverse_lazy('users:verify_email', kwargs={'token': token}))

        send_mail(
            subject='Подтвердите ваш адрес электронной почты',
            message=f'Привет! Пожалуйста, подтвердите свою электронную почту, перейдя по ссылке: {verify_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return super().form_valid(form)


class VerifyEmailView(TemplateView):
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        verified_token = get_object_or_404(VerificationToken, token=token)

        if verified_token.is_active:
            user = verified_token.user
            user.is_active = True
            user.save()

            verified_token.is_active = False
            verified_token.save()

            return redirect('users:login')

        return redirect('users:invalid_token')



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserResetPasswordView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserPassportResetForm
    template_name = 'users/reset_password.html'
    success_url = '/users/login/'

    def generate_random_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def form_valid(self, form):
        response = super().form_valid(form)
        password = self.generate_random_password()
        self.object.set_password(password)
        self.object.save()
        send_mail(
            subject='New password',
            message=f'Привет! Your new password: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[object.email],
        )
        return response
