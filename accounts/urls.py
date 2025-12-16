from django.urls import path
from .views import register_view, profile_view
from .admin_views import AdminUserListView, AdminUserDetailView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),

    # admin panel
    path("admin/users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
]
