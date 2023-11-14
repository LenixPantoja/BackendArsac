from django.urls import path
from .views import *
from AppUsuarios import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # Crea un token 
    path('post/create/', views.create_post , name = 'creando-post'),
    # Api para obtener un token
    path('api/Login/', TokenObtainPairView.as_view(), name='loginTkn'),
    # Api para actualizar el toke creado
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Api para inicio de sesión en la aplicacion
    path('api/getUser/', AppUser_Login_ApiView.as_view(), name = 'get_User'),
    # Api para crear docentes
    path('api/v1/crearDocente/', AppUser_Docente_ApiView.as_view(), name = 'crear-docente'),
]
