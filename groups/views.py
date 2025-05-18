from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import GroupSerializer
from django.shortcuts import get_object_or_404

class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(creator=request.user)
            group.members.add(request.user)  # Add creator as first member
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group.members.add(request.user)
        return Response({'message': f'Joined group {group.name} successfully.'}, status=status.HTTP_200_OK)

class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)

        # If user is not a member
        if request.user not in group.members.all():
            return Response({'error': 'You are not a member of this group.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove user from group
        group.members.remove(request.user)

        # If the user is the creator (admin)
        if group.creator == request.user:
            remaining_members = group.members.all()

            if remaining_members.exists():
                # Assign a new creator (first remaining member)
                new_creator = remaining_members.first()
                group.creator = new_creator
                group.save()
            else:
                # No one left — delete the group
                group.delete()
                return Response({'message': 'Group deleted as no members remained.'}, status=status.HTTP_200_OK)

        return Response({'message': f'You have left the group {group.name}.'}, status=status.HTTP_200_OK)

class ListUserGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = request.user.joined_groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
