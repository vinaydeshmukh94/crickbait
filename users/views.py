from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from .utils import get_user_token
from bets.models import Bet
from groups.models import Group
from django.db.models import Sum

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_user_token(user)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token = get_user_token(user)
                return Response({'token': token})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "contact": user.contact,
        })


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_bets = Bet.objects.filter(user=user).count()
        correct_bets = Bet.objects.filter(user=user, is_correct=True).count()
        total_points = Bet.objects.filter(user=user).aggregate(Sum('points_awarded'))['points_awarded__sum'] or 0
        groups_joined = user.joined_groups.count()
        win_percentage = round((correct_bets / total_bets) * 100, 2) if total_bets else 0.0

        return Response({
            "total_bets": total_bets,
            "correct_bets": correct_bets,
            "total_points": total_points,
            "groups_joined": groups_joined,
            "win_percentage": win_percentage
        })