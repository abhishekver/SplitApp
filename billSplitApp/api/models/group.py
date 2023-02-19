import uuid

from django.contrib.auth.models import User
from django.db import models


class ActivityGroup(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    group_name = models.CharField(
        max_length=50,
        default="",
    )
    created_by = models.ForeignKey(
        to=User,
        related_name="created_by",
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.group_name + " : " + self.id.__str__()


class GroupMembers(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    group = models.ForeignKey(
        to=ActivityGroup,
        on_delete=models.RESTRICT,
        default=""
    )
    user = models.ForeignKey(
        to=User,
        related_name="user",
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.group.group_name + " : " + self.user.username + " : " + self.id.__str__()
