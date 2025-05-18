from django.urls import path
from .views import GroupScoreboardView

urlpatterns = [
    path('scoreboard/<int:group_id>/', GroupScoreboardView.as_view(), name='group-scoreboard'),
]
