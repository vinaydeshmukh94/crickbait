from rest_framework import serializers
from .models import Bet

class BetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bet
        fields = ['id', 'user', 'match', 'group', 'chosen_team', 'created_at', 'is_correct', 'points_awarded']
        read_only_fields = ['is_correct', 'points_awarded']
