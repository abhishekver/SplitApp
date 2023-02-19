from django.contrib import admin

from billSplitApp.api.models.activity import Activity
from billSplitApp.api.models.group import GroupMembers, ActivityGroup
from billSplitApp.api.models.transaction import Transaction

admin.site.register(Activity)
admin.site.register(ActivityGroup)
admin.site.register(GroupMembers)
admin.site.register(Transaction)
