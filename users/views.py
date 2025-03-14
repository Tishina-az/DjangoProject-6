from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш магазин!'
        message = 'Спасибо, что зарегистрировались, приятных покупок!'
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [user_email, ]

        send_mail(subject, message, from_email, recipient_list)
