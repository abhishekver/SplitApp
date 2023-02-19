import uuid

from django.utils.timezone import now
from django.db import models


class Activity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(
        null=False,
        max_length=20
    )
    date = models.DateTimeField(
        null=False,
        auto_now=False,
        default=now
    )

    def __str__(self):
        return self.name + " : " + self.id.__str__()
