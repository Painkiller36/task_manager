from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.views.generic import ListView, DetailView

from tasks.models import Task

User = get_user_model()


class StaffOnlyMixin(UserPassesTestMixin):
    """
    Миксин-ограничитель доступа.
    Пускает только пользователей, у которых:
    - is_staff=True (staff-пользователь)
    - или is_superuser=True (суперпользователь)

    Используется в админских страницах, чтобы обычные пользователи не видели список всех пользователей.
    """
    def test_func(self):
        # self.request.user — текущий пользователь, который делает запрос
        return self.request.user.is_staff or self.request.user.is_superuser


class AdminUserListView(LoginRequiredMixin, StaffOnlyMixin, ListView):
    """
    Страница админ-панели: список всех пользователей.
    - Доступ только после логина (LoginRequiredMixin)
    - И только для staff/superuser (StaffOnlyMixin)
    - по 20 пользователей
    """
    model = User  # ListView будет работать с таблицей пользователей
    template_name = "adminpanel/user_list.html"  # HTML-шаблон для страницы списка
    context_object_name = "users"  # в шаблоне список будет доступен как переменная users
    paginate_by = 20  # по 20 пользователей на страницу

    def get_queryset(self):
        """
        Возвращает QuerySet пользователей, который будет показан на странице.
        Здесь мы добавляем:
        - annotate(tasks_count=Count("tasks")): считаем число задач пользователя на уровне SQL
        - order_by("-date_joined"): новые пользователи сверху
        """
        qs = (
            User.objects.all()
            .annotate(tasks_count=Count("tasks"))
            .order_by("-date_joined")
        )

        # Параметр поиска из URL: /accounts/admin/users/
        q = self.request.GET.get("q", "").strip()
        if q:
            # Ищем по username частичным совпадением (регистр не важен)
            qs = qs.filter(username__icontains=q)

        return qs


class AdminUserDetailView(LoginRequiredMixin, StaffOnlyMixin, DetailView):
    """
    Страница админ-панели: детали конкретного пользователя.
    Показывает:
    - базовые данные пользователя (через DetailView)
    - последние 50 задач пользователя
    - общее количество задач пользователя
    """
    model = User  # DetailView достаёт пользователя
    template_name = "adminpanel/user_detail.html"  # HTML-шаблон страницы деталей
    context_object_name = "u"  # пользователь будет доступен в шаблоне как переменная u

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст дополнительные данные, кроме самого пользователя:
        - tasks: последние 50 задач (для быстрого просмотра)
        - tasks_total: общее число задач
        """
        ctx = super().get_context_data(**kwargs)

        # self.object — это текущий пользователь, которого открыл DetailView
        ctx["tasks"] = Task.objects.filter(owner=self.object).order_by("-created_at")[:50]

        # Отдельный запрос для общего количества задач
        ctx["tasks_total"] = Task.objects.filter(owner=self.object).count()

        return ctx