import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm/{token}/'
        self.send_verification_email(user.email, host, url)
        return super().form_valid(form)

    def send_verification_email(self, user_email, host, url):
        send_mail(
            subject=f'Подтверждение почты на сайте {host}',
            message=f'''Здравствуйте!

                    Для завершения регистрации на сайте http://{host}/, пройдите по ссылке: 
                    {url} 
                    и подтвердите ваш email.''',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user_email]
        )


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/register.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('catalog:products_list')
