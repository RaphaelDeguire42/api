from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from customModels.models import Project, Classes

User = get_user_model()



class ClassSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Classes
        fields = ('id', 'name', 'project')
