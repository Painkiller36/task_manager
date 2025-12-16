from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
    Модель задачи (Task) — основная сущность таск-менеджера.

    Хранит:
    - владельца (owner),
    - название/описание,
    - статус, приоритет, дедлайн,
    - даты создания и обновления.
    """

    class Status(models.TextChoices):
        """
        Справочник статусов задачи.

        Формат: КОД_В_БД = "значение в базе", "как показывать пользователю"
        В базе хранится короткий код.
        """
        TODO = "TODO", "Сделать"
        IN_PROGRESS = "INPR", "В работе"
        DONE = "DONE", "Готово"

    class Priority(models.IntegerChoices):
        """
        Справочник приоритетов.

        В базе хранится число (1/2/3), в интерфейсе показывается текст.
        """
        LOW = 1, "Низкий"
        MEDIUM = 2, "Средний"
        HIGH = 3, "Высокий"

    # Владелец задачи: ссылка на пользователя
    # on_delete=models.CASCADE: если удалить пользователя — удалятся все его задачи
    # related_name="tasks": у пользователя появится доступ user.tasks.all()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Владелец",
    )

    # Основные текстовые поля
    title = models.CharField("Название", max_length=200)      # название задачи
    description = models.TextField("Описание", blank=True)    # описание

    # Статус: хранится код (TODO/INPR/DONE), варианты берутся из Status.choices
    # max_length=4 потому что коды длиной 4 символа
    status = models.CharField(
        "Статус",
        max_length=4,
        choices=Status.choices,
        default=Status.TODO
    )

    # Приоритет: хранится число 1/2/3, варианты берутся из Priority.choices
    priority = models.IntegerField(
        "Приоритет",
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    # Дедлайн: дата может отсутствовать (null=True в БД, blank=True в форме)
    due_date = models.DateField("Дедлайн", null=True, blank=True)

    # created_at: фиксируем время создания (не редактируется в админке)
    # updated_at: автоматически обновляется при каждом сохранении
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Настройки модели на уровне Django ORM/БД.
        """
        # Сортировка по умолчанию: новые задачи сверху
        ordering = ["-created_at"]

        # Индексы ускоряют частые запросы:
        # - найти задачи конкретного владельца по статусу
        # - найти задачи конкретного владельца по дедлайну
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["owner", "due_date"]),
        ]

    def __str__(self):
        """
        Как объект будет отображаться в админке и в логах.
        """
        return f"{self.title} ({self.owner})"
