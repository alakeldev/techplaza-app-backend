from django.urls import path
from .views import TaskView

urlpatterns = [
    path(
        "tasks_manager/",
        TaskView.as_view({"get": "list", "post": "create"}),
        name="tasks_manager",
    ),
    path(
        "tasks_manager/<int:pk>/",
        TaskView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="task_detail",
    ),
]
