from django.shortcuts import render

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register_view(request):
    """
    Регистрация нового пользователя.

    Логика:
    1) Если пользователь уже авторизован — регистрация не нужна, отправляем на главную (список задач).
    2) Если пришёл POST — значит пользователь отправил форму регистрации:
       - валидируем данные
       - создаём пользователя
       - автоматически логиним его
       - отправляем на страницу задач
    3) Если пришёл GET — показываем пустую форму регистрации.
    """

    # 1) Защита от повторной регистрации авторизованного пользователя
    if request.user.is_authenticated:
        return redirect("task_list")

    # 2) Обработка отправки формы
    if request.method == "POST":
        # Создаём форму и заполняем её данными из POST (username, password1, password2)
        form = RegisterForm(request.POST)

        # Проверяем корректность: совпадение паролей, правила сложности и т.д.
        if form.is_valid():
            # Создаём нового пользователя в БД
            user = form.save()

            # Сразу авторизуем пользователя (создаём session)
            login(request, user)

            # Редиректим на главную страницу с задачами
            return redirect("task_list")
    else:
        # 3) GET-запрос: показываем пустую форму регистрации
        form = RegisterForm()

    # Если GET или форма не прошла валидацию — показываем страницу регистрации.
    # form содержит ошибки, которые можно вывести в шаблоне.
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    """
    Профиль пользователя.

    @login_required:
    - если пользователь не авторизован, перенаправит на страницу логина
      (адрес задаётся в settings.py через LOGIN_URL).
    """
    return render(request, "accounts/profile.html")
