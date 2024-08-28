from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {'error': 'Unauthorized access.'}
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {'error': 'Bad request.'}

    return response
