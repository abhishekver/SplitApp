from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.transaction import get_transaction
from billSplitApp.api.controller.utils import get_sample_response, return_unknown_response
from billSplitApp.api.domaindata.constants import USER_DOES_NOT_EXISTS, UNKNOWN_ERROR
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.models.transaction import Transaction


class ViewTransactionAPIView(APIView):

    def get(self, request, transaction_id):
        response = get_sample_response()
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            group = transaction.group
            if group is not None:
                group = model_to_dict(group)
            response["output"] = get_transaction(transaction, group)
            return Response(response, 200)
        except Transaction.DoesNotExist:
            print("User does not exists!!")
            response["error"] = {
                "message": USER_DOES_NOT_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(response, 400)
        except Exception:
            return_unknown_response(response)
