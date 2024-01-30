from django.urls import path
from .views import *
from AppUsuarios import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # Crea un token 
    path('post/create/', views.create_post , name = 'creando-post'),
    # Api para obtener un token
    path('api/Login/', TokenObtainPairView.as_view(), name='loginTkn'),
    # Api para actualizar el token creado
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Api para inicio de sesión en la aplicacion
    path('api/getUser/', AppUser_Login_ApiView.as_view(), name = 'get_User'),
    # Api para crear docentes
    path('api/Docente/', AppUser_Docente_ApiView.as_view(), name = 'Api-docente'),
    # Api para crear, obtener, eliminar estudiantes
    path('api/Estudiantes', AppUser_Estudiante_ApiView.as_view(), name = 'Api-Estudiantes'),
    # Api para crear, obtener, eliminar participantes
    path('api/Participante', AppUser_Participante_ApiView.as_view(), name = 'Api-Estudiantes')

]
