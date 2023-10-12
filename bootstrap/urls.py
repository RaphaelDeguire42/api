from . import views
from django.urls import path

urlpatterns = [

    path('json/fetch', views.get_json),
    path('video/folder', views.ajout_dossier),
    path('json/upload', views.upload),
    path('config/store', views.store_config),

]
