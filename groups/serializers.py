from rest_framework import serializers
from .models import Group
from users.serializers import SimpleUserSerializer  # adjust the path as needed


class GroupSerializer(serializers.ModelSerializer):
    creator = SimpleUserSerializer(read_only=True)
    members = SimpleUserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'creator', 'members', 'created_at']
        read_only_fields = ['id', 'creator', 'members', 'created_at']
