from django.urls import path
from . import views


urlpatterns = [
    path('states/<pk>', views.states_details),
    path('states-create', views.states_create), 
    path('states-update/<pk>', views.states_update),
    path('states-delete/<pk>', views.states_delete),
]
