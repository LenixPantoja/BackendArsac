from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets

# Importamos los serializadores de App Usuarios
from AppUsuarios.serializers import *

# Importamos los views de App Usuarios
from AppUsuarios.models import *

# Librerias para JWT
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


class AppUser_Login_ApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            # Obtenemos el usuario autenticado
            user = request.user

            # Serializamos el usuario para obtener el nombre de usuario
            serializer = UsuariosSerializers(user)

            # Devolvemos el nombre de usuario como respuesta
            return Response({"username": serializer.data["username"]})
        else:
            return Response({"detail": "El usuario no está autenticado"}, status=401)


""" 
    Funcion que permite saber si el JWT fue aceptado
"""


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_post(request):
    return JsonResponse({"msg": "todo funcionando"})


"""
    @Class AppUser_ApiView
    y el método POST que permitirá guardar registros en la base de datos. 
"""


class AppUser_Docente_ApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # Serializar los datos del usuario
        user_data = request.data["docente"]
        user_serializer = UsuariosSerializers(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            # Asignar el usuario al docente
            docente_data = {
                "user": user.id,
                "docente_profesion": request.data["docente_profesion"],
                "docente_tipo_Id": request.data["docente_tipo_Id"],
                "docente_estado": request.data["docente_estado"],
                "docente_numero_Id": request.data["docente_numero_Id"],
                "docente_fecha_nacim": request.data["docente_fecha_nacim"],
            }
            docente_serializer = DocenteSerializers(data=docente_data)

            if docente_serializer.is_valid():
                docente_serializer.save()
                return Response(docente_serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                docente_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
