from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager



"""
Modele custom pour le user qui prend maintenant le email en tant que username et a aussi le forfait_id en foreign key.
"""

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    jetons = models.BigIntegerField(_("jetons"), default=0)
    jetons_or = models.BigIntegerField(_("jetons_or"), default=0)
    workplace = models.CharField(max_length=255, null=True, blank=True)

    projects = models.ManyToManyField('Project')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=255, unique=False)
    folderName = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.name
    
class ProjectConfig(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    duree = models.FloatField()
    sequence = models.FloatField()

    def __str__(self):
        return self.name
    
class Classes(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    
class States(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


