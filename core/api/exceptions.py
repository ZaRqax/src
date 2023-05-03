from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.api.common.openapi_serializers import BadRequestResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    data = {}
    if isinstance(exc, ValidationError):
        data = BadRequestResponse(
            data={
                'message': 'Validation error.',
                'extra': {
                    'fields': response.data,
                },
            },
        ).initial_data
    elif 'detail' in response.data:
        data = BadRequestResponse(
            data={
                'message': response.data.get('detail'),
                'extra': {},
            },
        ).initial_data

    return Response(data, status=response.status_code, headers=response.headers)
