from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "Сделать"
        IN_PROGRESS = "INPR", "В работе"
        DONE = "DONE", "Готово"

    class Priority(models.IntegerChoices):
        LOW = 1, "Низкий"
        MEDIUM = 2, "Средний"
        HIGH = 3, "Высокий"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Владелец",
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    status = models.CharField("Статус", max_length=4, choices=Status.choices, default=Status.TODO)
    priority = models.IntegerField("Приоритет", choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField("Дедлайн", null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["owner", "due_date"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.owner})"