import json
from collections import defaultdict


# import pandas as pd


# handle in error response
def error(message, data='', code=1000):
    return json.dumps({'result': 'error', 'code': code, 'log_data': data, 'message': message}, indent=4, sort_keys=True,
                      default=str)


# handle in success response
def success(result_data, email_notifications="", code=200):
    return json.dumps({'result': 'True', 'data': result_data, 'emaildata': email_notifications, 'code': code},
                      default=str)


def Notify_data(dict_date=defaultdict(list), data={}):
    data = {k: '' if not v else v for k, v in data.items()}
    dict_date[data['actionCreateDate']].append(data)
    return dict(dict_date)


def success_add(data):
    return json.dumps(data)


def error_add(message, code=1000):
    return json.dumps({'Result': 'error', 'code': code, 'message': message}, sort_keys=True, default=str)
