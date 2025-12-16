from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    Форма для создания и редактирования задач.

    ModelForm автоматически строит HTML-форму на основе модели Task:
    - сам создаёт поля,
    - сам проверяет типы данных (валидация),
    - умеет сохранять объект в БД через form.save().
    """

    class Meta:
        # Указываем, по какой модели строим форму
        model = Task

        # Какие поля модели показываем в форме.
        # Важно: owner сюда не включаем, потому что owner назначается автоматически
        fields = ["title", "description", "status", "priority", "due_date"]

        # Настраиваем виджет.
        # type="date" даёт календарь выбора даты в большинстве браузеров.
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"})
        }
