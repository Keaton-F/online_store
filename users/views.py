from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserLoginForm, UserRegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        # Сохраняем нового пользователя в базу данных
        response = super().form_valid(form)
        user = form.instance

        # Отправляем приветственное письмо
        send_mail(
            subject="Добро пожаловать в Skystore!",
            message=(
                f"Здравствуйте, {user.email}!\n\n"
                "Спасибо за регистрацию в нашем интернет-магазине. "
                "Теперь вам доступен полный функционал управления товарами."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    pass
