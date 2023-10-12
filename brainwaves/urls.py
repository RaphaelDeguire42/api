from django.urls import path
from . import views
from .serializer import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [

    path('user/<pk>', views.user),
    path('register', views.register_user),
    path('update/<pk>', views.update_user),
    path('delete/<pk>', views.delete_user),

    path('checkup', views.check_authentication),
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('project', views.user_related_projects),
    path('projectdetails/<pk>', views.project_details),
    path('project-create', views.project_create), 
    path('project-update/<pk>', views.project_update),
    path('project-delete/<pk>', views.project_delete),

    path('classes/<pk>', views.classes_details),
    path('classes-create', views.classes_create), 
    path('classes-update/<pk>', views.classes_update),
    path('classes-delete/<pk>', views.classes_delete),


    path('states/<pk>', views.states_details),
    path('states-create', views.states_create), 
    path('states-update/<pk>', views.states_update),
    path('states-delete/<pk>', views.states_delete),



]