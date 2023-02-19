import traceback

from rest_framework.response import Response

from billSplitApp.api.domaindata.constants import UNKNOWN_ERROR

def get_sample_response():
    return {
        "output": {},
        "error": {}
    }

def return_unknown_response(response):
    traceback.print_exc()
    response["error"]["message"] = UNKNOWN_ERROR
    return Response(response, 500)
