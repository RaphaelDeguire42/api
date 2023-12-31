from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import BaseValidator
from customModels.models import CustomUser, Project, Classes, States
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist



User = get_user_model()


class PasswordValidator(BaseValidator):
    def __init__(self, limit_value):
        super().__init__(limit_value=limit_value)
    
    def __call__(self, value):
        limit_value = self.limit_value
        if not any(char.islower() for char in value):
            raise ValidationError(
                _("The password must contain at least one lowercase letter."),
                code='password_no_lowercase',
            )

        if not any(char.isupper() for char in value):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_uppercase',
            )

        if not any(char for char in value if not char.isalnum()):
            raise ValidationError(
                _("The password must contain at least one symbol."),
                code='password_no_symbol',
            )

        if not any(char.isdigit() for char in value):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit',
            )


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

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=100,
        validators=[
            PasswordValidator(limit_value=100),
        ]
    )
    email = serializers.EmailField()
    projects = ProjectDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'projects']

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = CustomUser.objects.create(email=email, **validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user and not user.is_anonymous:
            self.update_last_login(user)

        return data

    def update_last_login(self, user):

        user.last_login = timezone.now()
        user.save()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            self.update_last_login(request.user)
        return response

    def update_last_login(self, user):

        if user and not user.is_anonymous:
            try:
             
                custom_user = get_user_model().objects.get(email=user.email)
                custom_user.last_login = timezone.now()
                custom_user.save()
            except ObjectDoesNotExist:
                pass

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if user and not user.is_anonymous:
        user.last_login = timezone.now()
        user.save()