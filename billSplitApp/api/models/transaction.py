import uuid

from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

from billSplitApp.api.models.activity import Activity
from billSplitApp.api.models.group import ActivityGroup

TRANSACTION_TYPE = (
    ("SPEND", "SPEND"),
    ("SETTLE", "SETTLE")
)


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    activity = models.ForeignKey(
        to=Activity,
        on_delete=models.RESTRICT
    )
    group = models.ForeignKey(
        null=True,
        to=ActivityGroup,
        on_delete=models.RESTRICT
    )
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='INR',
        max_digits=12
    )
    type = models.CharField(
        max_length=12,
        default="",
        choices=TRANSACTION_TYPE
    )
    from_user = models.ForeignKey(
        to=User,
        default="",
        related_name="from_user",
        on_delete=models.RESTRICT
    )
    to_user = models.ForeignKey(
        to=User,
        related_name="to_user",
        default="",
        on_delete=models.RESTRICT
    )

    def __str__(self):
        if self.group is not None:
            return self.group.group_name + " : " + self.id.__str__() + " : " + self.type + " : " + self.amount.__str__() \
                + " : " + self.from_user.username + " : " + self.to_user.username
        else:
            return self.id.__str__() + " : " + self.type + " : " + self.amount.__str__() \
                + " : " + self.from_user.username + " : " + self.to_user.username

