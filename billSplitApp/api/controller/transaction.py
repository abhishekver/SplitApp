import uuid

from django.contrib.auth.models import User
from django.db import transaction
from django.forms import model_to_dict

from billSplitApp.api.domaindata.create_transaction import CreateTransactionRequest, \
    CreateSettleBalanceTransactionRequest
from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException
from billSplitApp.api.models.activity import Activity
from billSplitApp.api.models.group import GroupMembers
from billSplitApp.api.models.transaction import Transaction


def validate_create_transaction_input(transaction_info):

    if "contribution" not in transaction_info or transaction_info["contribution"] is None or len(
            transaction_info["contribution"]) == 0:
        raise InvalidRequestException("Contribution list is empty")

    if "expenditure" not in transaction_info or transaction_info["expenditure"] is None or len(
            transaction_info["expenditure"]) == 0:
        raise InvalidRequestException("Expenditure list is empty")

    if "activity_name" not in transaction_info:
        raise InvalidRequestException("Activity name is empty")

    if "activity_date" not in transaction_info:
        raise InvalidRequestException("Activity date is empty")

    total_sum = 0

    for contribution in transaction_info["contribution"]:
        if not (type(contribution["amount"]) is int or type(contribution["amount"]) is float):
            raise InvalidRequestException("Incorrect amount")
        total_sum += contribution["amount"]

    for expenditure in transaction_info["expenditure"]:
        if not (type(expenditure["amount"]) is int or type(expenditure["amount"]) is float):
            raise InvalidRequestException("Incorrect amount")
        total_sum -= expenditure["amount"]

    if total_sum != 0:
        raise InvalidRequestException("Total contribution and expenditure mismatch")


def validate_create_settle_transaction_input(transaction_info):

    if "group_id" not in transaction_info:
        raise InvalidRequestException("Group id is empty")

    if "activity_name" not in transaction_info:
        raise InvalidRequestException("activity_name is empty")

    if "activity_date" not in transaction_info:
        raise InvalidRequestException("activity_date is empty")

    if "from_user" not in transaction_info:
        raise InvalidRequestException("from_user is empty")

    if "to_user" not in transaction_info:
        raise InvalidRequestException("to_user is empty")

    if "amount" not in transaction_info or "value" not in transaction_info["amount"] \
            or "currency" not in transaction_info["amount"]:
        raise InvalidRequestException("amount is empty")


def get_transaction(tr, group):
    return {
        "id": tr.id,
        "activity": model_to_dict(tr.activity),
        "group": group,
        "amount": {
            "value": tr.amount.amount,
            "currency": tr.amount.currency.__str__()
        },
        "type": tr.type,
        "from_user": {
            "id": tr.from_user.id,
            "username": tr.from_user.username
        },
        "to_user": {
            "id": tr.to_user.id,
            "username": tr.to_user.username
        }
    }


def make_transaction(new_activity, expenditure, from_user, to_user, spend_type, group_id=None):
    Transaction.objects.create(activity=new_activity,
                               amount=expenditure,
                               type=spend_type,
                               group_id=group_id,
                               from_user=from_user,
                               to_user=to_user)


def create_transaction(create_transaction_request: CreateTransactionRequest):

    with transaction.atomic():

        new_activity = Activity.objects.create(name=create_transaction_request.activity_name,
                                               date=create_transaction_request.activity_date,
                                               id=uuid.uuid4())
        _cont = len(create_transaction_request.contribution)
        i_cont = 0
        _exp = len(create_transaction_request.expenditure)
        i_exp = 0

        while i_cont < _cont and i_exp < _exp:

            contribution = create_transaction_request.contribution[i_cont]
            expenditure = create_transaction_request.expenditure[i_exp]
            to_user = GroupMembers.objects.get(user_id=expenditure["user_id"]).user
            from_user = GroupMembers.objects.get(user_id=contribution["user_id"]).user

            print("=================================")
            print(contribution)
            print(expenditure)
            print(from_user)
            print(to_user)

            if contribution["amount"] > expenditure["amount"]:
                make_transaction(new_activity=new_activity, expenditure=expenditure["amount"], from_user=from_user,
                                 to_user=to_user, spend_type="SPEND", group_id=create_transaction_request.group_id)
                contribution["amount"] -= expenditure["amount"]
                i_exp += 1

            elif contribution["amount"] == expenditure["amount"]:
                make_transaction(new_activity=new_activity, expenditure=expenditure["amount"], from_user=from_user,
                                 to_user=to_user, spend_type="SPEND", group_id=create_transaction_request.group_id)
                contribution["amount"] -= expenditure["amount"]
                i_exp += 1
                i_cont += 1

            elif contribution["amount"] < expenditure["amount"]:
                make_transaction(new_activity=new_activity, expenditure=contribution["amount"], from_user=from_user,
                                 to_user=to_user, spend_type="SPEND", group_id=create_transaction_request.group_id)
                expenditure["amount"] -= contribution["amount"]
                i_cont += 1

            print(contribution)
            print(expenditure)
            print(from_user)
            print(to_user)
            print("=================================")


def create_settle_transaction(create_settle_balance_transaction_request: CreateSettleBalanceTransactionRequest):
    with transaction.atomic():
        new_activity = Activity.objects.create(name=create_settle_balance_transaction_request.activity_name,
                                               date=create_settle_balance_transaction_request.activity_date,
                                               id=uuid.uuid4())

        make_transaction(new_activity=new_activity, expenditure=create_settle_balance_transaction_request.amount["value"],
                         from_user=User.objects.get(id=create_settle_balance_transaction_request.from_user),
                         to_user=User.objects.get(id=create_settle_balance_transaction_request.to_user),
                         spend_type="SETTLE", group_id=create_settle_balance_transaction_request.group_id)
