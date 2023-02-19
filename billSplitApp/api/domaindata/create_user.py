import json

from billSplitApp.api.domaindata.error import Error


class CreateUserRequest:
    def __init__(self, user_info):
        self.username = user_info["username"]
        self.emailId = user_info["emailId"]
        self.password = user_info["password"]


class CreateUserResponse:
    def __init__(self):
        self.output = dict()
        self.output["message"] = ""
        self.error = Error()

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
