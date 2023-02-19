from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum

from billSplitApp.api.domaindata.create_group import CreateGroupRequest, AddMembersInGroupRequest
from billSplitApp.api.domaindata.exceptions.data_already_exists import DataAlreadyExists
from billSplitApp.api.domaindata.exceptions.invalid_request_exception import InvalidRequestException
from billSplitApp.api.models.group import GroupMembers, ActivityGroup
from billSplitApp.api.models.transaction import Transaction


def validate_create_group_input(group_info):

    if "userIds" not in group_info or group_info["userIds"] is None or type(group_info["userIds"]) is not list \
            or len(group_info["userIds"]) == 0:
        raise InvalidRequestException("User ids can not be empty")

    if "group_name" not in group_info or group_info["group_name"] is None:
        raise InvalidRequestException("Group name can not be empty")

    if "created_by" not in group_info or group_info["created_by"] is None \
            or group_info["created_by"]["user_id"] is None:
        raise InvalidRequestException("created by can not be empty")


def validate_add_members_in_group_input(group_info):

    if "userIds" not in group_info or group_info["userIds"] is None or type(group_info["userIds"]) is not list:
        raise InvalidRequestException("User Ids can not be empty")

    if "group_id" not in group_info or group_info["group_id"] is None:
        raise InvalidRequestException("group id can not be empty")


def create_group(create_group_request: CreateGroupRequest):

    group_name = create_group_request.group_name

    with transaction.atomic():
        group = ActivityGroup.objects.create(group_name=group_name,
                                             created_by_id=create_group_request.created_by["user_id"])

        for user in create_group_request.userIds:
            GroupMembers.objects.create(user=User.objects.get(username=user), group=group)

    return group


def add_members_in_group(add_members_in_group_request: AddMembersInGroupRequest):

    group_id = add_members_in_group_request.group_id

    with transaction.atomic():

        for user in add_members_in_group_request.userIds:

            existing = GroupMembers.objects.filter(user__username=user, group_id=group_id)
            if existing:
                raise DataAlreadyExists("Members already exists in group.")

            GroupMembers.objects.create(user=User.objects.get(username=user), group_id=group_id)


def get_final_spend_and_settlement(group_id, member):

    spend = Transaction.objects.filter(group_id=group_id, from_user_id=member.user_id, type="SPEND") \
        .values('to_user_id', "to_user__username", 'type') \
        .annotate(Sum('amount'))

    settled = Transaction.objects.filter(group_id=group_id, from_user_id=member.user_id, type="SETTLE") \
        .values('to_user_id', "to_user__username", 'type') \
        .annotate(Sum('amount'))

    received_from_settlement = Transaction.objects.filter(group_id=group_id, to_user_id=member.user_id,
                                                          type="SETTLE") \
        .values('from_user_id', 'from_user__username', 'type') \
        .annotate(Sum('amount'))

    others_payed = Transaction.objects.filter(group_id=group_id, to_user_id=member.user_id, type="SPEND") \
        .values('from_user_id', 'from_user__username', 'type') \
        .annotate(Sum('amount'))

    return spend, settled, received_from_settlement, others_payed


def calculate_balance(spend, settled, received_from_settlement, others_payed_for, group_id):
    def get_amount(tr, mem_id):
        if mem_id not in tr:
            return 0
        else:
            return tr[mem_id]["amount__sum"]

    def get_tr_map(tr, key):
        ans = {}
        for j in tr:
            ans[j[key]] = j
        return ans

    def get_username(mp1, mp2, mem_id, key):
        _username = None
        if member_id in mp1:
            _username = mp1[mem_id][key]
        if _username is None:
            _username = mp2[member_id][key]
        return _username

    def create_tr(mem_id, user_name, value):
        return {
            "user_id": mem_id,
            "user_name": user_name,
            "amount": {
                "value": value
            }
        }

    spend_map = get_tr_map(spend, "to_user_id")
    settled_map = get_tr_map(settled, "to_user_id")
    others_payed_map = get_tr_map(others_payed_for, "from_user_id")
    received_from_settlement_map = get_tr_map(received_from_settlement, "from_user_id")

    final_spend = []
    final_received_from_settlement = []
    members = GroupMembers.objects.filter(group_id=group_id)

    for member in members:

        member_id = member.user.id
        if member_id not in spend_map and member_id not in settled_map \
                and member_id not in others_payed_map and member_id not in received_from_settlement_map:
            continue

        amount_spend = get_amount(spend_map, member_id)
        amount_settled = get_amount(settled_map, member_id)
        amount_received_from_settlement = get_amount(received_from_settlement_map, member_id)
        amount_others_paid = get_amount(others_payed_map, member_id)

        if amount_spend + amount_settled - (amount_received_from_settlement + amount_others_paid) > 0:
            username = get_username(spend_map, settled_map, member_id, "to_user__username")
            final_spend.append(
                create_tr(member_id, username,
                          amount_spend + amount_settled - (amount_received_from_settlement + amount_others_paid)))

        if amount_spend + amount_settled - (amount_received_from_settlement + amount_others_paid) < 0:
            username = get_username(received_from_settlement_map, others_payed_map, member_id, "from_user__username")
            final_received_from_settlement.append(
                create_tr(member_id, username,
                          amount_received_from_settlement + amount_others_paid - (amount_spend + amount_settled)))

    return final_spend, final_received_from_settlement
