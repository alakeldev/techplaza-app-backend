from django.urls import path
from .views import HighScoreViewSet

urlpatterns = [
    path(
        "high_scores/",
        HighScoreViewSet.as_view({"get": "list", "post": "create"}),
        name="high_scores",
    ),
]
