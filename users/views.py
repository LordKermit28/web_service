from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, VerificationToken
import dotenv
import os

dotenv.load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = email
EMAIL_HOST_PASSWORD = password
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
ACCOUNT_EMAIL_REQUIRED = True

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = '/users/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        token = default_token_generator.make_token(self.object)
        print(token)
        verify_url = self.request.build_absolute_uri(reverse_lazy('users:verify_email', args=[token]))
        print(verify_url)
        self.object.save()
        subject = 'Подтвердите ваш адрес электронной почты'
        message = f'Привет! Пожалуйста, подтвердите свою электронную почту, перейдя по ссылке: {verify_url}'
        from_email = EMAIL_HOST_USER
        recipient_list = [self.object.email]
        print(subject, message, from_email, recipient_list)
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
        return response


class VerifyEmailView(View):
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



class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user