from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


class OwnerOnlyMixin(UserPassesTestMixin):
    """
    Миксин для ограничения доступа к конкретному объекту Task.
    Используется в Detail/Update/Delete, чтобы пользователь мог:
    - просматривать
    - редактировать
    - удалять
    только СВОИ задачи.

    UserPassesTestMixin вызывает test_func(); если он вернёт False — будет 403.
    """
    def test_func(self):
        # self.get_object() — метод DetailView/UpdateView/DeleteView,
        # который достаёт объект из БД по pk из URL.
        obj = self.get_object()

        # Разрешаем доступ только если владелец задачи = текущий пользователь
        return obj.owner == self.request.user


class TaskListView(LoginRequiredMixin, ListView):
    """
    Главная страница таск-менеджера: список задач текущего пользователя.

    - LoginRequiredMixin: неавторизованных перенаправляет на страницу логина
    - ListView: отдаёт список объектов и рендерит template_name
    - paginate_by = 10: по 10 задач на страницу
    - get_queryset: фильтруем и ищем по параметрам из URL (?q=...&status=...&priority=...)
    """
    model = Task
    template_name = "tasks/task_list.html"      # шаблон списка задач
    context_object_name = "tasks"               # в шаблоне список будет доступен как tasks
    paginate_by = 10                            # количество задач на странице

    def get_queryset(self):
        """
        Возвращает QuerySet задач, которые будут показаны пользователю.
        Здесь же применяются фильтры и поиск.
        """
        # Базовое правило безопасности: показываем только задачи текущего пользователя
        qs = Task.objects.filter(owner=self.request.user)

        # Читаем параметры фильтров из строки запроса (GET-параметры)
        q = self.request.GET.get("q", "").strip()              # строка поиска
        status = self.request.GET.get("status", "").strip()    # статус (TODO/INPR/DONE)
        priority = self.request.GET.get("priority", "").strip()# приоритет (1/2/3)

        # Поиск по названию или описанию (без учёта регистра)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        # Фильтр по статусу, если он передан
        if status:
            qs = qs.filter(status=status)

        # Фильтр по приоритету: проверяем, что это число
        if priority.isdigit():
            qs = qs.filter(priority=int(priority))

        return qs


class TaskDetailView(LoginRequiredMixin, OwnerOnlyMixin, DetailView):
    """
    Страница просмотра одной задачи (карточка задачи).

    - LoginRequiredMixin: доступ только после входа
    - OwnerOnlyMixin: доступ только владельцу задачи
    - DetailView: достаёт объект по pk из URL (например /tasks/5/)
    """
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"  # в шаблоне объект будет доступен как task


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Создание новой задачи.

    - LoginRequiredMixin: создавать задачи могут только авторизованные
    - CreateView: отображает форму и сохраняет объект при POST
    - form_valid: назначаем owner автоматически (чтобы пользователь не мог подменить владельца)
    """
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")  # после создания возвращаемся на список задач

    def form_valid(self, form):
        # Назначаем владельцем текущего пользователя.
        # Это критично: owner не должен приходить с формы от пользователя.
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    """
    Редактирование задачи.

    - LoginRequiredMixin: только после входа
    - OwnerOnlyMixin: редактировать можно только свои задачи
    - UpdateView: отображает форму и обновляет объект при POST
    """
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"   # используем тот же шаблон, что и для создания
    success_url = reverse_lazy("task_list")  # после сохранения возвращаемся на список


class TaskDeleteView(LoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    """
    Удаление задачи.

    - LoginRequiredMixin: только после входа
    - OwnerOnlyMixin: удалять можно только свои задачи
    - DeleteView: показывает подтверждение и удаляет объект при POST
    """
    model = Task
    template_name = "tasks/task_confirm_delete.html"  # страница подтверждения удаления
    success_url = reverse_lazy("task_list")           # после удаления возвращаемся на список
