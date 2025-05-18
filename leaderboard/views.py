from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from bets.models import Bet
from groups.models import Group
from users.models import CustomUser

class GroupScoreboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)

        if not group.members.filter(id=request.user.id).exists():
            return Response({'error': 'You are not a member of this group'}, status=403)

        # Aggregate scores
        scores = (
            Bet.objects.filter(group=group)
            .values('user')
            .annotate(total_points=Sum('points_awarded'))
            .order_by('-total_points')
        )

        # Fetch usernames
        scoreboard = []
        for entry in scores:
            user = CustomUser.objects.get(id=entry['user'])
            scoreboard.append({
                'username': user.username,
                'name': user.name,
                'total_points': entry['total_points'] or 0
            })

        return Response(scoreboard)
