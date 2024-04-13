from django.test import TestCase

# Create your tests here.
import requests

def api_asistencia():
    # URL de la API
    url = 'https://06e8-8-242-169-8.ngrok-free.app/api/AsistenciaEstudiante/'

    # Datos que enviarás en el cuerpo de la solicitud (en formato JSON)
    datos = {
        "tipo_asistencia": "tipoAsistencia 44544",
        "descripcion": "descripcion jj ",
        "hora_llegada": "2024-04-01 01:05",
        "soporte": None,
        "matricula_estudiante": "4"
    }
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyMDA1ODIzLCJpYXQiOjE3MTE5MzM4MjMsImp0aSI6IjkzZTg2YTNmN2IwMDRjYWJiZjdiOGJlMzc1NjA1NDEyIiwidXNlcl9pZCI6MX0.rHo0dROd6lfNykHbIBLIIZf9j68Qj7lAn-mHmgrfBUI'

    # Encabezados de la solicitud con el token de autorización
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'  # Especificar el tipo de contenido JSON
    }

    # Realizar la solicitud POST enviando los datos en el cuerpo
    response = requests.post(url, json=datos, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa
        respuesta_api = response.json()
        print('Respuesta de la API:', respuesta_api)
    else:
        # Hubo un error en la solicitud
        print('Error en la solicitud:', response.status_code)
        print('Contenido de la respuesta:', response.text)


def obtener_observaciones_estudiante(url, token):
    # Encabezados de la solicitud con el token de autorización
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'  # Especificar el tipo de contenido JSON
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa
        respuesta_api = response.json()
        print('Respuesta de la API:', respuesta_api)
    else:
        # Hubo un error en la solicitud
        print('Error en la solicitud:', response.status_code)
        print('Contenido de la respuesta:', response.text)

# URL de la API
url_api = 'https://06e8-8-242-169-8.ngrok-free.app/api/ObservacionesEstudiante/?pIdEstudiante=1&pIdMateria=1&pIdCurso=2'

# Token de autorización
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNjkwOTIwLCJpYXQiOjE3MTI2MTg5MjAsImp0aSI6IjMxNGE4NzkzNjk4ZTQyYWY5N2MzMzE5YzhlMTZmMDlmIiwidXNlcl9pZCI6MX0.huxtbsaGQCfy5gOOXpENIa4hNXtbRiqETqycwtghpvE'

# Llamar a la función para obtener las observaciones del estudiante
obtener_observaciones_estudiante(url_api, token)
