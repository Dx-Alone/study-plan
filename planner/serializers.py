from rest_framework import serializers
from .models import Phase, Subject, Task, Note

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description']

class SubjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'tasks']

class PhaseSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Phase
        fields = ['id', 'number', 'name', 'description', 'date_range', 'subjects']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # 确保content字段不为空
        if not validated_data.get('content'):
            raise serializers.ValidationError({'content': '笔记内容不能为空'})
        return super().create(validated_data)