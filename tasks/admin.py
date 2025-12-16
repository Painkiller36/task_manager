from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Task в стандартной админке Django (/admin/).

    admin.ModelAdmin позволяет управлять тем:
    - какие колонки показывать в списке объектов,
    - какие фильтры доступны справа,
    - по каким полям работает поиск.
    """

    # Какие поля показывать в таблице списка задач в админке.
    # Это делает просмотр удобным: видно ключевые атрибуты без захода в карточку.
    list_display = (
        "id",         # первичный ключ задачи
        "title",      # название
        "owner",      # владелец (пользователь)
        "status",     # статус (TODO/INPR/DONE)
        "priority",   # приоритет (1/2/3)
        "due_date",   # дедлайн
        "created_at", # дата создания
    )

    # Фильтры в правой колонке админки.
    # Позволяют быстро отфильтровать задачи по статусу и приоритету.
    list_filter = ("status", "priority")

    # Поиск сверху в админке.
    # Ищет по:
    # - title (название задачи)
    # - description (описание)
    # - owner__username (username владельца)
    search_fields = ("title", "description", "owner__username")
