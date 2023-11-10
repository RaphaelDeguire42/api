from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import BaseValidator
from customModels.models import CustomUser, Project, Classes, States

User = get_user_model()



class StateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = States
        fields = ('id', 'name', 'project')