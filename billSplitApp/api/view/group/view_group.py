from django.forms import model_to_dict
from djmoney.money import Money
from rest_framework.response import Response
from rest_framework.views import APIView

from billSplitApp.api.controller.group import calculate_balance, get_final_spend_and_settlement
from billSplitApp.api.controller.transaction import get_transaction
from billSplitApp.api.controller.utils import get_sample_response, return_unknown_response
from billSplitApp.api.domaindata.constants import GROUP_DOES_NOT_EXISTS
from billSplitApp.api.domaindata.error import ErrorType
from billSplitApp.api.models.group import GroupMembers, ActivityGroup
from billSplitApp.api.models.transaction import Transaction


class ViewGroupAPIView(APIView):

    def get(self, request, group_id):
        response = get_sample_response()

        try:
            groups_members = GroupMembers.objects.filter(group_id=group_id)
            group = ActivityGroup.objects.get(id=group_id)
            transactions = Transaction.objects.filter(group_id=group_id)

            members = []
            total_spend = Money(amount=0, currency="INR")
            for transaction in transactions:
                if transaction.type == "SPEND":
                    total_spend += transaction.amount

            for member in groups_members:
                members.append({
                    "user_id": member.user.id,
                    "username": member.user.username,
                    "email": member.user.email,
                })

            response["output"] = {
                "members": members,
                "group_name": group.group_name,
                "group_id": group_id,
                "total_spend": {
                    "currency": total_spend.currency.__str__(),
                    "amount": total_spend.amount
                }
            }
            return Response(response, 200)

        except GroupMembers.DoesNotExist:
            response["error"] = {
                "message": GROUP_DOES_NOT_EXISTS,
                "type": ErrorType.INVALID_INPUT.name
            }
            return Response(response, 400)

        except Exception:
            return_unknown_response(response)


class ViewGroupBalanceSheetAPIView(APIView):

    def get(self, request, group_id):
        response = get_sample_response()
        response["output"] = []
        try:
            all_members = GroupMembers.objects.filter(group_id=group_id)
            for member in all_members:

                spend, settled, received_from_settlement, others_payed = get_final_spend_and_settlement(group_id, member)
                print("=================================")
                print(member)
                # print(spend)
                # print(settled)
                # print(received_from_settlement)
                # print(others_payed)
                final_spend, final_settled = calculate_balance(spend, settled, received_from_settlement, others_payed,
                                                               group_id)
                print("=================================")

                response["output"].append({
                    "user": {
                        "user_id": member.user.id,
                        "username": member.user.username
                    },
                    "receives": {
                        "individual": final_spend,
                        "total": sum(c["amount"]["value"] for c in final_spend)

                    },
                    "pays": {
                        "individual": final_settled,
                        "total": sum(c["amount"]["value"] for c in final_settled)

                    }
                })

            return Response(response, 200)
        except Exception:
            return_unknown_response(response)


class ViewGroupTransactionsAPIView(APIView):

    def get(self, request, group_id):
        response = get_sample_response()
        response["output"] = {
            "total_spend": 0,
            "transactions": []
        }
        try:
            total = 0
            transactions = Transaction.objects.filter(group_id=group_id)

            for transaction in transactions:
                if transaction.type != "SETTLE":
                    total += transaction.amount
                group = transaction.group
                if group is not None:
                    group = model_to_dict(group)
                response["output"]["transactions"].append(get_transaction(transaction, group))
            response["output"]["total_spend"] = total.__str__()

            return Response(response, 200)
        except Exception:
            return_unknown_response(response)
