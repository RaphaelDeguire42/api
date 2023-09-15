from . import views
from django.urls import path

urlpatterns = [
    path('video/json', views.voir_json),
    path('video/folder', views.ajout_dossier),
    path('json/upload', views.upload)
]
