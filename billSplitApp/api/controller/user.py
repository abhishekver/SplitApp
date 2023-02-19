from django.contrib.auth.models import User

from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException


def validate_create_user_input(user_info):

    if "username" not in user_info or user_info["username"] is None:
        raise InvalidRequestException("User name is empty")

    if "emailId" not in user_info or user_info["emailId"] is None:
        raise InvalidRequestException("emailId is empty")

    if "password" not in user_info or user_info["password"] is None:
        raise InvalidRequestException("password is empty")


def get_transaction(transaction, key):
    return {
        "user": {
            "user_id": transaction[key + "_id"],
            "user_name": transaction[key + "__username"]
        },
        "type": transaction["type"],
        "amount": {
            "value": transaction["amount__sum"]
        }
    }


def create_user(create_user_request):
    User.objects.create_user(username=create_user_request.username,
                             email=create_user_request.emailId,
                             password=create_user_request.password)
