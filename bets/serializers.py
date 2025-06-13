from rest_framework import serializers
from .models import Bet
from matches.models import Match
from groups.models import Group

class BetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    group_name = serializers.SerializerMethodField()
    match_title = serializers.SerializerMethodField()
    chosen_team_name = serializers.SerializerMethodField()

    class Meta:
        model = Bet
        fields = [
            'id', 'user', 'match', 'match_title', 'group', 'group_name',
            'chosen_team', 'chosen_team_name', 'created_at',
            'is_correct', 'points_awarded'
        ]
        read_only_fields = ['is_correct', 'points_awarded']

    def get_group_name(self, obj):
        return obj.group.name

    def get_match_title(self, obj):
        return f"{obj.match.team1sname} vs {obj.match.team2sname}"

    def get_chosen_team_name(self, obj):
        if obj.chosen_team == 'team1':
            return obj.match.team1name
        elif obj.chosen_team == 'team2':
            return obj.match.team2name
        return ""