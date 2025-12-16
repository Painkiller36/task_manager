from django.urls import path
from .views import register_view, profile_view
from .admin_views import AdminUserListView, AdminUserDetailView

urlpatterns = [
    # Регистрация: /accounts/register/
    path("register/", register_view, name="register"),

    # Профиль: /accounts/profile/
    # name="profile" используется в меню и редиректах
    path("profile/", profile_view, name="profile"),

    # Админ-панель
    # Список пользователей: /accounts/admin/users/
    # Внутри view есть ограничения доступа (только staff/superuser)
    path("admin/users/", AdminUserListView.as_view(), name="admin_user_list"),

    # Детали пользователя по id: /accounts/admin/users/12/
    # <int:pk> — параметр маршрута: pk = первичный ключ пользователя
    # DetailView автоматически использует pk, чтобы найти пользователя в БД
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
]