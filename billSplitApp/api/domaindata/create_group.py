class CreateGroupRequest:
    def __init__(self, group_info):
        self.userIds = group_info["userIds"]
        self.group_name = group_info["group_name"]
        self.created_by = group_info["created_by"]


class AddMembersInGroupRequest:
    def __init__(self, group_info):
        self.group_id = group_info["group_id"]
        self.userIds = group_info["userIds"]
