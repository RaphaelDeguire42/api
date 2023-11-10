from django.urls import path
from . import views


urlpatterns = [
    path('project', views.user_related_projects),
    path('projectdetails/<pk>', views.project_details),
    path('project-create', views.project_create), 
    path('project-update/<pk>', views.project_update),
    path('project-delete/<pk>', views.project_delete),
]
