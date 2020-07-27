""" Load all files"""
import importlib

importlib.import_module("iRPA")
from iRPA import iRPA


def call_service(service, request):
    method = service + '(request)'
    result = eval(method)
    # result = iRPA(request)
    return result
