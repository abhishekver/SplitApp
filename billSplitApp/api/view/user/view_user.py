import traceback

from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.user import get_transaction
from billSplitApp.api.controller.utils import get_sample_response, return_unknown_response
from billSplitApp.api.domaindata.constants import USER_DOES_NOT_EXISTS, UNKNOWN_ERROR
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.models.group import GroupMembers
from billSplitApp.api.models.transaction import Transaction


class ListUserAPIView(APIView):

    def get(self, request, user_id):
        response = get_sample_response()

        try:
            user = User.objects.get(username=user_id)
            group_members = GroupMembers.objects.filter(user=user)
            all_groups = []
            for member in group_members:
                all_groups.append({
                    "group_name": member.group.group_name,
                    "group_id": member.group.id,
                    "created_by": member.group.created_by.username,
                })
            response["output"] = {
                "info": model_to_dict(user),
                "groups": all_groups
            }
            return Response(response, 200)
        except User.DoesNotExist:
            response["error"] = {
                "message": USER_DOES_NOT_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(response, 400)
        except Exception:
            return return_unknown_response(response, 500)


class ListUserBalanceSheetAPIView(APIView):

    def get(self, request, user_id):
        response = get_sample_response()
        try:
            response["output"] = {
                "total_owes": 0,
                "total_receives": 0,
                "transactions": {
                    "paid": [],
                    "received": [],
                }
            }
            total = 0
            transactions = Transaction.objects.filter(from_user__username=user_id) \
                .values('to_user_id', "to_user__username", 'type') \
                .annotate(Sum('amount'))

            for transaction in transactions:
                total += transaction["amount__sum"]
                response["output"]["transactions"]["paid"].append(get_transaction(transaction, "to_user"))

            transactions = Transaction.objects.filter(to_user__username=user_id) \
                .values('from_user_id', "from_user__username", 'type') \
                .annotate(Sum('amount'))

            for transaction in transactions:
                total -= transaction["amount__sum"]
                response["output"]["transactions"]["received"].append(get_transaction(transaction, "from_user"))

            if total < 0:
                response["output"]["total_owes"] = -total
            else:
                response["output"]["total_receives"] = total
            return Response(response, 200)
        except Exception:
            return return_unknown_response(response, 500)
