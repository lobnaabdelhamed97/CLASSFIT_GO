import base64
import json
from json import JSONDecodeError
import requests
from database import config, execution


def key_sec(params):
    try:
        if 'ProjectKey' in params and 'ProjectSecret' in params and type(params['ProjectKey']) is str \
                and type(params['ProjectSecret']) is str:
            projectkey = params['ProjectKey']
            projectsecret = params['ProjectSecret']
            message = str(projectkey) + "-" + str(projectsecret)
            key_sec = base64.b64encode(message.encode(encoding='utf-8', errors='strict'))
            return key_sec
        else:
            raise Exception("Something went wrong: required project key and secret")
    except Exception as err:
        return err


def bundle_curl(service_name, params):
    # data['ply_id','org_id','gm_id','coupon_code','join_type','sub_id','fees','PayChoice','pay_type','source','tkn','dev_id','IsFree','ProjectKey','ProjectSecret','contact_email','GmDate','currency_id']

    try:
        url = config.bundle_url + service_name
        key_security = key_sec(params)
        headers = {
            'Key-Sec': key_security,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # print(params)
        s = requests.Session()
        response = s.post(url, headers=headers, data=params)
        return json.loads(response.text.encode('utf8'))
    except ConnectionError:
        return 'BundleCurl: Error in Connection.'
    except JSONDecodeError:
        return 'BundleCurl: Error Json Decode.'
    except Exception:
        return 'Error In BundleCurl.'


# json data type
def game_curl(service_name, params):
    try:
        url = config.payment_url + service_name
        payload = json.dumps(params)
        secret_key = key_sec(params)
        headers = {
            'Key-Sec': secret_key,
            'Content-Type': 'application/json; charset=utf-8'
        }
        responses = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(responses.text.encode('utf8'))
    except ConnectionError:
        return 'callPayment: Error in Connection.'
    except JSONDecodeError:
        return 'callPayment: Error Json Decode.'
    except Exception:
        return 'Error In callPayment.'

def logAllActions(log_data):
    try:
        if not log_data:
            return 0
        else:
            if 'UserId' not in log_data: log_data['UserId'] = 0
            if 'GmID' not in log_data: log_data['GmID'] = 0
            if 'SubscriptionId' not in log_data: log_data['SubscriptionId'] = 0
            if 'OrgId' not in log_data: log_data['OrgId'] = 0
            if 'Cost' not in log_data: log_data['Cost'] = 0
            if 'PolicyId' not in log_data: log_data['PolicyId'] = 0
            if 'IsMedical' not in log_data: log_data['IsMedical'] = 0
            if 'LogType' not in log_data: log_data['LogType'] = 0
            if 'ContactId' not in log_data: log_data['ContactId'] = 0
            if 'PayType' not in log_data: log_data['PayType'] = ''
            if 'CouponCode' not in log_data: log_data['CouponCode'] = ''
            if 'SrcType' not in log_data: log_data['SrcType'] = ''
            if 'CurrencySymbol' not in log_data: log_data['CurrencySymbol'] = ''
            if 'oldClassId' not in log_data: log_data['oldClassId'] = ''
            if 'Note' not in log_data: log_data['Note'] = ''
            execution.execute(
                f"INSERT INTO actions_log (actions_log_user_id , actions_log_class_id ,actions_log_old_class_id, actions_log_subscription_id ,actions_log_org_id , actions_log_payment_type , actions_log_cost ,actions_log_coupon_code ,actions_log_note, actions_log_policy_id, actions_log_is_medical, actions_log_src_type ,actions_log_action_type_id ,actions_log_contact_id,actions_log_currency_symbol) Values ({log_data['UserId']},{log_data['GmID']},'{log_data['oldClassId']}',{log_data['SubscriptionId']},{log_data['OrgId']},'{log_data['PayType']}',{log_data['Cost']},'{log_data['CouponCode']}','{log_data['Note']}',{log_data['PolicyId']},{log_data['IsMedical']},'{log_data['SrcType']}',{log_data['LogType']},{log_data['ContactId']},'{log_data['CurrencySymbol']}');")

            log_id = execution.execute(
                f"SELECT action_log_id FROM actions_log WHERE actions_log_user_id='{log_data['UserId']}' and actions_log_class_id='{log_data['GmID']}' and actions_log_subscription_id='{log_data['SubscriptionId']}' and actions_log_org_id='{log_data['OrgId']}' and actions_log_payment_type='{log_data['PayType']}' and actions_log_cost='{log_data['Cost']}' and actions_log_note='{log_data['Note']}' and actions_log_policy_id={log_data['PolicyId']} and actions_log_is_medical={log_data['IsMedical']} and actions_log_src_type='{log_data['SrcType']}' and actions_log_action_type_id={log_data['LogType']} and actions_log_contact_id={log_data['ContactId']} and actions_log_currency_symbol='{log_data['CurrencySymbol']}';")
            if not log_id:
                raise Exception("Insertion Error")
            else:
                return log_id
    except Exception as e:
        return "something happened:" + e.__str__()
