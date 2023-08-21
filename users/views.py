from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from data import my_ps, my_email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = my_email
EMAIL_HOST_PASSWORD = my_ps
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
ACCOUNT_EMAIL_REQUIRED = True


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)

        verify_url = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', args=[token])
        )

        send_mail(
            'Пожалуйста, подтвердите свою электронную почту',
            f'Привет {user.email}! Пожалуйста, подтвердите свою электронную почту, перейдя по ссылке: {verify_url}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:login')
        return redirect('users:invalid_token')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user