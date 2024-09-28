import os
import base64
import json
from storeData import store_user_app_data


def decode_pubsub(data) -> dict:
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    pubsub_json = json.loads(pubsub_data)
    return pubsub_json


def get_values(pubsub_json) -> tuple:
    app_id = pubsub_json['app_id']
    app_department = pubsub_json['app_department']
    action_id = pubsub_json['action_id']
    department_id = pubsub_json['department_id']
    user_email = pubsub_json['user_email']
    return app_id, app_department, action_id, department_id, user_email


def validation_get_values(pubsub_json):
    try:
        app_id, app_department, department, department_id = get_values(pubsub_json)
        return app_id, app_department, department, department_id
    except Exception as e:
        print(f'ERROR: {e} not found')
        return 'ERROR'


def data_processing(data, context):
    pubsub_json = decode_pubsub(data)
    if validation_get_values(pubsub_json) == 'ERROR':
        print('There is not available data')
        return 'STOP HERE'
    else:
        app_id, app_department, action_id, department_id, user_email = validation_get_values(pubsub_json)
        store_user_app_data(app_id, app_department, action_id, department_id, user_email)
        return 'Everything works'
