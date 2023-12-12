from . import views
from django.urls import path

urlpatterns = [

    path('json/fetch', views.get_json),
    path('video/folder', views.ajout_dossier),
    path('json/upload', views.upload),
    path('config/store', views.store_config),
    path('image/upload', views.upload_image),
    path('feedback/upload', views.feedback_log_create),
    path('feedback/list', views.feedback_log_list),
    path('feedback/destroy', views.feedback_log_destroy),
]
