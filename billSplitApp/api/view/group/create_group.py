import traceback

from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, HTMLFormRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.group import validate_create_group_input, create_group, \
    validate_add_members_in_group_input, add_members_in_group
from billSplitApp.api.controller.utils import get_sample_response, return_unknown_response
from billSplitApp.api.domaindata.constants import USER_DOES_NOT_EXISTS, GROUP_DOES_NOT_EXISTS
from billSplitApp.api.domaindata.create_group import CreateGroupRequest, AddMembersInGroupRequest
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.domaindata.exceptions.data_already_exists import DataAlreadyExists
from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException


class CreateGroupAPIView(APIView):
    renderer_classes([BrowsableAPIRenderer, HTMLFormRenderer])

    def post(self, request):
        create_group_response = get_sample_response()
        try:
            validate_create_group_input(request.data)
            create_group_request = CreateGroupRequest(request.data)
            group = create_group(create_group_request)
            create_group_response["output"] = {
                "group_id": group.id,
                "message": "Group created successfully",
            }
            return Response(create_group_response, 200)

        except InvalidRequestException as ex:
            traceback.print_exc()
            create_group_response["error"] = {
                "message": ex.message,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(create_group_response, 400)

        except User.DoesNotExist:
            create_group_response["error"] = {
                "message": USER_DOES_NOT_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(create_group_response, 400)
        except Exception:
            return_unknown_response(create_group_response)


class AddMembersInGroupAPIView(APIView):

    def post(self, request):
        add_members_in_group_response = get_sample_response()
        try:
            validate_add_members_in_group_input(request.data)
            add_members_in_group_request = AddMembersInGroupRequest(request.data)
            add_members_in_group(add_members_in_group_request)
            add_members_in_group_response["output"] = {
                "message": "Members added successfully"
            }
            return Response(add_members_in_group_response, 200)

        except InvalidRequestException as ex:
            add_members_in_group_response["error"] = {
                "message": ex.message,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(add_members_in_group_response, 400)
        except IntegrityError:
            add_members_in_group_response["error"] = {
                "message": GROUP_DOES_NOT_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(add_members_in_group_response, 400)

        except DataAlreadyExists as ex:
            add_members_in_group_response["error"] = {
                "message": ex.message,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(add_members_in_group_response, 400)

        except Exception:
            return_unknown_response(add_members_in_group_response)
