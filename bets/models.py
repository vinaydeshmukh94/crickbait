from django.db import models
from django.conf import settings
from matches.models import Match
from groups.models import Group

class Bet(models.Model):
    BET_CHOICES = [
        ('team1', 'Team 1'),
        ('team2', 'Team 2'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    chosen_team = models.CharField(max_length=10, choices=BET_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(null=True, blank=True)  # Will be set after match is completed
    points_awarded = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'match', 'group')  # Enforce one bet per match per group per user

    def __str__(self):
        return f"{self.user.username} - {self.match.title} - {self.chosen_team}"
