# matches/models.py

from django.db import models

class Match(models.Model):
    match_id = models.BigIntegerField()  # Match ID from API
    series_id = models.BigIntegerField() 

    date = models.DateField()   
    state = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    team1name = models.CharField(max_length=100)
    team1sname = models.CharField(max_length=10)
    team2name = models.CharField(max_length=100)
    team2sname = models.CharField(max_length=10)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match_id', 'series_id'], name='unique_match_series_combo')
        ]

    def __str__(self):
        return f"{self.team1sname} vs {self.team2sname} - {self.status}"
