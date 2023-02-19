import traceback
from sqlite3 import IntegrityError

from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.transaction import validate_create_transaction_input, create_transaction, \
    create_settle_transaction, validate_create_settle_transaction_input
from billSplitApp.api.controller.utils import get_sample_response, return_unknown_response
from billSplitApp.api.domaindata.constants import TRANSACTION_ALREADY_EXISTS, ERROR_TRANSACTION_CREATION
from billSplitApp.api.domaindata.create_transaction import CreateTransactionRequest, CreateTransactionResponse, \
    CreateSettleBalanceTransactionRequest
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException


class CreateTransactionAPIView(APIView):

    def post(self, request):
        create_transaction_response = CreateTransactionResponse()
        try:
            validate_create_transaction_input(request.data)
            create_transaction_request = CreateTransactionRequest(request.data)
            create_transaction(create_transaction_request)
            create_transaction_response.output = {"message": "Transaction created successfully"}
            return Response(create_transaction_response.to_dict(), 200)

        except InvalidRequestException as ex:
            create_transaction_response.error.message = ex.message
            create_transaction_response.error.type = ErrorType.INVALID_INPUT.name
            return Response(create_transaction_response.to_dict(), 400)

        except IntegrityError:
            create_transaction_response.error.message = TRANSACTION_ALREADY_EXISTS
            create_transaction_response.error.type = ErrorType.INVALID_INPUT.name
            return Response(create_transaction_response.to_dict(), 400)

        except Exception:
            traceback.print_exc()
            create_transaction_response.error.message = ERROR_TRANSACTION_CREATION
            create_transaction_response.error.type = ErrorType.UNKNOWN.name

            return Response(create_transaction_response.to_dict(), 500)


class SettleBalanceSheetAPIView(APIView):

    def post(self, request):
        response = get_sample_response()
        try:
            validate_create_settle_transaction_input(request.data)
            create_settle_transaction_request = CreateSettleBalanceTransactionRequest(request.data)
            create_settle_transaction(create_settle_transaction_request)
            response["output"] = {"message": "Transaction created successfully"}
            return Response(response, 200)

        except InvalidRequestException as ex:
            traceback.print_exc()
            response["error"] = {
                "message": ex.message
            }
            return Response(response, 400)

        except IntegrityError:
            response["error"] = {
                "message": TRANSACTION_ALREADY_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(response, 400)

        except Exception:
            return_unknown_response(response)
