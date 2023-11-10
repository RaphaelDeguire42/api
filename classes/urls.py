from django.urls import path
from . import views


urlpatterns = [
    path('classes/<pk>', views.classes_details),
    path('classes-create', views.classes_create), 
    path('classes-update/<pk>', views.classes_update),
    path('classes-delete/<pk>', views.classes_delete),
]
