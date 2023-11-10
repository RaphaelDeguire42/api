from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from customModels.models import Project, Classes, States

User = get_user_model()


class StateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = States
        fields = ('id', 'name', 'project')


class ClassSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Classes
        fields = ('id', 'name', 'project')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'folderName')

class ProjectDetailsSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'classes', 'states')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        classes = self.context.get('classes')
        states = self.context.get('states')
        if classes is not None:
            representation['classes'] = ClassSerializer(classes, many=True).data
        if states is not None:
            representation['states'] = StateSerializer(states, many=True).data
        return representation
