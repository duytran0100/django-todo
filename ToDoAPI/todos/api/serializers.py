from todos.models import ToDo
from rest_framework import serializers


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = [
            "id", "title", "description", "completed", "created_at", "updated_at"
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }