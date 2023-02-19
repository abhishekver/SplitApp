import traceback

from django.db import IntegrityError
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, HTMLFormRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.user import validate_create_user_input, create_user
from billSplitApp.api.domaindata.constants import USER_ALREADY_EXISTS, UNKNOWN_ERROR
from billSplitApp.api.domaindata.create_user import CreateUserResponse, CreateUserRequest
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException


class CreateUserAPIView(APIView):
    renderer_classes([BrowsableAPIRenderer, HTMLFormRenderer])

    def post(self, request):

        create_user_response = CreateUserResponse()
        try:
            validate_create_user_input(request.data)
            create_user_request = CreateUserRequest(request.data)
            create_user(create_user_request)
            create_user_response.output = {
                "message": "User created successfully"
            }
            return Response(create_user_response.to_dict(), 200)

        except InvalidRequestException as ex:
            create_user_response.error.message = ex.message
            create_user_response.error.type = ErrorType.INVALID_INPUT.name
            return Response(create_user_response.to_dict(), 400)

        except IntegrityError:
            create_user_response.error.message = USER_ALREADY_EXISTS
            create_user_response.error.type = ErrorType.INVALID_INPUT.name
            return Response(create_user_response.to_dict(), 400)

        except Exception:
            traceback.print_exc()
            create_user_response.error.message = UNKNOWN_ERROR
            create_user_response.error.type = ErrorType.UNKNOWN.name

            return Response(create_user_response.to_dict(), 500)
