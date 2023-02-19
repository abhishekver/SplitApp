import json

from billSplitApp.api.domaindata.error import Error


class CreateTransactionRequest:
    def __init__(self, transaction_info):
        self.group_id = transaction_info["group_id"]
        self.contribution = transaction_info["contribution"]
        self.expenditure = transaction_info["expenditure"]
        self.activity_name = transaction_info["activity_name"]
        self.activity_date = transaction_info["activity_date"]


class CreateSettleBalanceTransactionRequest:
    def __init__(self, transaction_info):
        self.group_id = transaction_info["group_id"]
        self.activity_name = transaction_info["activity_name"]
        self.activity_date = transaction_info["activity_date"]
        self.from_user = transaction_info["from_user"]
        self.to_user = transaction_info["to_user"]
        self.amount = transaction_info["amount"]


class CreateTransactionResponse:
    def __init__(self):
        self.output = dict()
        self.output["message"] = ""
        self.error = Error()

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
