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

]