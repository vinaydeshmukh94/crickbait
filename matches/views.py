from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Match
from .serializers import MatchSerializer
from django.shortcuts import get_object_or_404
from decouple import config
import requests
import logging



# Api Keys for CrickBuzz
x_rapid_api_key = config('x_RapidAPI_KEY')
x_rapid_api_host = config('x_RapidAPI_HOST')


class CreateMatchView(APIView):
    permission_classes = [IsAuthenticated]  # Later: only admin/staff?

    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        matches = Match.objects.all().order_by('-date')  # or by `date`, but it's a string
        serializer = MatchSerializer(matches, many=True)
        return Response({'matches': serializer.data})
    



class MatchDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        serializer = MatchSerializer(match)
        return Response(serializer.data)

    def put(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        serializer = MatchSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






