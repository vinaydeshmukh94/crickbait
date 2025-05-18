from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Bet
from .serializers import BetSerializer
from matches.models import Match
from groups.models import Group

class PlaceBetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.validated_data['match']
            group = serializer.validated_data['group']

            # Check if user is part of the group
            if not group.members.filter(id=request.user.id).exists():
                return Response({'error': 'You are not a member of this group'}, status=403)

            # Prevent duplicate bet
            if Bet.objects.filter(user=request.user, match=match, group=group).exists():
                return Response({'error': 'You have already placed a bet for this match in this group'}, status=400)

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserBetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bets = Bet.objects.filter(user=request.user).order_by('-created_at')
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)
