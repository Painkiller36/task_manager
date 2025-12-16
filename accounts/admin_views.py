from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.views.generic import ListView, DetailView

from tasks.models import Task

User = get_user_model()


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AdminUserListView(LoginRequiredMixin, StaffOnlyMixin, ListView):
    model = User
    template_name = "adminpanel/user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            User.objects.all()
            .annotate(tasks_count=Count("tasks"))
            .order_by("-date_joined")
        )

        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(username__icontains=q)

        return qs


class AdminUserDetailView(LoginRequiredMixin, StaffOnlyMixin, DetailView):
    model = User
    template_name = "adminpanel/user_detail.html"
    context_object_name = "u"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tasks"] = Task.objects.filter(owner=self.object).order_by("-created_at")[:50]
        ctx["tasks_total"] = Task.objects.filter(owner=self.object).count()
        return ctx
