import urllib
from datetime import datetime, timedelta, date
from urllib.parse import urlparse

import pytz
from dateutil.relativedelta import relativedelta

from database import config, execution, response
from utils import common_utils, player_utils, questionnaire_utils, organizer_utils, recur_utils
from utils.zoom import *

s3_bucket_url = config.s3_bucket_url
pytz.timezone("UTC")


def create_charge(fees, ply_id, pay_type, currency_id, ProjectKey, ProjectSecret, dev_id, class_id, tkn):
    try:
        if ply_id and ply_id > 0 and class_id and type(class_id) == int and class_id > 0 and fees and type(
                fees) == float and ProjectKey and ProjectSecret and dev_id and tkn:
            if float(fees) < 0.5:
                raise Exception('Minimum charge is $0.50 for payment to be made through Stripe')
            stripe_data = execution.execute(
                f"SELECT stripe_users_cust_id FROM stripe_users where stripe_users_ply_id={ply_id};")
            if str(stripe_data).__contains__('Something went wrong'):
                raise Exception(stripe_data)
            if not stripe_data or 'stripe_users_cust_id' not in stripe_data[0]:
                raise Exception('invalid stripe user')
            stripe_users_cust_id = stripe_data[0]['stripe_users_cust_id']
            Player_Name = execution.execute(
                f"SELECT CONCAT(ply_fname,' ',ply_lname) AS Player_Name FROM players WHERE ply_id={ply_id};")[0][
                "Player_Name"]
            if not stripe_users_cust_id or not pay_type:
                log_dict = {'UserId': ply_id, 'GmID': class_id,
                            'Note': f"{Player_Name} does not have a valid payment method linked to their account.",
                            'Fees': fees, 'Tkn': tkn, 'PayType': pay_type, 'CurrencyId': currency_id, 'LogType': 2}
                raise Exception(response.error(code=603,
                                               message="Please make sure you have added your payment details before proceeding. If you are using a discount code to pay, please make sure you have clicked APPLY ",
                                               data=log_dict))
            currency = execution.execute(
                f"SELECT currency_name , currency_commission_limit , stripe_perecnt_fees , stripe_fixed_fees FROM currencies WHERE currency_id={currency_id}")
            if str(currency).__contains__('Something went wrong'):
                raise Exception(currency)
            if not currency or 'currency_name' not in currency[0]:
                log_dict = {'UserId': ply_id, 'GmID': class_id, 'Note': "Currency Not Specified in Paid Game",
                            'Fees': fees, 'Tkn': tkn, 'PayType': pay_type, 'CurrencyId': currency_id, 'LogType': 0}
                raise Exception(
                    response.error(code=619, message="Currency Not Specified in Paid Game", data=log_dict))
            currency_name = currency[0]['currency_name']
            params = {
                "amount": float(fees),
                "currency": currency_name,
                "currency_id": int(currency_id),
                "customerID": stripe_users_cust_id,
                "PlyID": ply_id,
                "DevID": dev_id,
                "Tkn": tkn,
                "GmID": class_id,
                "ProjectKey": ProjectKey,
                "ProjectSecret": ProjectSecret
            }
            final_result = common_utils.game_curl('game/charge', params)
            if str(final_result).__contains__('callPayment') or str(final_result).__contains__('error'):
                raise Exception(final_result)
            return final_result
    except Exception as e:
        return e.__str__()


def class_type(class_id, org_id):
    # (offline, free,online(bundle or fees)) check if org connected to offline check if org connected to stripe
    # if offline and org is connected to offline
    # if online and org is connected to stripe
    try:
        if class_id and type(class_id) == int and class_id > 0 and org_id and type(org_id) == int and org_id > 0:
            Class_Type = execution.execute(f"SELECT gm_is_free , gm_payment_type FROM game WHERE gm_id={class_id}")
            if Class_Type and (Class_Type[0]['gm_is_free'] == 'y' or Class_Type[0]['gm_payment_type'] == 'onsite'):
                active_offline = execution.execute(
                    f"SELECT is_enabled FROM offline_payments WHERE next_billing_date >NOW() and admin_id={org_id}",
                    db_name=config.mysql_payment_db_name)
                if not active_offline or active_offline[0]['is_enabled'] == 0:
                    log_dict = {'GmID': class_id,
                                'Note': 'You cannot register for this class because your class organizer has not enabled offline payments yet',
                                'OrgID': org_id, 'LogType': 2}
                    raise Exception(response.error(code=610,
                                                   message="You cannot register for this class because your class organizer hasn't enabled offline payments yet",
                                                   data=log_dict))
                else:
                    return "offline"
            elif Class_Type and Class_Type[0]['gm_payment_type'] == 'stripe':
                connected = execution.execute(
                    f"SELECT stripe_users_account_id FROM stripe_users WHERE stripe_users_ply_id={org_id}")
                if connected and connected[0]['stripe_users_account_id'] == '':
                    log_dict = {'GmID': class_id,
                                'Note': 'You cannot pay or register for this class because class organizer has not connected to Stripe yet',
                                'OrgID': org_id, 'LogType': 2}
                    raise Exception(response.error(code=610,
                                                   message="You cannot pay or register for this class because class organizer hasn't connected to Stripe yet",
                                                   data=log_dict))
                elif connected and connected[0]['stripe_users_account_id'] != '':
                    return "online"
                else:
                    raise Exception("Org not found")
            else:
                log_dict = {}
                raise Exception(response.error(code=119, message='Invalid Game', data=log_dict))

        else:
            raise Exception("Something went wrong: ORG ID and CLASS ID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def add_attendee_to_class(class_id, ply_id):
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            check = execution.execute(
                f" SELECT gm_ply_id FROM gm_players WHERE gm_ply_gm_id ={class_id} AND gm_ply_ply_id = {ply_id};")
            if str(check).__contains__('Something went wrong'):
                raise Exception(check)
            if not check:
                insert = execution.execute(
                    f" INSERT INTO gm_players(gm_ply_gm_id,gm_ply_ply_id,gm_ply_status) VALUES ({class_id},{ply_id},'y');")
                if insert:
                    raise Exception(insert)
            elif 'gm_ply_id' in check[0]:
                update = execution.execute(
                    f"UPDATE gm_players SET gm_ply_status = 'y',gm_ply_refunded=0,gm_ply_leave = NULL,gm_ply_created=NOW() WHERE gm_ply_id ={check[0]['gm_ply_id']};")
                if update:
                    raise Exception(update)
                delete = execution.execute(
                    f"DELETE FROM gm_waitlist WHERE gm_wait_list_gm_id={class_id} AND gm_wait_list_ply_id={ply_id};")
                if delete:
                    raise Exception(delete)

        else:
            raise Exception("ply_id and class_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def class_capacity(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice, ProjectKey, ProjectSecret,
                   join_type, fees, currency_id):
    # check for class capacity if at it's maximum will go wait list else will go to join_class if capacity at it's maximum go to add_wait-list_attendee
    # elif offline go to add_attendee_to_class elif online go to check_pending_refund
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(
                class_id) == int and class_id >= 0 and org_id and type(org_id) == int and org_id >= 0:
            capacityQ = """
                           SELECT 
                           gm_max_players,
                           ( 
                               (
                                   SELECT COUNT(gm_ply_id)
                                   FROM gm_players
                                   WHERE gm_id = gm_ply_gm_id
                                   AND gm_ply_status = 'y'
                                   AND gm_ply_ply_id NOT IN ( SELECT guest_ply_id FROM guests WHERE guest_ply_id !=0 AND guest_gm_id = gm_id)
                               ) + (
                                   SELECT COUNT(guest_id)
                                   FROM guests
                                   WHERE gm_id = guest_gm_id
                               ) 
                           ) AS total
                           FROM game 
                           WHERE gm_id=%s
                       """
            capacityQ = capacityQ % class_id
            capacity = execution.execute(capacityQ)
            if str(capacity).__contains__("something happened:"):
                raise Exception(capacity)
            if capacity and capacity[0]['total'] >= capacity[0]['gm_max_players']:
                add_wait_list_attendee = add_waitlisted_attendee(class_id, ply_id)
                if add_wait_list_attendee:
                    raise Exception(add_wait_list_attendee)
                else:
                    return "you are in the waiting list"
            elif capacity and capacity[0]['total'] < capacity[0]['gm_max_players']:
                Class_type = class_type(class_id, org_id)
                if Class_type == "offline":
                    add_attendee_class = add_attendee_to_class(class_id, ply_id)
                    if add_attendee_class:
                        raise Exception(add_attendee_to_class)
                    else:
                        return "you are member now"
                elif Class_type == "online":
                    pending_refund_check = check_pending_refund(class_id, org_id, ply_id, pay_type, coupon_code, tkn,
                                                                dev_id, pay_choice, ProjectKey, ProjectSecret,
                                                                join_type, fees, currency_id)
                    if str(pending_refund_check).__contains__("something happened:"):
                        raise Exception(pending_refund_check)
                    else:
                        return pending_refund_check
                else:
                    raise Exception(Class_type)
            else:
                raise Exception("something went wrong with selection")
        else:
            raise Exception("Something went wrong: ORG ID and CLASS ID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def add_waitlisted_attendee(class_id, ply_id):
    # add user to the wait-list class
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            delete = execution.execute(
                f"DELETE FROM gm_waitlist WHERE gm_wait_list_gm_id ={class_id}AND gm_wait_list_ply_id = {ply_id};")
            if delete:
                raise Exception(delete)
            insert = execution.execute(
                f"INSERT INTO gm_waitlist (gm_wait_list_gm_id,gm_wait_list_ply_id) VALUES ({class_id},{ply_id});")
            if insert:
                raise Exception(insert)
        else:
            raise Exception("ply_id and class_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def check_pending_refund(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice, ProjectKey,
                         ProjectSecret, join_type, fees, currency_id):
    #  check for refund policy for this class that it is refund if replace , if user having pending refund for the **SAME**CLASS**
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            class_policy = execution.execute(f"SELECT gm_policy_id FROM game WHERE gm_id = {class_id}")
            if class_policy and class_policy[0]['gm_policy_id'] == 1:
                latest_user = execution.execute(
                    "SELECT gm_ply_ply_id FROM gm_players where gm_ply_refunded =0 and not gm_ply_leave is null"
                    f" and gm_ply_gm_id={class_id} order by gm_ply_leave Desc limit 1 ;")
                if not latest_user:
                    Paid_type = paid_type(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice,
                                          ProjectKey, ProjectSecret, join_type, fees, currency_id)
                    if str(Paid_type).__contains__("something happened:"):
                        raise Exception(Paid_type)
                    else:
                        return Paid_type
                elif latest_user and latest_user[0]['gm_ply_ply_id'] == ply_id:
                    # will curl if buying new bundle then will buy bundle without dec by 1 ,no new charge will happen
                    add_attendee_class = add_attendee_to_class(class_id, ply_id)
                    if add_attendee_class:
                        raise Exception(add_attendee_class)
                    else:
                        return "you are member now"
                elif latest_user and latest_user[0]['gm_ply_ply_id'] != ply_id:
                    Paid_type = paid_type(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice,
                                          ProjectKey, ProjectSecret, join_type, fees, currency_id)
                    if str(Paid_type).__contains__("something happened:"):
                        raise Exception(Paid_type)
                    else:
                        # if successfully paid then go to refund the last withdrawn player
                        refund_replaced = refund_if_replaced(class_id, ply_id, ProjectSecret, ProjectKey, pay_type)
                        if str(refund_replaced).__contains__("something happened:"):
                            raise Exception(refund_replaced)
                    return Paid_type
            elif class_policy and class_policy[0]['gm_policy_id'] != 1:
                Paid_type = paid_type(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice,
                                      ProjectKey, ProjectSecret, join_type, fees, currency_id)
                if str(Paid_type).__contains__("something happened:"):
                    raise Exception(Paid_type)
                else:
                    return Paid_type
            else:
                raise Exception("something went wrong with selection of policy")
        else:
            raise Exception("class_id and ply_id are required")
        # if pending user and buying new bundle then will buy bundle without dec by 1 ,no new charge will happen
        # elif not pending user or refund policy not (refund if replace)go to check online pay type
        # if came from paid type function success and refund policy is (refund if replace)
        # then go to refund function with refund policy refund if replace
    except Exception as e:
        return "something happened:" + e.__str__()


def paid_type(class_id, org_id, ply_id, pay_type, coupon_code, tkn, dev_id, pay_choice, ProjectKey, ProjectSecret,
              join_type=None, fees=0.0, currency_id=0):
    # check if using bundle, purchasing bundle or paying for this class only
    # using bundle or purchasing bundle
    # if pay_choice:
    # will go to curl to join_by_bundle(coupon_code,class_id,bundle_id,join_type,,ply_id,tkn,dev_id,new_client,org_id)
    # elif pay for this class only
    # if user used discount code then will go to apply coupon to fees
    # if there is remaining fees after discount or full, fees curl to pay charge enter(fees,ply_id,tkn,dev_id)
    # if user join by invitation then will go to delete invitation from db
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and org_id and type(
                org_id) == int and org_id >= 0 and class_id and class_id > 0:
            check_exist = execution.execute(
                f"SELECT contact_id FROM contacts where contact_org_id='{org_id}' and contact_ply_id='{ply_id}';")
            if check_exist:
                new_client = 0
            else:
                new_client = 1
        elif not pay_choice:
            log_dict = {}
            raise Exception(response.error(code=1000, message='something error.', data=log_dict))
        else:
            raise Exception('ply_id and org_id are required')
        if pay_choice > 0:
            params = {'bundle_id': pay_choice, 'join_type': join_type,
                      'class_id': class_id, 'ply_id': ply_id, 'dev_id': dev_id,
                      'coupon_code': coupon_code, 'tkn': tkn, 'ProjectKey': ProjectKey,
                      'ProjectSecret': ProjectSecret, 'new_client': new_client}
            BundleResponse = common_utils.bundle_curl('joinByBundle', params)
            if str(BundleResponse).__contains__('Something went wrong') or str(BundleResponse).__contains__(
                    'Error') or str(BundleResponse).__contains__('error'):
                log_dict = {}
                raise Exception(
                    response.error(code=BundleResponse['code'], message=BundleResponse['message'], data=log_dict))
            recurr_class = check_recurr_class(class_id, ply_id)
            if str(recurr_class).__contains__("something happened:"):
                raise Exception(recurr_class)
            else:
                inv_id = execution.execute(
                    f"SELECT inv_id FROM invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id} AND (inv_approve = 'y' or inv_approve = 'p')")
                if inv_id and not str(inv_id).__contains__("Something went wrong"):
                    delete = execution.execute(
                        f"DELETE from invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id}")
                    if delete:
                        raise Exception(delete)
                if new_client == 1:
                    player_details = execution.execute(
                        f"SELECT ply_fname,ply_lname,ply_email FROM players where ply_id={ply_id};")
                    if player_details and not str(player_details).__contains__(
                            'Something went wrong') and 'ply_fname' in player_details[0] \
                            and 'ply_lname' in player_details[0] and 'ply_email' in player_details[0]:

                        insert = execution.execute(
                            "INSERT INTO contacts(contact_org_id,contact_email,contact_ply_id,contact_f_name,contact_l_name)"
                            f" Values('{org_id}','{player_details[0]['ply_email']}','{ply_id}','{player_details[0]['ply_fname']}','{player_details[0]['ply_lname']}');")
                        if insert:
                            raise Exception(insert)
                    else:
                        raise Exception("error in getting player details")
                return recurr_class
        else:
            if coupon_code and coupon_code != 0:

                New_Fees, coupon_id = apply_coupon_to_fees(coupon_code, class_id, org_id, fees)
                if str(coupon_id).__contains__('something happened'):
                    raise Exception(
                        response.error(code=5000, message="Error in applying coupon. Try to join again please"))
                if New_Fees == fees:
                    raise Exception('Error in calculation of fees after discount')
                elif New_Fees == 0:
                    add_attendee_class = add_attendee_to_class(class_id, ply_id)
                    if str(add_attendee_class).__contains__("something happened:"):
                        raise Exception(add_attendee_class)
                    else:
                        insert = execution.execute(
                            f"INSERT INTO coupon_uses(coupon_id, ply_id, gm_id, subscription_id) VALUES ({coupon_id},{ply_id},{class_id},0);")
                        if insert:
                            raise Exception(insert)
                        recurr_class = check_recurr_class(class_id, ply_id)
                        if str(recurr_class).__contains__("something happened:"):
                            raise Exception(recurr_class)
                        else:
                            inv_id = execution.execute(
                                f"SELECT inv_id FROM invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id} AND (inv_approve = 'y' or inv_approve = 'p')")
                            if inv_id and not str(inv_id).__contains__("Something went wrong"):
                                delete2 = execution.execute(
                                    f"DELETE from invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id}")
                                if delete2:
                                    raise Exception(delete2)
                            if new_client == 1:
                                player_details = execution.execute(
                                    f"SELECT ply_fname,ply_lname,ply_email FROM players where ply_id={ply_id};")
                                if player_details and not str(player_details).__contains__(
                                        'Something went wrong') and 'ply_fname' in player_details[0] \
                                        and 'ply_lname' in player_details[0] and 'ply_email' in player_details[0]:
                                    insert2 = execution.execute(
                                        "INSERT INTO contacts(contact_org_id,contact_email,contact_ply_id,contact_f_name,contact_l_name)"
                                        f" Values('{org_id}','{player_details[0]['ply_email']}','{ply_id}','{player_details[0]['ply_fname']}','{player_details[0]['ply_lname']}');")
                                    if insert2:
                                        raise Exception(insert2)
                                else:
                                    raise Exception("error in getting player details")
                            return recurr_class
                else:
                    if type(pay_type) is not str or pay_type is None:
                        Player_Name = execution.execute((
                            f"SELECT CONCAT(ply_fname,' ',ply_lname) AS Player_Name FROM players WHERE ply_id={ply_id};"))[
                            0]["Player_Name"]
                        log_dict = {'UserId': ply_id, 'GmID': class_id, 'Fees': fees, 'Tkn': tkn, 'PayType': pay_type,
                                    'CurrencyId': currency_id, 'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret,
                                    'OrgId': org_id, 'CouponCode': coupon_code, 'JoinType': join_type, 'DevID': dev_id,
                                    'PayChoice': pay_choice,
                                    'Note': f'{Player_Name} does not have a valid payment method linked to their account.',
                                    'LogType': 2}
                        raise Exception(response.error(code=602, message="Missing Pay Type", data=log_dict))
                    else:
                        pay_result = create_charge(New_Fees, ply_id, pay_type, currency_id, ProjectKey, ProjectSecret,
                                                   dev_id, class_id, tkn)
                        if str(pay_result).__contains__('Something went wrong') or str(pay_result).__contains__(
                                'callPayment') or str(pay_result).__contains__('error'):
                            raise Exception(pay_result)
                        pay_id = execution.execute(
                            f"SELECT payment_id FROM payments.online_payments WHERE player_id = '{ply_id}' AND game_id = '{class_id}';",
                            db_name=config.mysql_payment_db_name)
                        if str(pay_id).__contains__('Something went wrong'):
                            raise Exception(pay_id)
                        if not pay_id or 'payment_id' not in pay_id:
                            raise Exception('problem in payments')
                        add_attendee_class = add_attendee_to_class(class_id, ply_id)
                        if str(add_attendee_class).__contains__("something happened:"):
                            raise Exception(add_attendee_class)
                        else:
                            insert3 = execution.execute(
                                f"INSERT INTO coupon_uses(coupon_id, ply_id, gm_id, subscription_id) VALUES ({coupon_id},{ply_id},{class_id},0);")
                            if insert3:
                                raise Exception(insert3)
                            recurr_class = check_recurr_class(class_id, ply_id)
                            if str(recurr_class).__contains__("something happened:"):
                                raise Exception(recurr_class)
                            else:
                                inv_id = execution.execute(
                                    f"SELECT inv_id FROM invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id} AND (inv_approve = 'y' or inv_approve = 'p')")
                                if inv_id and not str(inv_id).__contains__(
                                        "Something went wrong") and 'inv_id' in inv_id:
                                    delete3 = execution.execute(
                                        f"DELETE from invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id}")
                                    if delete3:
                                        raise Exception(delete3)
                                if new_client == 1:
                                    player_details = execution.execute(
                                        f"SELECT ply_fname,ply_lname,ply_email FROM players where ply_id={ply_id};")
                                    if player_details and not str(player_details).__contains__(
                                            'Something went wrong') and 'ply_fname' in player_details[0] and \
                                            'ply_lname' in player_details[0] and 'ply_email' in player_details[0]:
                                        insert4 = execution.execute(
                                            "INSERT INTO contacts(contact_org_id,contact_email,contact_ply_id,contact_f_name,contact_l_name)"
                                            f" Values('{org_id}','{player_details[0]['ply_email']}','{ply_id}','{player_details[0]['ply_fname']}','{player_details[0]['ply_lname']}');")
                                        if insert4:
                                            raise Exception(insert4)
                                    else:
                                        raise Exception("something happened: error in getting player details")
                                return recurr_class
            else:
                pay_result = create_charge(fees, ply_id, pay_type, currency_id, ProjectKey, ProjectSecret,
                                           dev_id, class_id, tkn)
                if str(pay_result).__contains__('Something went wrong') or str(pay_result).__contains__(
                        'callPayment') or str(pay_result).__contains__('error'):
                    raise Exception(pay_result)
                pay_id = execution.execute(
                    f"SELECT payment_id FROM payments.online_payments WHERE player_id = '{ply_id}' AND game_id = '{class_id}';",
                    db_name=config.mysql_payment_db_name)
                if str(pay_id).__contains__('Something went wrong'):
                    raise Exception(pay_id)
                if not pay_id or 'payment_id' not in pay_id:
                    raise Exception('problem in payments')
                add_attendee_class = add_attendee_to_class(class_id, ply_id)
                if str(add_attendee_class).__contains__("something happened:"):
                    raise Exception(add_attendee_class)
                else:
                    recurr_class = check_recurr_class(class_id, ply_id)
                    if str(recurr_class).__contains__("something happened:"):
                        raise Exception(recurr_class)
                    else:
                        inv_id = execution.execute(
                            f"SELECT inv_id FROM invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id} AND (inv_approve = 'y' or inv_approve = 'p')")
                        if inv_id and 'inv_id' in inv_id:
                            delete4 = execution.execute(
                                f"DELETE from invitations WHERE inv_gm_id = {class_id} AND inv_ply_to_id = {ply_id}")
                            if delete4:
                                raise Exception(delete4)
                        elif str(inv_id).__contains__(inv_id):
                            raise Exception(inv_id)
                        if new_client == 1:
                            player_details = execution.execute(
                                f"SELECT ply_fname,ply_lname,ply_email FROM players where ply_id={ply_id};")
                            if player_details:
                                insert5 = execution.execute(
                                    "INSERT INTO contacts(contact_org_id,contact_email,contact_ply_id,contact_f_name,contact_l_name)"
                                    f" Values('{org_id}','{player_details[0]['ply_email']}','{ply_id}','{player_details[0]['ply_fname']}','{player_details[0]['ply_lname']}');")
                                if insert5:
                                    raise Exception(insert5)
                            else:
                                raise Exception("error in getting player details")
                        return recurr_class
    except Exception as e:
        return e.__str__()


def apply_coupon_to_fees(coupon_code, class_id, org_id, fees):
    # apply discount if remaining fees then return the remaining as fees to enter pay charge
    try:
        if org_id and class_id and coupon_code and fees and type(coupon_code) == str and type(org_id) == int and type(
                class_id) == int and type(fees) == float \
                and org_id >= 0 and class_id >= 0 and fees >= 0:
            coupon_data = execution.execute(
                f"SELECT coupons.id as ID,code,type, discount, start_date, end_date,all_subscriptions, all_games, subscription_id, gm_id,uses_per_coupon, uses_per_ply FROM coupons LEFT JOIN coupon_products ON coupon_products.coupon_id = coupons.id WHERE (all_games=1 or gm_id= {class_id}) and status=1 and BINARY coupons.code = '{coupon_code}' and admin_id={org_id} and end_date_time >= now() ORDER BY all_subscriptions DESC, all_games DESC ;")
            if coupon_data and coupon_data[0]['ID']:
                # if coupon type is fixed
                if coupon_data[0]['type'] == 'f':
                    newFees = fees - float(coupon_data['discount'])
                    if float(newFees) < 0:
                        newFees = 0
                # if coupon type is percentage
                elif coupon_data[0]['type'] == 'p':
                    discount = float((coupon_data[0]['discount'] / 100) * fees)
                    newFees = fees - float(discount)
                    if float(newFees) < 0:
                        newFees = 0
                else:
                    raise Exception("coupon type not correct")
                return newFees, coupon_data[0]['ID']
            else:
                log_dict = {}
                raise Exception(response.error(code=5000, message="Error in applying coupon. Try to join again please",
                                               data=log_dict))
        else:
            raise Exception("org_id ,class_id,coupon_code and fees are required")
    except Exception as e:
        return "", "something happened:" + e.__str__()


def check_recurr_class(class_id, ply_id):
    # this function returns False if class is not recurring - else will return recur days if user didn't join class of this set before
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            zoom_details_check = check_zoom_details(class_id)
            if str(zoom_details_check).__contains__("something happened:"):
                raise Exception(zoom_details_check)
            else:
                recur = execution.execute(f"SELECT gm_recurr_id, gm_recurr_times FROM game WHERE gm_id= {class_id}")
                if recur and 'gm_recurr_id' in recur[0] and 'gm_recurr_times' in recur[0]:
                    # individual class
                    if recur[0]['gm_recurr_id'] == 0 and recur[0]['gm_recurr_times'] == 0:
                        is_recurred = False
                    # parent class
                    elif recur[0]['gm_recurr_id'] == 0 and recur[0]['gm_recurr_times'] == 1:
                        child = execution.execute(
                            f"SELECT gm_id FROM gm_players AS gm INNER JOIN game AS g ON gm.gm_ply_gm_id=g.gm_id WHERE gm_ply_ply_id={ply_id} AND g.gm_recurr_id={class_id};")
                        if not child:
                            recurr_days = execution.execute(
                                f"SELECT gm_recurr_days_times FROM game WHERE gm_id={class_id}")
                            is_recurred = recurr_days
                        else:
                            raise Exception('error in recurr')
                    # child class
                    elif recur[0]['gm_recurr_id'] != 0:
                        child = execution.execute(
                            f"SELECT gm_id FROM gm_players AS gm INNER JOIN game AS g ON gm.gm_ply_gm_id=g.gm_id WHERE gm_ply_ply_id={ply_id} AND g.gm_recurr_id={recur[0]['gm_recurr_id']};")

                        if not child:
                            recurr_days = execution.execute(
                                f"SELECT gm_recurr_days_times FROM game WHERE gm_id={recur[0]['gm_recurr_id']}")
                            is_recurred = recurr_days
                        else:
                            raise Exception('error in recurr')
                    else:
                        raise Exception("class have something wrong")
                else:
                    raise Exception("Class Not Found")
        else:
            raise Exception("Enter valid class_id and ply_id")
    except Exception as e:
        return "something happened:" + e.__str__()
    else:
        return {"recur": is_recurred, "zoom_details": check_zoom_details}


def check_zoom_details(class_id):
    # if type is zoom then we will view password and link for the meeting
    try:
        if class_id and type(class_id) == int and class_id >= 0:
            check_class_is_zoom = execution.execute(
                f"SELECT zoom_url,zoom_meeting_id,zoom_pwd FROM game where attend_type='zoom' and gm_id='{class_id}';")
            if check_class_is_zoom:
                return {"zoom_url": check_class_is_zoom[0]['zoom_url'],
                        "zoom_meeting_id": check_class_is_zoom[0]['zoom_meeting_id'],
                        "zoom_pwd": check_class_is_zoom[0]['zoom_pwd']}
            else:
                return "in person class"
        else:
            raise Exception("class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


#                                                                     *refund function part*

def check_abs_type(class_id, ply_id, source='web', ProjectKey=None, ProjectSecret=None):
    # check remove or withdrawn
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            abs_type = execution.execute(
                f"SELECT gm_ply_removed_by_admin from gm_players WHERE gm_ply_leave is not null and gm_ply_status='r' and gm_ply_ply_id='{ply_id}' and gm_ply_gm_id='{class_id}';")
            if abs_type and abs_type[0]['gm_ply_removed_by_admin'] == 1:
                complete_refund = check_type_payment(class_id, ply_id, source, ProjectKey, ProjectSecret)
                if str(complete_refund).__contains__("something happened:"):
                    raise Exception(response.error(complete_refund))
                else:
                    return response.success(complete_refund)
            elif abs_type and abs_type[0]['gm_ply_removed_by_admin'] == 0:
                refund_policy_check = check_refund_policy(class_id, ply_id, source, ProjectKey, ProjectSecret)
                if str(refund_policy_check).__contains__("something happened:"):
                    raise Exception(response.error(refund_policy_check))
                else:
                    return response.success(refund_policy_check)
            else:
                raise Exception(response.error("error in getting gm_ply_removed_by_admin"))
        else:
            raise Exception(response.error("ply_id and class_id are required"))
    except Exception as e:
        return e


def update_player_asrefunded(ply_id, class_id):
    # update player as refunded in gm_players
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            check_refund = execution.execute(
                f"SELECT gm_ply_id FROM gm_players WHERE gm_ply_refunded=0 and gm_ply_gm_id={class_id} and gm_ply_ply_id={ply_id};")
            if check_refund and not str(check_refund).__contains__('Something went wrong'):
                update_player_gm = execution.execute(
                    f"UPDATE gm_players SET gm_ply_refunded=1 WHERE gm_ply_ply_id={ply_id} AND gm_ply_gm_id = {class_id};")
                if update_player_gm:
                    raise Exception(update_player_gm)
            else:
                raise Exception("something went wrong this user already refunded")
        else:
            raise Exception("class_id and ply_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def check_refund_policy(class_id, ply_id, ProjectKey, ProjectSecret, source='web'):
    # check refund policy
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            refund_type = execution.execute(
                f"SELECT gm_policy_id, gm_ply_refunded FROM game JOIN gm_players ON gm_id = gm_ply_gm_id WHERE gm_id = {class_id} AND gm_ply_ply_id={ply_id};")
            # if no refund will end the process without refund
            if refund_type and (refund_type[0]['gm_policy_id'] == 2 or refund_type[0]['gm_policy_id'] == 0):
                return {"noteText": "This policy No Refund"}
            # if refund 100% with time
            elif refund_type and refund_type[0]['gm_policy_id'] in range(5, 11):
                fully_refunded_time = fully_refunded_per_time(class_id=class_id,
                                                              policy_id=refund_type[0]['gm_policy_id'])
                if fully_refunded_time is True:
                    check_payment_type = check_type_payment(class_id, ply_id, source, ProjectKey, ProjectSecret)
                    if str(check_payment_type).__contains__("something happened:"):
                        raise Exception(check_payment_type)
                    else:
                        return check_payment_type
                elif fully_refunded_time['GameRefundable'] is False:
                    return fully_refunded_time
                else:
                    raise Exception(fully_refunded_time)
            #  refund if replaced
            elif refund_type and refund_type[0]['gm_policy_id'] == 1:
                refund_replaced = refund_if_replaced(class_id, ply_id, source, ProjectKey, ProjectSecret)
                if str(refund_replaced).__contains__("something happened:"):
                    raise Exception(refund_replaced)
                else:
                    return refund_replaced
            else:
                raise Exception("something went wrong in the selection")
        else:
            raise Exception("class_id and ply_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def fully_refunded_per_time(policy_id, class_id):
    # check if the time exceeds the refunded policy time or no
    try:
        if policy_id and type(policy_id) == int and policy_id >= 0 and class_id and type(
                class_id) == int and class_id >= 0:
            hours_text = execution.execute(f"SELECT policy_title FROM policy where policy_id={policy_id};")
            hours = timedelta(hours=int(
                hours_text[0]['policy_title'].replace("100 Percent (", '').replace(" hours)", '').replace("hour)",
                                                                                                          ''))).total_seconds()
            current_time = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            gm_times = execution.execute(f"SELECT gm_utc_datetime from game where gm_id='{class_id}';")
            if gm_times and "gm_utc_datetime" in gm_times[0]:
                difference = (gm_times[0]['gm_utc_datetime'] - current_time).total_seconds()
                if difference < hours:
                    return {"GameRefundable": False,
                            "noteText": f"User has been no refund because the policy is full refund before({hours} hours), but the game will start less than {hours} hours"}
                elif difference >= hours:
                    return True
                else:
                    raise Exception("Something went wrong in the calculations")
            else:
                raise Exception("gm_utc_datetime not found")
        else:
            raise Exception("policy id and class_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def refund_if_replaced(class_id, ply_id, ProjectKey, ProjectSecret, source='web'):
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(class_id) == int and class_id >= 0:
            # if check capacity is not full go to complete_refund
            capacity = execution.execute(
                f"SELECT game.gm_max_players,count(gm_players.gm_ply_id) as total from game Left Join gm_players on game.gm_id=gm_players.gm_ply_gm_id where gm_id={class_id};")
            if capacity and capacity[0]['total'] < capacity[0]['gm_max_players']:
                check_payment_type = check_type_payment(class_id, ply_id, source, ProjectKey, ProjectSecret)
                if str(check_payment_type).__contains__("something happened:"):
                    raise Exception(check_payment_type)
                else:
                    return check_payment_type
            # if full then go to refund the latest withdrawn user and user is different from the last user so refund the last withdrawn user
            elif capacity and capacity[0]['total'] >= capacity[0]['gm_max_players']:
                latest_user = execution.execute(
                    f"SELECT gm_ply_ply_id , gm_ply_pay_type FROM gm_players where gm_ply_refunded = 0 and not gm_ply_leave is null and gm_ply_gm_id={class_id} order by gm_ply_leave Desc limit 1")
                if latest_user and latest_user[0]['gm_ply_ply_id'] != ply_id:
                    check_payment_type = check_type_payment(class_id, latest_user[0]['gm_ply_ply_id'], source,
                                                            ProjectKey, ProjectSecret)
                    if str(check_payment_type).__contains__("something happened:"):
                        raise Exception(check_payment_type)
                    else:
                        return check_payment_type
                else:
                    return {"noteText": "User will be refunded if someone else takes your spot"}
        else:
            raise Exception("player id and class_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def check_type_payment(class_id, ply_id, source='web', ProjectKey=None, ProjectSecret=None):
    # check type of  payment(pay this class only or bundle) from check subscription id if exist then will be bundle
    # else then will be by stripe checking actions_log_cost from action_logs to know how much did he pay
    try:
        if ply_id and type(ply_id) == int and ply_id >= 0 and class_id and type(
                class_id) == int and class_id >= 0:
            check_payment_type = execution.execute(
                f"SELECT bundle_id FROM games_subscriptions left join bundles.bundles_subscriptions ON bundles_subscriptions.id=games_subscriptions.subscription_id"
                f" where game_id={class_id} and member_id={ply_id};")
            if check_payment_type and check_payment_type[0]['bundle_id'] != 0:
                # if bundle call updatePlayerCredit
                params = {'bundle_id': check_payment_type[0]['bundle_id'], 'class_id': class_id, 'ply_id': ply_id,
                          'process': '+', 'source': source, 'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret}
                BundleResponse = common_utils.bundle_curl('updatePlayerCredit', params)
                if str(BundleResponse).__contains__('Something went wrong') or str(BundleResponse).__contains__(
                        'Error') or str(BundleResponse).__contains__('error'):
                    raise Exception(BundleResponse)
                update_player_refunded = update_player_asrefunded(ply_id, class_id)
                if str(update_player_refunded).__contains__("something happened:"):
                    raise Exception(update_player_refunded)
                else:
                    return {"bundle_data": BundleResponse, "noteText": "User has been refunded via class credit"}
            elif not check_payment_type:
                abs_type = execution.execute(
                    f"SELECT gm_ply_removed_by_admin from gm_players WHERE gm_ply_leave is not null and gm_ply_status='r' and gm_ply_ply_id={ply_id} and gm_ply_gm_id={class_id};")
                if abs_type and not str(abs_type).__contains__('Something went wrong'):
                    # if pay for this class only then check that the cost user pay not equal to 0 then will go to (direct refund or make refund) in payment module
                    params = {"GmID": class_id, "PlyID": ply_id, "ply_withdraw": abs_type[0]['gm_ply_removed_by_admin'],
                              "ProjectKey": ProjectKey, "ProjectSecret": ProjectSecret}
                    curl_output = common_utils.game_curl('game/refund', params)
                    if str(curl_output).__contains__('callPayment') or str(curl_output).__contains__('error'):
                        update_player_refunded = update_player_asrefunded(ply_id, class_id)
                        if str(update_player_refunded).__contains__("something happened:"):
                            raise Exception(update_player_refunded)
                        else:
                            return {"payment_output": curl_output, "noteText": "User has been fully refunded"}
                    else:
                        raise Exception(curl_output)
                else:
                    raise Exception("something went wrong with payment type")
        else:
            raise Exception("player id and class_id are required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_game_player_data(game_id, player_id, ProjectKey, ProjectSecret, tkn, dev_id, gmcals=0):
    """
         desc: get main info for the game and player
         input: game_id,player_id

         output:result[GmID,GmT,OrgID,OrgName,OrgEmail,OrgGdr,OrgImg,OrgImgThumb,OrgBusiness,STypeID,STypeName,CourtID,CourtT
         ,LevelID,LevelT,ImgName,Gdr,Age,MinPly,MaxPly,GmOrgDate,STime,ETime,timeZone,CountryID,CountryIso,CountryName,CityID,CityName,Lat,Long,LocDesc,
         Scope,HasGlly,Desc,Req,Notes,Rules,Kits,showMem,IsFree,PayType,attendType,zoomUrl,zoomMeetingId,zoomPwd,PlyBirthDate,gm_s3_status,GmRecurrDaysTimes,FeedPlyID
         ,RecurrPeriod,GmDate,FeedStatus,STypeImg,GmImg,GmImgThumb,Fees,CurrencyName,PolicyID,PolicyT,CurrencyID,RecurrID,ParentState,IsStopRecurred,GmDist,RenewID,Symbol,
         Day,SSTime,EETime,UTCDateTime,Subscriptions,PlySubscriptions,InvalidPlySubscriptions,validJoinSubscriptions,orgOfflineStatus,EndRecurr,Days,gm_time_zone]

    """
    try:
        if not gmcals:
            game_data = execution.execute(f"SELECT gm_id as GmID,gm_title as GmT,gm_org_id as OrgID,ply_email as OrgEmail,CONCAT(ply_fname,' ',ply_lname) AS OrgName,ply_gender as OrgGdr,ply_business as OrgBusiness,gm_s_type_id as STypeID,gm_s_type_name as STypeName,court_id as CourtID,court_title as CourtT,\
                    level_id as LevelID,level_title as LevelT,gm_img as ImgName,gm_gender as Gdr,gm_min_players as MinPly,gm_max_players as MaxPly,gm_start_time as STime,gm_end_time as ETime,\
                    gm_time_zone as timeZone,country_id as CountryID,iso as CountryIso,country_name as CountryName,gm_city_id as CityID,city_name as CityName,\
                    gm_loc_lat as Lat,gm_display_org as DisOrg,gm_loc_long as 'Long',gm_loc_desc as LocDesc,gm_scope as Scope,gm_has_gallery as HasGlly,gm_desc as 'Desc',gm_requirements as Req,gm_notes as Notes,\
                    gm_rules as Rules,gm_kits as Kits,gm_is_free as IsFree,attend_type as attendType,zoom_url as zoomUrl,zoom_meeting_id as zoomMeetingId,ply_brithdate as PlyBirthDate,\
                    gm_recurr_days_times as GmRecurrDaysTimes,gm_payment_type as PayType,gm_showMem as showMem,currency_id as CurrencyID,currencies.currency_name as CurrencyName,currency_symbol,gm_policy_id as PolicyID,policy_title as PolicyT,\
                    gm_recurr_id as RecurrID,gm_is_stop_recurred as IsStopRecurred,gm_recurr_times,gm_recurr_type,gm_renew_id as RenewID,\
                    ply_img,s3_profile,gm_s3_status,gm_available_to_join as GmIsAvailableToJoin,gm_date as GmOrgDate,gm_img,gm_fees as Fees,gm_utc_datetime as UTCDateTime,CONCAT('gm_s_types/',gm_s_type_img) as STypeImg,(CASE WHEN ((gm_org_id = {int(player_id)} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP) OR (gm_org_id != {int(player_id)} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP)) THEN 'n' ELSE 'y' END) AS IsHis,ply_country_id,s3_profile FROM game FULL JOIN players org ON gm_org_id =org.ply_id left JOIN gm_s_types ON gm_sub_type_id = gm_s_type_id\
                    LEFT JOIN court ON gm_court_id = court_id\
                    LEFT JOIN level ON gm_level_id = level_id\
                    LEFT JOIN country ON gm_country_id = country_id\
                    LEFT JOIN city ON gm_city_id = city_id\
                    LEFT JOIN currencies ON gm_currency_symbol = currency_id\
                    LEFT JOIN `policy` ON gm_policy_id = policy_id WHERE gm_id = {game_id} AND (gm_status IS NULL OR gm_status NOT LIKE '%deleted%')")
        else:

            game_data = execution.execute(f"SELECT gm_time_zone as timeZone,gm_available_to_join as GmIsAvailableToJoin,gm_utc_datetime as UTCDateTime,attend_type as attendType,s3_profile ,gm_s3_status,gm_payment_type as PayType,gm_recurr_id as RecurrID,gm_id , gm_title , gm_org_id as OrgID , ply_fname , ply_lname , ply_gender , ply_img , gm_display_org , gm_s_type_id , gm_s_type_name,\
                                              gm_s_type_img , court_id , court_title , level_id , level_title , gm_img , gm_gender , gm_min_players , gm_max_players ,\
                                              gm_status , gm_date as GmOrgDate , gm_start_time as STime, gm_end_time as ETime , gm_utc_datetime , gm_end_pause , gm_city_id , city_name , gm_loc_lat , gm_loc_long,\
                                              gm_loc_desc , gm_scope , gm_has_gallery , gm_desc , gm_fees as Fees , gm_currency_symbol , currency_symbol , currency_id ,\
                                              gm_requirements , gm_notes , gm_rules , gm_kits , gm_showMem as showMem , gm_is_free as IsFree , gm_payment_type , gm_policy_id , policy_title , zoom_url,\
                                             (CASE WHEN ((gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP) THEN 'n' ELSE 'y' END)AS IsHis,\
                                             gm_reqQues , gm_status , gm_recurr_id , gm_is_stop_recurred , gm_recurr_times , gm_recurr_type , gm_renew_id , country_id,iso,country_name\
                                    FROM gm_players\
                                            LEFT JOIN game ON  gm_id=gm_ply_gm_id\
                                            LEFT JOIN players ON  gm_org_id = ply_id\
                                            LEFT JOIN gm_s_types ON  gm_sub_type_id = gm_s_type_id\
                                            LEFT JOIN court ON gm_court_id = court_id\
                                            LEFT JOIN level ON  gm_level_id = level_id\
                                            LEFT JOIN country ON gm_country_id = country_id\
                                            LEFT JOIN city ON gm_city_id = city_id\
                                            LEFT JOIN policy ON gm_policy_id = policy_id\
                                            LEFT JOIN currencies ON currency_id=gm_currency_symbol\
                                            LEFT JOIN ply_bans on (ply_ban_ply_frm=gm_org_id and ply_ban_ply_to={player_id})or(ply_ban_ply_frm={player_id} and ply_ban_ply_to=gm_org_id)\
                                     WHERE\
                                     ply_ban_id IS NULL AND\
                                     gm_ply_ply_id = {player_id}\
                                     AND gm_ply_gm_id > 0 AND gm_status IS NULL\
                                     AND gm_pid=1\
                                     AND gm_ply_status = 'y'\
                                     AND (CASE\
                                         WHEN attend_type = 'zoom' THEN  DATE(CONVERT_TZ(gm_utc_datetime, 'UTC', 'Africa/Cairo')) LIKE '%%'\
                                         WHEN attend_type != 'zoom' THEN gm_date LIKE '%%'\
                                     END)\
                                     ORDER BY gm_date DESC,gm_start_time DESC\
                                     LIMIT 0,50")

        if not game_data:
            raise Exception('game data not found')
        if str(game_data).__contains__('Something went wrong'):
            raise Exception(game_data)
        game_data[0]['FeedStatus'] = ""
        game_data[0]['FeedPlyID'] = ""
        game_data[0]['GmDist'] = ""
        game_data[0]['zoomPwd'] = ""
        game_data[0]['RecurrID'] = game_data[0]['RecurrID'] if game_data[0]['RecurrID'] != '' else 0
        if game_data[0]['showMem'] == 1:
            game_data[0]['showMem'] = 'True'
        else:
            game_data[0]['showMem'] = 'False'
        if 'gm_recurr_times' in game_data[0] and 'gm_recurr_type' in game_data[0]:
            if game_data[0]['gm_recurr_type'] and game_data[0]['gm_recurr_times'] > 0:
                game_data[0]['ParentState'] = 'p'
        elif 'RecurrID' in game_data[0]:
            if int(game_data[0]['RecurrID']) > 0:
                game_data[0]['ParentState'] = 'c'
        game_data[0]['PayType'] = str(game_data[0]['PayType']).capitalize()
        game_data[0]['gm_s3_status'] = game_data[0]['gm_s3_status'] if game_data[0]['gm_s3_status'] else '0'
        game_data[0]['Fees'] = float(game_data[0]['Fees']) if float(game_data[0]['Fees']) > 0 else 0
        if game_data[0]['s3_profile'] == 1:
            game_data[0]['OrgImg'] = s3_bucket_url + "/upload/ply/" + str(game_data[0]['ply_img'])
            game_data[0]['ply_img'] = str(game_data[0]['ply_img']).replace("profile", "profile/thumb")
            game_data[0]['OrgImgThumb'] = s3_bucket_url + "/upload/ply/" + str(game_data[0]['ply_img'])
        else:
            game_data[0]['OrgImg'] = s3_bucket_url + "/backup/upload/ply/" + str(game_data[0]['ply_img'])
            game_data[0]['OrgImgThumb'] = s3_bucket_url + "/backup/upload/ply/" + str(game_data[0]['ply_img'])
        if game_data[0]['gm_s3_status'] == 1:
            game_data[0]['GmImg'] = s3_bucket_url + str(game_data[0]['gm_img'])
            game_data[0]['gm_img'] = str(game_data[0]['gm_img']).replace("classes", "classes/thumb")
            game_data[0]['GmImgThumb'] = s3_bucket_url + str(game_data[0]['gm_img'])
        else:
            game_data[0]['GmImg'] = s3_bucket_url + "/images/upload/gm/" + str(game_data[0]['gm_img'])
            game_data[0]['GmImgThumb'] = s3_bucket_url + "/images/upload/gm/thumb/" + str(game_data[0]['gm_img'])
        if game_data[0]['OrgID'] == player_id:
            game_data[0]['Symbol'] = game_data[0]['currency_symbol']
        elif game_data[0]['attendType'] == 'zoom':
            game_data[0]['Symbol'] = game_data[0]['CurrencyName']
        if game_data[0]['gm_recurr_type'] and game_data[0]['gm_recurr_type'] != "" and game_data[0][
            'gm_recurr_type'] == 0:
            start_month = game_data[0]['GmOrgDate'].month
            end_date = game_data[0]['gm_recurr_type'].split('_')[1]
            end_month = int(end_date.split('-')[1])
            if end_month - start_month > 12:
                game_data[0]['RecurrPeriod'] = 0
            else:
                game_data[0]['RecurrPeriod'] = end_month - start_month
        ply_time_zone = execution.execute(f"SELECT id,timezone FROM ply_timezone WHERE player_id={player_id}")
        if str(ply_time_zone).__contains__('Something went wrong'):
            raise Exception(ply_time_zone)
        if ply_time_zone and ply_time_zone[0]['id'] and int(ply_time_zone[0]['id']) > 0 and ply_time_zone[0][
            'timezone']:
            time_zone = urllib.parse.unquote(urllib.parse.unquote(ply_time_zone[0]['timezone']))
            if time_zone:
                updated_utc_date = str(game_data[0]['UTCDateTime'])
                updated_utc_date = datetime.strptime(updated_utc_date, '%Y-%m-%d %H:%M:%S')
                timezone = pytz.timezone(time_zone)

                updated_utc_date = updated_utc_date.replace(tzinfo=timezone)
                game_data[0]['GmDate'] = updated_utc_date.strftime('%Y-%m-%d')
                game_data[0]['SSTime'] = updated_utc_date.strftime('%I:%M %p')
                game_data[0]['Day'] = updated_utc_date.strftime("%A")
                if int(game_data[0]['ETime']) > 0:
                    updated_time = updated_utc_date + timedelta(minutes=game_data[0]['ETime'])
                    game_data[0]['EETime'] = str(updated_time.strftime("%I:%M %p"))
        else:
            game_data[0]['Day'] = game_data[0]['GmOrgDate'].strftime("%A")
            start_24 = datetime.strptime(str(game_data[0]['STime']), "%H:%M:%S")
            game_data[0]['SSTime'] = start_24.strftime("%I:%M %p")
            if int(game_data[0]['ETime']) > 0:
                string_date = str(game_data[0]['GmOrgDate']) + ' ' + str(game_data[0]['STime'])
                endtime = datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
                updated_time = endtime + timedelta(minutes=game_data[0]['ETime'])

                game_data[0]['EETime'] = str(updated_time.strftime("%I:%M %p"))
            else:
                # game_data[0]['EETime'] = str(game_data[0]['ETime']).strftime("%I:%M %p")
                game_data[0]['EETime'] = 0
            game_data[0]['GmDate'] = game_data[0]['GmOrgDate']
        check_exist = execution.execute(
            f"SELECT contact_id FROM contacts where contact_org_id={game_data[0]['OrgID']} and contact_ply_id={player_id}")
        if check_exist:
            new_client = 0
        else:
            new_client = 1
        params = {'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret, 'new_client': new_client, 'dev_id': dev_id,
                  'ply_id': player_id,
                  'org_id': game_data[0]['OrgID'], 'tkn': tkn, 'class_id': game_id,
                  'class_datetime': str(game_data[0]['UTCDateTime'])}
        # commented during testing only
        subscriptions_data = common_utils.bundle_curl('playerBundles', params)
        if str(subscriptions_data).__contains__('error'):
            raise Exception(subscriptions_data)
        game_data[0]['Subscriptions'] = subscriptions_data['orgBundles'] if subscriptions_data['orgBundles'] else ''
        game_data[0]['plySubscriptions'] = subscriptions_data['plySubscriptions'] if subscriptions_data[
            'plySubscriptions'] else ''
        game_data[0]['validJoinSubscriptions'] = subscriptions_data['validJoinSubscriptions'] if subscriptions_data[
            'validJoinSubscriptions'] else ''
        game_data[0]['invalidPlySubscriptions'] = subscriptions_data['invalidPlySubscriptions'] if subscriptions_data[
            'invalidPlySubscriptions'] else ''
        if game_data[0]['PayType'].lower() == 'onsite' and game_data[0]['IsFree'].lower() == 'y':
            params = {'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret, 'DevID': dev_id,
                      'PlyID': game_data[0]['OrgID'], 'Tkn': tkn}
            status = common_utils.game_curl('offline/admin/status', params)
            game_data[0]['orgOfflineStatus'] = status['Status']
        else:
            game_data[0]['orgOfflineStatus'] = ''
        recurr_arr = ''
        if game_data[0]['gm_recurr_type'] and game_data[0]['RecurrID'] == 0:
            recurr_arr = game_data[0]['gm_recurr_type'].split('_')
        elif game_data[0]['RecurrID'] == 0:
            recurr_data = execution.execute(
                f"SELECT gm_recurr_type FROM game WHERE gm_id = {int(game_data[0]['RecurrID'])}")
            if str(recurr_data).__contains__('Something went wrong'):
                raise Exception(recurr_data)
            if recurr_data:
                recurr_arr = recurr_data[0]['gm_recurr_type'].split('_')
        if recurr_arr:
            game_data[0]['EndRecurr'] = recurr_arr[1]
            if len(recurr_arr) > 2:
                Days = '{'
                for i in range(2, len(recurr_arr)):
                    if i == len(recurr_arr) - 1:
                        Days = Days + recurr_arr[i] + '}'
                    else:
                        Days = Days + recurr_arr[i] + '.'

                game_data[0]['Days'] = Days

        else:
            game_data[0]['Days'] = ''
            game_data[0]['EndRecurr'] = ''
        if game_data[0]['timeZone']:

            utcnow = pytz.timezone('utc').localize(datetime.utcnow())  # generic time
            here = utcnow.astimezone(pytz.timezone(str(game_data[0]['timeZone']))).replace(tzinfo=None)
            there = utcnow.astimezone(pytz.timezone('utc')).replace(tzinfo=None)
            offset = relativedelta(here, there)
            if str(offset.hours).__contains__('-'):
                hour = str(offset.hours).split('-')[1]

                if int(hour) > 9:
                    game_data[0]['gm_time_zone'] = "(Utc-" + str(hour) + ":00)"
                else:

                    game_data[0]['gm_time_zone'] = "(Utc-0" + str(hour) + ":00)"
            else:
                if int(offset.hours) > 9:
                    game_data[0]['gm_time_zone'] = "(Utc+" + str(offset.hours) + ":00)"
                else:
                    game_data[0]['gm_time_zone'] = "(Utc+0" + str(offset.hours) + ":00)"
        game_data[0]['STime'] = game_data[0]['STime'].__str__()
        game_data[0]['GmOrgDate'] = game_data[0]['GmOrgDate'].__str__()
        game_data[0]['UTCDateTime'] = game_data[0]['UTCDateTime'].__str__()
        game_data[0]['GmDate'] = game_data[0]['GmDate'].__str__()
        return game_data[0]
    except Exception as e:
        return "Something went wrong:" + e.__str__()


# hbh
def get_game_info_to_org_view(game_id, player_id, token, dev_id):
    """
    GmT,Desc,Age,PayType,IsFree,IsHis,GmID,STime,OrgID,attendType,zoomUrl,OrgName
    Scope,UTCDateTime,ETime,MaxPly,LevelT,CourtT,Fees,PolicyT,LocDesc,PolicyID,IsStopRecurred
    GmImg,GmReqQues,PlyAnswers,GmStatus,ISRecurr,ParentState,gmIsPaused,GmReported,FeedPlyID
    GmPlys,IssetOrgTerms,MemGm,PlyMethods
    ---
    error in bundles => Subscriptions,PlySubscriptions,validJoinSubscriptions,

    QuesDiff,,WithdrawMess,Days
    ,GmDate,SSTime,InstructorData


    """
    try:
        game_info = execution.execute(
            f"SELECT gm_id as GmID,gm_title as GmT,gm_reqQues,gm_org_id as OrgID,gm_img,CONCAT(ply_fname,' ',ply_lname) AS OrgName,gm_s_type_name as STypeName,court_title as CourtT,\
                    level_title as LevelT,gm_max_players as MaxPly,gm_start_time as STime,gm_end_time as ETime,\
                    gm_loc_desc as LocDesc,gm_scope as Scope,gm_desc as 'Desc',IFNULL(gm_status, '') AS GmStatus,\
                    gm_is_free as IsFree,attend_type as attendType,zoom_url as zoomUrl,\
                    gm_payment_type as PayType,gm_policy_id as PolicyID,policy_title as PolicyT,\
                    gm_is_stop_recurred as IsStopRecurred,gm_is_stop_recurred,gm_recurr_times,gm_recurr_type,gm_recurr_id as RecurrID,\
                    gm_fees as Fees,gm_utc_datetime as UTCDateTime,(CASE WHEN ((gm_org_id = {int(player_id)} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP) OR (gm_org_id != {int(player_id)} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP)) THEN 'n' ELSE 'y' END) AS IsHis\
                    FROM game FULL JOIN players org ON gm_org_id =org.ply_id LEFT JOIN gm_s_types ON gm_sub_type_id = gm_s_type_id \
                    LEFT JOIN court ON gm_court_id = court_id \
                    LEFT JOIN level ON gm_level_id = level_id \
                    LEFT JOIN gm_ages ON gm_ages_id = gm_age \
                    LEFT JOIN country ON gm_country_id = country_id \
                    LEFT JOIN `policy` ON gm_policy_id = policy_id WHERE gm_id = {game_id} AND (gm_status IS NULL OR gm_status NOT LIKE '%deleted%')")
        if not game_info:
            raise Exception('game data not found')

        is_game_member = execution.execute(
            f"SELECT (gm_ply_id) AS Mem FROM gm_players WHERE gm_ply_gm_id ={game_id} AND gm_ply_ply_id = {player_id} AND gm_ply_status = 'y'")

        check_exist = execution.execute(
            f"SELECT contact_id FROM contacts where contact_org_id='{game_info[0]['OrgID']}' and contact_ply_id='{player_id}';")
        if check_exist:
            new_client = 0
        else:
            new_client = 1

        # need modification after auth to get tkn , dev_id
        params = {'ProjectKey': '1234', 'ProjectSecret': '1234', 'new_client': new_client, 'dev_id': dev_id,
                  'ply_id': player_id,
                  'org_id': game_info[0]['OrgID'], 'tkn': token, 'class_id': game_id,
                  'class_datetime': str(game_info[0]['UTCDateTime'])}

        subscriptions_data = common_utils.bundle_curl('playerBundles', params)
        if str(subscriptions_data).__contains__('error'):
            raise Exception(subscriptions_data)

        # subscriptions_data=subscriptions_data["data"]
        answers_dict = questionnaire_utils.get_player_questionnaire_answers(game_id, player_id)
        result = game_info[0]
        # return game_info

        if 'gm_recurr_times' in game_info[0] and 'gm_recurr_type' in game_info[0]:
            if game_info[0]['gm_recurr_type'] and game_info[0]['gm_recurr_times'] > 0:
                result['ParentState'] = 'p'
        elif 'RecurrID' in game_info[0]:
            if int(game_info[0]['RecurrID']) > 0:
                result['ParentState'] = 'c'
        result["GmImg"] = s3_bucket_url + str(game_info[0]["gm_img"])
        result["GmReqQues"] = 'yes' if game_info[0]["gm_reqQues"] == 1 else 'no'
        result["GmReported"] = ""

        result["PlyAnswers"] = answers_dict["PlyAnswers"]
        result['GmImg'] = s3_bucket_url + str(game_info[0]['gm_img'])
        result['ISRecurr'] = "True" if game_info[0]["gm_is_stop_recurred"] == "n" else "False"
        result['FeedPlyID'] = ""
        result['FeedStatus'] = ""
        result['GmPlys'] = player_utils.get_players_count_in_game(game_id)
        result['IssetOrgTerms'] = organizer_utils.get_IssetOrgTerms_key_for_game(game_info[0]["OrgID"])

        result["MemGm"] = "True" if is_game_member and is_game_member[0]["Mem"] else "False"
        result["PlyMethods"] = get_ply_verified_methods(player_id)
        result["Days"] = recur_utils.get_days(game_info[0]["gm_recurr_type"])
        # return subscriptions_data
        result["Subscriptions"] = subscriptions_data["orgBundles"] if subscriptions_data["orgBundles"] else ''
        result['PlySubscriptions'] = subscriptions_data['plySubscriptions'] if subscriptions_data[
            'plySubscriptions'] else ''
        result['validJoinSubscriptions'] = subscriptions_data['validJoinSubscriptions'] if subscriptions_data[
            'validJoinSubscriptions'] else ''

        return result
    except Exception as e:
        return "something went wrong:" + e.__str__()


def get_game_flags(game_id, player_id):
    """"
             desc: get game flags and checks(boolean values) that used in game_view
             input: game_id,player_id
             output: result[GmStatus,IsHis,ISRecurr,Days,Parent,GmReqQues,GmReported,Withdrawable,gmIsPaused,RecSetPaused]
    """
    try:
        game_flags = execution.execute(
            f"SELECT gm_recurr_id,(CASE WHEN ((gm_org_id = {player_id} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP) OR (gm_org_id != {player_id} && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP)) THEN 'n' ELSE 'y' END) AS IsHis\
            ,gm_is_stop_recurred,gm_recurr_id,gm_reqQues,gm_min_players,gm_date,gm_start_time,gm_org_id,gm_recurr_times\
            ,gm_end_pause,IFNULL(gm_status, '') AS GmStatus\
            FROM game WHERE gm_id={game_id}")
        if str(game_flags).__contains__('Something went wrong'):
            raise Exception(game_flags)
        if not game_flags:
            raise Exception('not found')

        result = {
            "GmStatus": game_flags[0]["GmStatus"], "IsHis": game_flags[0]["IsHis"],
            "ISRecurr": "True" if game_flags[0]["gm_is_stop_recurred"] == "n" else "False",
            "Parent": "False" if int(game_flags[0]["gm_recurr_id"]) > 0 or game_flags[0][
                "gm_date"] < date.today() or int(game_flags[0]["gm_recurr_times"]) > 0 else 'True',
            "GmReqQues": 'yes' if game_flags[0]["gm_reqQues"] == 1 else 'no', "GmReported": "",
            "Withdrawable": player_utils.can_player_withdraw_from_game(game_id, player_id)
        }
        return result

    except Exception as e:
        return e.__str__()


def getClassIds(project_id):
    # parameter is project_id must be int
    # return array of classes_ids waitlist ex:[{'gm_id': 272841}, {'gm_id': 273216}, {'gm_id': 272817}]
    try:
        if project_id and type(project_id) == int and int(project_id) > 0:
            #                                 ## write your query here to get class ids
            Class_id = execution.execute(
                f"SELECT gm_id FROM game WHERE gm_utc_datetime > CURRENT_TIMESTAMP AND(gm_status IS NULL OR gm_status = '' OR gm_status = 'admin')"
                f"AND gm_id IN(SELECT gm_wait_list_gm_id FROM gm_waitlist WHERE gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0)"
                f" AND gm_pid = {project_id};")
            return Class_id
        else:
            raise Exception("project_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def getClassData(SqlArray):
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    # return array of  classes data ex:[{'gm_id': 272817, 'gm_org_id': 1765, 'gm_utc_datetime': datetime.datetime(2022, 1, 5, 17, 0), 'gm_max_players': 1}]
    try:
        # check if Class_id is not empty and type is list
        if SqlArray and type(SqlArray) == str:
            # write your query here to get class data

            Class_data = execution.execute(
                f"SELECT gm_id,gm_org_id,gm_utc_datetime,gm_max_players FROM game WHERE gm_id IN {SqlArray};")
            return Class_data
        else:
            raise Exception("Classes_ids is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def informWaitlist(ClassesData, SqlArray):
    # parameter is array od classesData ex:[{'gm_id': 272817, 'gm_org_id': 1765, 'gm_utc_datetime': datetime.datetime(2022, 1, 5, 17, 0), 'gm_max_players': 1}
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    # return False or True
    try:
        # check if ClassesData is not array or  empty
        if not ClassesData or not type(ClassesData) == list:
            return False
        # get classes countGmPlays
        GmPlys = countGmPlys(SqlArray)
        if str(GmPlys).__contains__("something happened:"):
            raise Exception(GmPlys)
        currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        game_time_difference_check = [bool]
        for ClassData in ClassesData:
            # check if class GmPlys >= class gm_max_players
            for count in GmPlys:
                if count['total'] >= ClassData['gm_max_players']:
                    return False
            # get class UTC dateTime and currentTime
            game_utc_datetime = ClassData['gm_utc_datetime']
            # check if class UTC dateTime < currentTime
            if datetime.strptime(str(game_utc_datetime), '%Y-%m-%d %H:%M:%S') < currentTime:
                return False
            # get class time before 12 hours
            game_time_before_12_hrs = datetime.strptime(str(game_utc_datetime), '%Y-%m-%d %H:%M:%S') - timedelta(
                hours=12)
            if game_time_before_12_hrs > currentTime:
                game_time_difference_check.append(True)
            else:
                game_time_difference_check.append(False)
        # get wait list members
        waitlist_members = getWaitListMembers(SqlArray)
        if str(waitlist_members).__contains__("something happened:"):
            raise Exception(waitlist_members)
        # check if empty wait list members
        if not waitlist_members:
            return False

        send = sendWaitlistInform(ClassesData, game_time_difference_check, waitlist_members, SqlArray)
        if str(send).__contains__("something happened:"):
            raise Exception(send)
        return send
    except Exception as e:
        return "something happened:" + e.__str__()


def countGmPlys(SqlArray):
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    # return array of countGmPlys ex:[{'gm_max_players': 1, 'gm_id': 272817, 'total': 3}]
    try:
        # check if ClassesData is not empty and type is list
        if SqlArray and type(SqlArray) is str:
            #                                 ## write your query here to get countGmPlys
            count_gm_plys = execution.execute(
                f"SELECT game.gm_max_players,game.gm_id,count(gm_players.gm_ply_id) as total from game Left Join gm_players on game.gm_id=gm_players.gm_ply_gm_id where gm_id IN {SqlArray};")
            return count_gm_plys
        else:
            raise Exception("Class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def getWaitListMembers(SqlArray):
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    # return array of WaitListMembers ex:[{'gm_wait_list_id': 4566, 'gm_wait_list_gm_id': 272841, 'gm_wait_list_ply_id': 1767, 'gm_wait_list_withdrew': 0, 'gm_wait_list_removed_by_admin': 0, 'gm_wait_list_created': datetime.datetime(2022, 1, 2, 12, 7, 54)}]
    try:
        # check if ClassesData is not empty and type is list
        if SqlArray and type(SqlArray) == str:
            #                                    ## write your query here to get WaitListMembers
            wait_data = execution.execute(
                f"SELECT * FROM gm_waitlist WHERE gm_wait_list_gm_id IN {SqlArray} AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0 ORDER BY gm_wait_list_created ASC;")
            return wait_data

        else:
            raise Exception("Class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def sendWaitlistInform(ClassesData, game_time_difference_check, waitlist_members, SqlArray):
    # parameter is array of classesData  ex:[{'gm_id': 272817, 'gm_org_id': 1765, 'gm_utc_datetime': datetime.datetime(2022, 1, 5, 17, 0), 'gm_max_players': 1}]
    # parameter is array of waitlist_members ex:[{'gm_wait_list_id': 4566, 'gm_wait_list_gm_id': 272841, 'gm_wait_list_ply_id': 1767, 'gm_wait_list_withdrew': 0, 'gm_wait_list_removed_by_admin': 0, 'gm_wait_list_created': datetime.datetime(2022, 1, 2, 12, 7, 54)}]
    # parameter game_time_difference_check ex:[False,True,False,True]
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    try:
        # check if wait-list_members is not array and  empty
        if not waitlist_members or not type(waitlist_members) == list:
            return False
        # check if ClassesData is not array and  empty
        if not ClassesData or not type(ClassesData) == list:
            return False
        OrgArray = []
        WaitArray = []
        BanArray = []
        sql_list = []
        sql_list2 = []
        for OrgID in ClassesData:
            OrgArray.append(OrgID['gm_org_id'])
        OrgIDArray = str(tuple([key for key in OrgArray])).replace(',)', ')')
        for WaitID in waitlist_members:
            WaitArray.append(WaitID['gm_wait_list_ply_id'])
        WaitIDArray = str(tuple([key for key in WaitArray])).replace(',)', ')')
        # check if member is banned from admin
        isBan = ChkIsBan(OrgIDArray, WaitIDArray)
        if str(isBan).__contains__("something happened:"):
            raise Exception(isBan)
        if isBan:
            for banId in waitlist_members:
                BanArray.append(banId['gm_wait_list_id'])
            IdBanArray = str(tuple([key for key in BanArray])).replace(',)', ')')
            # remove waitlist row for the player with this game
            delete = execution.execute(f"DELETE FROM gm_waitlist WHERE gm_wait_list_id IN {IdBanArray};")
            if delete:
                raise Exception(delete)
            return False
        # check if members is invited before to this game
        isInv = ChkIsInvGm(SqlArray, WaitIDArray)
        if str(isInv).__contains__("something happened:"):
            raise Exception(isInv)
        if not isInv:
            return False
        currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        # get last invitation date time
        lastInvDateTime = getLastInvDateTime(SqlArray)
        if str(lastInvDateTime).__contains__("something happened:"):
            raise Exception(lastInvDateTime)
        if not lastInvDateTime:
            return False
        for time_difference in game_time_difference_check:
            for Gm_id in ClassesData:
                if not time_difference:
                    sql_list.append(Gm_id['gm_id'])
                else:
                    sql_list2.append(Gm_id['gm_id'])

            for LastDate in lastInvDateTime:
                if time_difference is True and lastInvDateTime:
                    # check if the time between last invitation and current time less than one hour
                    time_diff_in_minutes = (
                            (currentTime - datetime.strptime(LastDate['inv_created'], '%Y-%m-%d %H:%M:%S')) / 60)
                    if time_diff_in_minutes < timedelta(minutes=60):
                        return False

        SqlArray = str(tuple([key for key in sql_list])).replace(',)', ')')
        SqlArray2 = str(tuple([key for key in sql_list])).replace(',)', ')')
        # this means the class has less than 12 hours to start...then it will show in the search for classes.
        execution.execute(f"UPDATE game SET gm_available_to_join = 1 WHERE gm_id IN {SqlArray}")
        # update game available to search to 0 = > means that anyone will join as a waitList.
        execution.execute(f"UPDATE game SET gm_available_to_join = 0 WHERE gm_id IN {SqlArray2}")

        # insert new invitation to this member for these classes
        execution.execute(f"INSERT INTO invitations (inv_gm_id, inv_ply_frm_id, inv_ply_to_id, inv_approve) "
                          f"VALUES({SqlArray}, {OrgIDArray}, {WaitIDArray}, 'y')")
        # log this invitation
        execution.execute(f"INSERT INTO invitations_log (inv_log_gm_id, inv_log_ply_id) "
                          f"VALUES({SqlArray}, {WaitIDArray})")

        # send mail to inform this member
        # sends notification to inform this member
    except Exception as e:
        return "something happened:" + e.__str__()


def ChkIsInvGm(SqlArray, WaitIDArray):
    # parameter is array of SqlArray ex:"(272841, 273216, 272817)"
    # parameter is array of WaitIDArray ex:"(4566, 273216, 272817)"

    # parameter is array of waitlist_members ex:[{PlyId:4356,Ply_fname:'asf',..},{PlyId:4356,Ply_fname:'asf',..},{PlyId:4356,Ply_fname:'asf',..}]
    # return array of True or False ex:[True,False,....]
    try:
        # check if ClassId and PlayerID is not empty and type is int and >=0
        if SqlArray and type(SqlArray) == str and WaitIDArray and type(WaitIDArray) == str:
            #                                              ## write your query here to get invitations
            IsInv = execution.execute(
                f"SELECT * FROM invitations WHERE inv_gm_id IN {SqlArray} AND inv_ply_to_id IN {WaitIDArray} AND (inv_approve = 'y' or inv_approve = 'p')")
            return IsInv
        else:
            raise Exception("PlayerID or ClassId is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def getLastInvDateTime(SqlArray):
    # parameter is array of SqlArray  "(272841, 273216, 272817)"
    # return array of True or False ex:['ply_ban_id'1767:,'ply_ban_id'1767:,....]
    try:
        # check if OrgId and PlayerID is not empty and type is int and >=0
        if SqlArray and type(SqlArray) == str:
            #                                           ## write your query here to get ply_ban_id
            lastDate = execution.execute(
                f"SELECT inv_created FROM invitations WHERE inv_gm_id IN {SqlArray} AND (inv_approve = 'y' or inv_approve = 'p') ORDER BY inv_id DESC")
            return lastDate

        else:
            raise Exception("PlayerID or OrgId is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def ChkIsBan(OrgIDArray, WaitIDArray):
    # parameter is array of OrgIDArray  "(1765, 1765, 1765)"
    # parameter is array of WaitIDArray ex:"(1767, 1767, 1767)"
    # return array of True or False ex:['ply_ban_id'1767:,'ply_ban_id'1767:,....]
    try:
        # check if OrgId and PlayerID is not empty and type is int and >=0
        if OrgIDArray and type(OrgIDArray) is str and WaitIDArray and type(WaitIDArray) is str:
            #                                            ## write your query here to get ply_ban_id
            IsBan = execution.execute(
                f"SELECT ply_ban_id FROM ply_bans WHERE ((ply_ban_ply_frm IN {OrgIDArray} AND ply_ban_ply_to IN {WaitIDArray})"
                f" or (ply_ban_ply_frm IN {WaitIDArray}  AND ply_ban_ply_to IN {OrgIDArray}));")
            return IsBan
        else:
            raise Exception("PlayerID or OrgId is required")
    except Exception as e:
        return "something happened:" + e.__str__()


#                                                                 ##### Edit Class part ####
def get_new_data(EditField, oldData):
    # parameter is dict of EditField  ex: {"GmT":"%20nola1%20test"}
    # return str of EditFieldChange ex:  gm_title = '%2520nola1%2520test',gm_display_org = 'n',gm_sub_type_id = '464',gm_court_id = '1',gm_level_id = '8',gm_age = '3',gm_min_players = '1',gm_max_players = '3',gm_max_players_orig = '3',gm_country_id = '66',gm_loc_lat = '30.8760568',gm_loc_long = '29.742604',gm_loc_desc = 'Alexandria%2520Governorate%252C%2520Egypt',gm_has_gallery = 'n',gm_img = '05-2021/classes/09052021JSbc0mdRZyL8ApTiB7MKe5sPV2UYqzHuNCFhl46wXQEIrg.jpg',gm_requirements = 'ReqReqReqReqReq',gm_notes = 'NoteNoteNoteNote',gm_rules = 'RulesRulesRules',gm_kits = 'KitsKitsKitsKits',gm_showMem = '0',gm_reqQues = '0',gm_payment_type = 'stripe',gm_policy_id = '1',gm_is_free = 'n',gm_fees = '80',gm_currency_symbol = '61',gm_scope = 'Open to public',attend_type = 'inPerson',gm_time_zone = 'Europe/London',gm_date = '2021-5-17', gm_utc_datetime = '2021-05-17 13:40:00', gm_unix_utc_datetime = 1621251600, gm_unix_utc_end_datetime = 1621253400  , gm_available_to_join = 1, gm_start_time = '14:40', gm_utc_datetime = CONVERT_TZ(CONCAT(gm_date,' ','14:40'), 'Europe/London', 'UTC'), gm_unix_utc_datetime = 1621251600,gm_end_time = '30', gm_unix_utc_end_datetime = 1621253400
    try:
        # check if field in dict and field is not empty and also check type
        if not EditField or type(EditField) != dict:
            raise Exception("invalid Data")

        if 'GmT' in EditField and EditField['GmT'] and type(EditField['GmT']) == str:
            oldData['GmT'] = EditField['GmT']

        if 'DisOrg' in EditField and EditField['DisOrg'] and type(EditField['DisOrg']) == str:
            oldData['DisOrg'] = EditField['DisOrg']

        if 'STypeID' in EditField and EditField['STypeID'] and type(EditField['STypeID']) == int:
            oldData['STypeID'] = EditField['STypeID']

        if 'CourtID' in EditField and EditField['CourtID'] and type(EditField['CourtID']) == int:
            EditField['CourtID'] = "0" if EditField['CourtID'] == "" else EditField['CourtID']
            oldData['CourtID'] = EditField['CourtID']

        if 'LevelID' in EditField and EditField['LevelID']:
            EditField['LevelID'] = "0" if EditField['LevelID'] == "" else EditField['LevelID']
            oldData['LevelID'] = EditField['LevelID']

        if 'Gdr' in EditField and EditField['Gdr'] and type(EditField['Gdr']) == str:
            oldData['Gdr'] = EditField['Gdr']
        if 'Minply' in EditField and EditField['Minply'] and type(EditField['Minply']) == int:
            oldData['Minply'] = EditField['Minply']

        if 'Maxply' in EditField and EditField['Maxply'] and type(EditField['Maxply']) == int:
            oldData['Maxply'] = EditField['Maxply']

        if 'CtyID' in EditField and EditField['CtyID'] and type(EditField['CtyID']) == int:
            oldData['CtyID'] = EditField['CtyID']

        if 'CountryID' in EditField and EditField['CountryID'] and type(EditField['CountryID']) == int:
            oldData['CountryID'] = EditField['CountryID']

        if 'Lat' in EditField and EditField['Lat'] and type(EditField['Lat']) == float:
            oldData['Lat'] = EditField['Lat']

        if 'Long' in EditField and EditField['Long'] and type(EditField['Long']) == float:
            oldData['Long'] = EditField['Long']

        if 'LocDesc' in EditField and EditField['LocDesc'] and type(EditField['LocDesc']) == str:
            oldData['LocDesc'] = EditField['LocDesc']

        if 'HasGlly' in EditField and EditField['HasGlly'] and type(EditField['HasGlly']) == str:
            oldData['HasGlly'] = EditField['HasGlly']

        if 'gameImg' in EditField and EditField['gameImg'] and type(EditField['gameImg']) == str:
            oldData['gameImg'] = EditField['gameImg']

        if 'Desc' in EditField and EditField['Desc'] and type(EditField['Desc']) == str:
            oldData['Desc'] = EditField['Desc']

        if 'Req' in EditField and EditField['Req'] and type(EditField['Req']) == str:
            oldData['Req'] = EditField['Req']

        if 'Note' in EditField and EditField['Note'] and type(EditField['Note']) == str:
            oldData['Note'] = EditField['Note']

        if 'Rules' in EditField and EditField['Rules'] and type(EditField['Rules']) == str:
            oldData['Rules'] = EditField['Rules']

        if 'Kits' in EditField and EditField['Kits'] and type(EditField['Kits']) == str:
            oldData['Kits'] = EditField['Kits']

        if 'showMem' in EditField and EditField['showMem'] and type(EditField['showMem']) == str:
            oldData['showMem'] = EditField['showMem']

        if 'GmReqQues' in EditField and EditField['GmReqQues'] and type(EditField['GmReqQues']) == str:
            oldData['GmReqQues'] = EditField['GmReqQues']

        if 'PayType' in EditField and EditField['PayType'] and type(EditField['PayType']) == str:
            oldData['PayType'] = EditField['PayType']

        if 'PolicyID' in EditField and EditField['PolicyID'] and type(EditField['PolicyID']) == int:
            oldData['PolicyID'] = EditField['PolicyID']

        if 'Fees' in EditField and EditField['Fees']:
            if 'Symbol' in EditField and EditField['Symbol'] and type(EditField['Symbol']) == str:
                IsFree = 'n' if float(int(EditField['Fees']) > 0) else 'y'
                Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
                Symbol = EditField['Symbol'] if IsFree == 'n' else ''
                oldData['Fees'] = Fees
                oldData['Symbol'] = Symbol
                oldData['IsFree'] = IsFree
                oldData['ISFreeChk'] = IsFree

        if 'Scope' in EditField and EditField['Scope'] and type(EditField['Scope']) == str:
            oldData['Scope'] = EditField['Scope']

        if 'IsFree' in EditField and EditField['IsFree'] and type(EditField['IsFree']) == str:
            IsFree = EditField['IsFree']
            oldData['IsFree'] = IsFree
            oldData['ISFreeChk'] = IsFree
            if 'Fees' in EditField and 'Symbol' in EditField:
                Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
                Symbol = EditField['Symbol'] if IsFree == 'n' else ''
                oldData['Fees'] = Fees
                oldData['Symbol'] = Symbol

        if 'ISFreeChk' in EditField and EditField['ISFreeChk'] and type(EditField['ISFreeChk']) == str:
            IsFree = EditField['ISFreeChk']
            oldData['IsFree'] = IsFree
            oldData['ISFreeChk'] = IsFree
            if 'Fees' in EditField and 'Symbol' in EditField:
                Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
                Symbol = EditField['Symbol'] if IsFree == 'n' else ''
                oldData['Fees'] = Fees
                oldData['Symbol'] = Symbol

        if 'AttendType' in EditField and EditField['AttendType'] and type(EditField['AttendType']) == str:
            oldData['AttendType'] = EditField['AttendType']

        if 'timeZone' in EditField and EditField['timeZone'] and type(EditField['timeZone']) == str:
            oldData['timeZone'] = EditField['timeZone']

        if 'modify' in EditField:
            if EditField['modify'] and type(EditField['modify']) == str and str(EditField['modify']).lower() == "one":
                oldData['gm_copy_id'] = EditField['GmID']

        if 'UTCDateTime' in EditField and EditField['UTCDateTime'] and type(EditField['UTCDateTime']) == str:
            oldData['UTCDateTime'] = EditField['UTCDateTime']

        if 'STime' in EditField and EditField['STime'] and type(EditField['STime']) == str:
            oldData['STime'] = EditField['STime']

        if 'ETime' in EditField and EditField['ETime'] and type(EditField['ETime']) == str:
            oldData['ETime'] = EditField['ETime']

        return oldData
    except Exception as e:
        return "something happened:" + e.__str__()


def validation_field_to_edit(EditField):
    # parameter is dict of EditField  ex: {"GmT":"%20nola1%20test"}
    # return str of EditFieldChange ex:  gm_title = '%2520nola1%2520test',gm_display_org = 'n',gm_sub_type_id = '464',gm_court_id = '1',gm_level_id = '8',gm_age = '3',gm_min_players = '1',gm_max_players = '3',gm_max_players_orig = '3',gm_country_id = '66',gm_loc_lat = '30.8760568',gm_loc_long = '29.742604',gm_loc_desc = 'Alexandria%2520Governorate%252C%2520Egypt',gm_has_gallery = 'n',gm_img = '05-2021/classes/09052021JSbc0mdRZyL8piB7MKe5sPV2UYqzHuNCha46wXQEIrg.jpg',gm_requirements = 'ReqReqReqReqReq',gm_notes = 'NoteNoteNoteNote',gm_rules = 'RulesRulesRules',gm_kits = 'KitsKitsKitsKits',gm_showMem = '0',gm_reqQues = '0',gm_payment_type = 'stripe',gm_policy_id = '1',gm_is_free = 'n',gm_fees = '80',gm_currency_symbol = '61',gm_scope = 'Open to public',attend_type = 'inPerson',gm_time_zone = 'Europe/London',gm_date = '2021-5-17', gm_utc_datetime = '2021-05-17 13:40:00', gm_unix_utc_datetime = 1621251600, gm_unix_utc_end_datetime = 1621253400  , gm_available_to_join = 1, gm_start_time = '14:40', gm_utc_datetime = CONVERT_TZ(CONCAT(gm_date,' ','14:40'), 'Europe/London', 'UTC'), gm_unix_utc_datetime = 1621251600,gm_end_time = '30', gm_unix_utc_end_datetime = 1621253400
    try:
        # check if field in dict and field is not empty and also check type
        if not EditField or type(EditField) != dict:
            raise Exception("invalid Data")

        EditFieldChange = str()

        if 'GmT' in EditField and EditField['GmT'] and type(EditField['GmT']) == str:
            GmT = urllib.parse.quote(EditField['GmT'])
            EditFieldChange += "gm_title = '" + GmT + "',"

        if 'DisOrg' in EditField and EditField['DisOrg'] and type(EditField['DisOrg']) == str:
            DisOrg = EditField['DisOrg']
            EditFieldChange += "gm_display_org = '" + DisOrg + "',"

        if 'STypeID' in EditField and EditField['STypeID'] and type(EditField['STypeID']) == int:
            EditFieldChange += "gm_sub_type_id = '" + str(EditField['STypeID']) + "',"

        if 'CourtID' in EditField and EditField['CourtID'] and type(EditField['CourtID']) == int:
            EditField['CourtID'] = "0" if EditField['CourtID'] == "" else EditField['CourtID']
            EditFieldChange += "gm_court_id = '" + str(EditField['CourtID']) + "',"

        if 'LevelID' in EditField and EditField['LevelID']:
            EditField['LevelID'] = "0" if EditField['LevelID'] == "" else EditField['LevelID']
            EditFieldChange += "gm_level_id = '" + str(EditField['LevelID']) + "',"

        if 'Gdr' in EditField and EditField['Gdr'] and type(EditField['Gdr']) == str:
            EditFieldChange += "gm_gender = '" + EditField['Gdr'] + "',"
        if 'Minply' in EditField and EditField['Minply'] and type(EditField['Minply']) == int:
            Minply = urllib.parse.unquote(str(EditField['Minply']))
            EditFieldChange += "gm_min_players = '" + Minply + "',"

        if 'Maxply' in EditField and EditField['Maxply'] and type(EditField['Maxply']) == int:
            Maxply = urllib.parse.unquote(str(EditField['Maxply']))
            EditFieldChange += "gm_max_players = '" + Maxply + "',"
            EditFieldChange += "gm_max_players_orig = '" + Maxply + "',"

        if 'CtyID' in EditField and EditField['CtyID'] and type(EditField['CtyID']) == int:
            EditFieldChange += "gm_city_id = '" + str(EditField['CtyID']) + "',"

        if 'CountryID' in EditField and EditField['CountryID'] and type(EditField['CountryID']) == int:
            EditFieldChange += "gm_country_id = '" + str(EditField['CountryID']) + "',"

        if 'Lat' in EditField and EditField['Lat'] and type(EditField['Lat']) == float:
            EditFieldChange += "gm_loc_lat = '" + str(EditField['Lat']) + "',"

        if 'Long' in EditField and EditField['Long'] and type(EditField['Long']) == float:
            EditFieldChange += "gm_loc_long = '" + str(EditField['Long']) + "',"

        if 'LocDesc' in EditField and EditField['LocDesc'] and type(EditField['LocDesc']) == str:
            LocDesc = urllib.parse.quote(EditField['LocDesc'])
            EditFieldChange += "gm_loc_desc = '" + LocDesc + "',"

        if 'HasGlly' in EditField and EditField['HasGlly'] and type(EditField['HasGlly']) == str:
            EditFieldChange += "gm_has_gallery = '" + EditField['HasGlly'] + "',"

        if 'gameImg' in EditField and EditField['gameImg'] and type(EditField['gameImg']) == str:
            EditFieldChange += "gm_img = '" + EditField['gameImg'] + "',"

        if 'Desc' in EditField and EditField['Desc'] and type(EditField['Desc']) == str:
            Desc = urllib.parse.quote(EditField['Desc'])
            EditFieldChange += "gm_desc = '" + Desc + "',"

        if 'Req' in EditField and EditField['Req'] and type(EditField['Req']) == str:
            Req = urllib.parse.quote(EditField['Req'])
            EditFieldChange += "gm_requirements = '" + Req + "',"

        if 'Note' in EditField and EditField['Note'] and type(EditField['Note']) == str:
            Note = urllib.parse.quote(EditField['Note'])
            EditFieldChange += "gm_notes = '" + Note + "',"

        if 'Rules' in EditField and EditField['Rules'] and type(EditField['Rules']) == str:
            Rules = urllib.parse.quote(EditField['Rules'])
            EditFieldChange += "gm_rules = '" + Rules + "',"

        if 'Kits' in EditField and EditField['Kits'] and type(EditField['Kits']) == str:
            EditFieldChange += "gm_kits = '" + EditField['Kits'] + "',"

        if 'showMem' in EditField and EditField['showMem'] and type(EditField['showMem']) == str:
            showMem = "0" if EditField['showMem'] == "no" else "1"
            EditFieldChange += "gm_showMem = '" + showMem + "',"

        if 'GmReqQues' in EditField and EditField['GmReqQues'] and type(EditField['GmReqQues']) == str:
            EditField['GmReqQues'] = "1" if EditField['GmReqQues'] == "yes" else "0"
            EditFieldChange += "gm_reqQues = '" + EditField['GmReqQues'] + "',"

        if 'PayType' in EditField and EditField['PayType'] and type(EditField['PayType']) == str:
            EditFieldChange += "gm_payment_type = '" + EditField['PayType'] + "',"

        if 'PolicyID' in EditField and EditField['PolicyID'] and type(EditField['PolicyID']) == int:
            EditFieldChange += "gm_policy_id = '" + str(EditField['PolicyID']) + "',"

        if 'Fees' in EditField and EditField['Fees']:
            if 'Symbol' in EditField and EditField['Symbol'] and type(EditField['Symbol']) == str:
                IsFree = 'n' if float(int(EditField['Fees']) > 0) else 'y'
                Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
                Symbol = str(EditField['Symbol']) if IsFree == 'n' else ''
                EditFieldChange += "gm_is_free = '" + IsFree + "',gm_fees = '" + Fees + "',gm_currency_symbol = '" + Symbol + "',"

        if 'IsFree' in EditField and EditField['IsFree'] and type(EditField['IsFree']) == str:
            IsFree = EditField['IsFree']
            Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
            Symbol = str(EditField['Symbol']) if IsFree == 'n' else ''
            EditFieldChange += "gm_is_free = '" + IsFree + "',gm_fees = '" + Fees + "',gm_currency_symbol = '" + Symbol + "',"

        if 'ISFreeChk' in EditField and EditField['ISFreeChk'] and type(EditField['ISFreeChk']) == str:
            IsFree = EditField['ISFreeChk']
            Fees = str(round(int(EditField['Fees']), 2)) if IsFree == 'n' else '0'
            Symbol = str(EditField['Symbol']) if IsFree == 'n' else ''
            EditFieldChange += "gm_is_free = '" + IsFree + "',gm_fees = '" + Fees + "',gm_currency_symbol = '" + Symbol + "',"

        if 'Scope' in EditField and EditField['Scope'] and type(EditField['Scope']) == str:
            EditFieldChange += "gm_scope = '" + EditField['Scope'] + "',"

        if 'AttendType' in EditField and EditField['AttendType'] and type(EditField['AttendType']) == str:
            EditFieldChange += "attend_type = '" + EditField['AttendType'] + "',"

        if 'timeZone' in EditField and EditField['timeZone'] and type(EditField['timeZone']) == str:
            timeZone = str(EditField['timeZone']).replace("\\", "")
            EditFieldChange += "gm_time_zone = '" + timeZone + "',"

        if 'modify' in EditField:
            if EditField['modify'] and type(EditField['modify']) == str and str(EditField['modify']).lower() == "one":
                EditFieldChange += "gm_copy_id = '" + str(EditField['GmID']) + "',"

        newUTCDateTime = ''
        formatting = ''
        gmUTCDateTime = ''

        if 'UTCDateTime' in EditField and EditField['UTCDateTime']:
            newUTCDateTime = EditField['UTCDateTime']
            formatting = '%a, %d %b %Y %H:%M:%S %Z'
            gmUTCDateTime = datetime.strptime(str(newUTCDateTime), formatting)

        elif 'GmDate' in EditField and 'STime' in EditField and 'timeZone' in EditField and EditField['timeZone']:
            timeZone = str(EditField['timeZone']).replace("\\", "")
            newUTCDateTime = get_Utc_Datetime(timeZone, EditField['GmDate'] + " " + EditField['STime'])
            if str(newUTCDateTime).__contains__("something happened:"):
                raise Exception(newUTCDateTime)
            formatting = '%Y-%m-%d %H:%M:%S%z'
            # gmUTCDateTime = datetime.fromisoformat(str(newUTCDateTime))
            gmUTCDateTime = datetime.strptime(str(newUTCDateTime), formatting)

        elif 'GmDate' in EditField and 'STime' in EditField:
            newUTCDateTime = EditField['GmDate'] + " " + EditField['STime']
            formatting = '%Y-%m-%d %H:%M'
            gmUTCDateTime = datetime.strptime(str(newUTCDateTime), formatting)
            # gmUTCDateTime = datetime.fromisoformat(str(newUTCDateTime))

        gmEndTime = urllib.parse.unquote(EditField['ETime'])
        newGmUTCDateTime = gmUTCDateTime.strftime('%Y-%m-%d')
        gmUnixUTCDateTime = gmUTCDateTime.strftime("%s")
        d = datetime.strptime(str(newUTCDateTime), formatting) + timedelta(minutes=int(gmEndTime))
        gmUnixUTCEndDateTime = str(d.strftime("%s"))

        if ('GmDate' in EditField) or ('modify' in EditField and EditField['modify'] == 'one'):
            GmDate = EditField['GmDate'] if 'GmDate' in EditField else ""
            EditFieldChange += "gm_date = '" + GmDate + "', gm_utc_datetime = '" + newGmUTCDateTime + "',"
            game_time_before_12_hrs = gmUTCDateTime - timedelta(hours=12)
            currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            # if $game_time_difference_check is true then there is more than 12 hours before the game start time ** /
            game_time_difference_check = True if game_time_before_12_hrs.timestamp() > currentTime.timestamp() else False
            # get wait list members
            waitlist_members = get_Wait_List_Members(int(EditField['GmID']))
            if str(waitlist_members).__contains__("something happened:"):
                raise Exception(waitlist_members)

            if game_time_difference_check is True:
                # this means the class has more than 12 hours to start.
                # update game available to search to 0 = > means it won't show in search for classes .
                if waitlist_members:
                    EditFieldChange += "gm_available_to_join = 0, "

            else:
                # this means the class has less than 12 hours to start...then it will show in the search for classes.
                EditFieldChange += "gm_available_to_join = 1, "

        if 'STime' in EditField and EditField['STime'] and type(EditField['STime']) == str:
            timeZone = EditField['timeZone'] if 'timeZone' in EditField else ''
            EditFieldChange += "gm_start_time = '" + EditField[
                'STime'] + "', gm_utc_datetime = CONVERT_TZ(CONCAT(gm_date,' ','" + EditField[
                                   'STime'] + "'), '" + timeZone + "', 'UTC'), gm_unix_utc_datetime = " + gmUnixUTCDateTime + ","

        if 'ETime' in EditField and EditField['ETime'] and type(EditField['ETime']) == str:
            EditFieldChange += "gm_end_time = '" + EditField[
                'ETime'] + "', gm_unix_utc_end_datetime = " + gmUnixUTCEndDateTime + ","

        # create Zoom meeting to game if not created before
        if 'AttendType' in EditField and EditField['AttendType'] == "zoom":
            zoom_details_check = check_zoom_details(int(EditField['GmID']))
            if str(zoom_details_check).__contains__("something happened:"):
                raise Exception(zoom_details_check)
            if zoom_details_check == "in person class" or zoom_details_check['zoom_url'] is None:
                EditField['timeZone'] = EditField['timeZoneZoom']
                zoom_user = get_zoom_user(int(EditField['PlyID']))
                if str(zoom_user).__contains__("something happened:"):
                    raise Exception(zoom_user)
                if not zoom_user:
                    raise Exception("You are not connect in zoom service , please go to setting and connect it!")

                meetingData = {}
                zoom_user_id = zoom_user[0]['zoom_user_id']
                startTime = newGmUTCDateTime
                meetingData['topic'] = urllib.parse.quote(EditField['GmT'])
                meetingData['agenda'] = ""
                meetingData['type'] = 2
                meetingData['start_time'] = startTime
                meetingData['timezone'] = EditField['timeZone']
                meetingData['duration'] = EditField['ETime']

                token = refreshAccessToken(zoom_user[0]['ply_id'], zoom_user[0]['refresh_token'])
                if token['error']:
                    raise Exception(token)
                crMeeting = createMeeting(zoom_user_id, meetingData, token)
                if not (crMeeting['join_url']) or (crMeeting['join_url'] == ""):
                    if (crMeeting['code']) and crMeeting['code'] == 1001:
                        raise Exception(
                            "To create an online class with Zoom you must fully connect your Zoom account with your ClassFit account. Our records show you need to approve the connection request in an email sent by Zoom. Please accept this request then resume your class creation.",
                            6000)
                    elif (crMeeting['code']) and crMeeting['code'] == 429:
                        raise Exception(
                            "Zoom only allows a maximum of 100 meetings to be created per day. You have exceeded this number and can continue creating classes from tomorrow.",
                            6000)
                    else:
                        raise Exception(crMeeting['message'], 6000)
                zoom_url = crMeeting['join_url']
                zoom_pwd = crMeeting['password']
                zoom_meeting_id = crMeeting['id']
                EditFieldChange += "zoom_url='" + zoom_url + "', zoom_meeting_id='" + zoom_meeting_id + "', zoom_pwd='" + zoom_pwd + "' "

        new_string = EditFieldChange.rstrip(',')
        return new_string
    except Exception as e:
        return "something happened:" + e.__str__()


# def number_format(num, places=0):
#     return locale.format_string("%.*f", (places, num), True)


def get_game_recur_id(GmID):
    # parameter is array of GmID ex:6
    # return array of  [{'gm_recurr_id': 0, 'gm_copy_id': 6}]
    try:
        # check if GmID is not empty and type is int
        if GmID and type(GmID) == int:
            #                                    ## write your query here to get gm_recurr_id and gm_copy_id

            wait_data = execution.execute(
                f"SELECT gm_recurr_id,gm_copy_id FROM game WHERE gm_id = {GmID};")
            return wait_data

        else:
            raise Exception("Class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def update_access_token(player_id, access_token):
    # parameter is array of GmID ex:"6"
    # return array of WaitListMembers ex:[{'gm_wait_list_id': 4566, 'gm_wait_list_gm_id': 272841, 'gm_wait_list_ply_id': 1767, 'gm_wait_list_withdrew': 0, 'gm_wait_list_removed_by_admin': 0, 'gm_wait_list_created': datetime.datetime(2022, 1, 2, 12, 7, 54)}]
    try:
        if type(player_id) != int or player_id < 1:
            raise Exception('Invalid player id')

        if access_token == '':
            raise Exception('invalid access token')

        # prepare query

        query = execution.execute(f"UPDATE zoom_users SET refresh_token = '{access_token}' WHERE ply_id={player_id}")
        return query

    except Exception as e:
        return "something happened:" + e.__str__()


# ##################### work for renew game ###########################


def handle_game_instructor(game_id, game_recurr_id, instructor_id, modify_type=""):
    try:
        # check data
        if type(game_id) != int or game_id < 1:
            raise Exception("Invalid game id ")
        if type(game_recurr_id) != int:
            raise Exception("Invalid game recurr id ")

        if type(instructor_id) != int or int(instructor_id) < 1:
            raise Exception("Invalid instructor id ")

        if type(modify_type) != str:
            raise Exception("Invalid modify_type ")

        parent_id = get_parent_id(game_id, game_recurr_id)
        if str(parent_id).__contains__('something happened:'):
            raise Exception(parent_id)
        if type(parent_id) != int or parent_id < 1:
            raise Exception("Invalid ID")
        """
        * handle queries based on modify type
        * empty or one >> instructor for this class only
        * one future >> instructor for this class and new created classes in recur set
        * all >> instructor for all upcoming classes in the recur set
        """
        modify_type_lower_case = str(modify_type).lower()
        delete_sql = ""
        instructor_sql = ""
        if modify_type_lower_case == "one":
            if int(game_id) == int(parent_id):
                delete_sql = execution.execute(
                    f"DELETE  FROM gm_instructors WHERE gm_id = {game_id}"
                )
                instructor_sql = execution.execute(
                    f"INSERT INTO gm_instructors_parents_only (gm_id, instructor_id) VALUES ({game_id},{instructor_id})"
                )
        if modify_type_lower_case == "onefuture":
            delete_sql = execution.execute(
                f"DELETE  FROM gm_instructors WHERE gm_id = {game_id}\
                    DELETE FROM gm_instructors_parents_only WHERE gm_id = {game_id}"
            )
            if int(game_id) == int(parent_id) and int(game_recurr_id) == 0:
                instructor_sql = handle_one_future_recur_instructorQuery(instructor_id, game_id)
                if str(instructor_sql).__contains__('something happened'):
                    raise Exception(instructor_sql)
        if modify_type_lower_case == "all":
            if int(game_id) == int(parent_id) and int(game_recurr_id) == 0:
                delete_sql = execution.execute(
                    f"DELETE FROM gm_instructors WHERE gm_id IN (SELECT gm_id FROM game WHERE gm_id = {game_id} OR gm_recurr_id = {game_id}\
                            DELETE FROM gm_instructors_parents_only WHERE gm_id IN (SELECT gm_id FROM game WHERE gm_id = {game_id} OR gm_recurr_id = {game_id}"
                )
            else:
                delete_sql = execution.execute(
                    f"DELETE FROM gm_instructors WHERE gm_id IN (SELECT gm_id FROM game WHERE gm_id = {game_recurr_id} OR gm_recurr_id = {game_recurr_id})\
                        DELETE FROM gm_instructors_parents_only WHERE gm_id IN (SELECT gm_id FROM game WHERE gm_id ={game_recurr_id} OR gm_recurr_id = {game_recurr_id}"
                )
                instructor_sql = handle_all_recur_instructorQuery(instructor_id, game_id, game_recurr_id)
                if str(instructor_sql).__contains__('something happened'):
                    raise Exception(instructor_sql)

        # delete old instructor if found
        if delete_sql or delete_sql != "":
            delete_sql = execution.execute(
                f"DELETE FROM gm_instructors WHERE gm_id = {game_id}"
            )

        # insert new instructor
        if instructor_sql or instructor_sql != "":
            instructor_sql = execution.execute(
                f"INSERT INTO gm_instructors (gm_id, instructor_id) VALUES ({game_id},{instructor_id})"
            )

    except Exception as e:
        return "something happened:" + e.__str__()


def handle_one_future_recur_instructorQuery(instructor_id, game_id):
    try:
        # check data
        if type(game_id) != int or game_id < 1:
            raise Exception("Invalid game id ")

        if type(instructor_id) != int or int(instructor_id) < 1:
            raise Exception("Invalid instructor id ")

        # get old instructor for this recur set
        old_instructor_data = get_game_instructor_data(game_id, 0, True)
        if str(old_instructor_data).__contains__('something happened:'):
            raise Exception(old_instructor_data)

        if not old_instructor_data:
            raise Exception("Invalid instructor id ")

        if old_instructor_data['id'] < 1 or old_instructor_data == "":
            raise Exception("Invalid instructor id ")

        # get child classes which no records before
        child_classes = execution.execute(
            f"SELECT gm_id FROM game WHERE gm_recurr_id = {game_id} \
                AND gm_id NOT IN (SELECT gm_id FROM gm_instructors)"
        )

        # insert row for every child class in series
        if child_classes or child_classes != "":
            result = execution.execute(
                f"INSERT INTO gm_instructors (gm_id, instructor_id) VALUES ({game_id} , {instructor_id})"
            )
            for classs in child_classes:
                game_id = int(classs['gm_id'])
                old_instructor_id = int(old_instructor_data['id'])
                result = str(result) + "(" + str(game_id) + ", " + str(old_instructor_id) + "),"

            # result = str(result).strip(',')

        # insert row for parent class
        result = execution.execute(
            f"INSERT INTO gm_instructors (gm_id, instructor_id) VALUES ({game_id},{instructor_id})"
        )
        # return final result
        return result

    except Exception as e:
        return "something happened:" + e.__str__()


def handle_all_recur_instructorQuery(instructor_id, game_id, game_recurr_id):
    try:
        # check data
        if type(game_id) != int or game_id < 1:
            raise Exception("Invalid game id ")

        if type(game_recurr_id) != int:
            raise Exception("Invalid game recurr id ")

        if type(instructor_id) != int or int(instructor_id) < 1:
            raise Exception("Invalid instructor id ")

        """
        * get history classes before this child class
        * get old instructors for these history classes
        * insert individual row for each old/history class with its instructor
        """

        old_classes = execution.execute(
            f"SELECT gm_id, gm_recurr_id FROM game\
                WHERE (gm_id = {game_id} OR gm_recurr_id = {game_recurr_id})\
                AND (gm_utc_datetime + INTERVAL gm_end_time MINUTE) < CURRENT_TIMESTAMP"
        )
        if not old_classes or old_classes == "":
            """
            * all classes in the recur set is upcoming
            * so delete all old records for them
            * and insert one new row for this new parent class
            * and insert one new row for this old parent class
            """
            result = execution.execute(
                f"INSERT INTO gm_instructors \
                (gm_id, instructor_id) \
                VALUES ({game_id}, {instructor_id}),({game_id}, {instructor_id})"
            )

        else:
            """
            * some classes not upcoming
            * so insert rows for them only
            * and insert new row for new parent class(this class)
            """
            result = execution.execute(
                f"INSERT INTO gm_instructors (gm_id, instructor_id) VALUES ({game_id}, {instructor_id})"
            )
            for classs in old_classes:
                class_id = int(classs['gm_id'])
                class_recurr_id = int(classs['gm_recurr_id'])
                instructor_data = get_game_instructor_data(class_id, class_recurr_id)
                if str(instructor_data).__contains__('something happened:'):
                    raise Exception(instructor_data)

                class_instructor_id = instructor_data['id'] if 'id' in instructor_data and instructor_data[
                    'id'] != "" else 0

                if not class_id or not class_instructor_id:
                    continue
                result = str(result) + ", (" + str(class_id) + ", " + str(class_instructor_id) + ")"

                # handle result query
            result = str(result).strip(',')

        return result

    except Exception as e:
        return "something happened:" + e.__str__()


def get_parent_id(game_id, game_recurr_id):
    # parameter game_id ex :6
    # parameter game_recurr_id ex :1
    # return ex: 1

    try:
        if type(game_id) != int or game_id < 1:
            raise Exception("Invalid game id ")

        if int(game_recurr_id) == 0:
            return int(game_id)

        parent_data = execution.execute(
            f"SELECT gm_recurr_id FROM game WHERE gm_id = {game_id}"
        )

        if parent_data[0]['gm_recurr_id'] != "" and int(
                parent_data[0]['gm_recurr_id'] > 0 and int(game_id) >= int(parent_data[0]['gm_recurr_id'])):
            return int(parent_data[0]['gm_recurr_id'])

        return game_recurr_id
    except Exception as e:
        return "something happened:" + e.__str__()


def get_game_instructor_data(game_id, game_recurr_id, for_recur_only=False):
    # parameter game_id ex: 141818
    # parameter Game_recurr_id ex: 1
    # parameter ex :for_recur_only = False
    # return  {'id': 473, 'name': 'sang%20bin-ah', 'bio': 'any', 'image': 'https://images.fastclassapp.com/grand/images/upload/ply/c6a539eed32c3f658552e8f5ed402e72.jpg'}
    try:
        data = {}
        result = {}

        # check data
        if type(game_id) != int or game_id < 1:
            raise Exception("Invalid game id ")

        if type(game_recurr_id) != int:
            raise Exception("Invalid game recurr id ")

        # get instructor if set for this class only in parent table
        if for_recur_only is False:
            sql = execution.execute(
                f"SELECT instructor_id, name, bio, image FROM gm_instructors_parents_only \
                    JOIN instructors ON instructors.id = gm_instructors_parents_only.instructor_id\
                    WHERE gm_id = {game_id}"
            )

            data = sql

            # get instructor data from general table
        if data == "" or data == {}:
            sql = execution.execute(
                f"SELECT instructor_id, name, bio, image \
                FROM gm_instructors \
                JOIN instructors ON instructors.id = gm_instructors.instructor_id\
                WHERE gm_id = {game_id}"
            )
            data = sql

        # get instructor for class from its parent class in general table
        if data == "" or data == {}:
            parent_id = get_parent_id(game_id, game_recurr_id)
            if str(parent_id).__contains__('something happened:'):
                raise Exception(parent_id)
            sql = execution.execute(
                f"SELECT instructor_id, name, bio, image \
                        FROM gm_instructors \
                        JOIN instructors ON instructors.id = gm_instructors.instructor_id\
                        WHERE gm_id = {parent_id}"
            )

            data = sql

            if data == "":
                return result

        # handle returned results
        if data:
            result = {
                "id": data[0]['instructor_id'],
                "name": data[0]['name'],
                "bio": data[0]['bio'],
                "image": data[0]['image']
            }
        return result

    except Exception as e:
        return "something happened:" + e.__str__()


def get_Wait_List_Members(GmID):
    # parameter is array of GmID ex:"6"
    # return array of WaitListMembers ex:[{'gm_wait_list_id': 4566, 'gm_wait_list_gm_id': 272841, 'gm_wait_list_ply_id': 1767, 'gm_wait_list_withdrew': 0, 'gm_wait_list_removed_by_admin': 0, 'gm_wait_list_created': datetime.datetime(2022, 1, 2, 12, 7, 54)}]
    try:
        # check if GmID is not empty and type is int
        if GmID and type(GmID) == int:
            #                                    ## write your query here to get WaitListMembers
            wait_data = execution.execute(
                f"SELECT * FROM gm_waitlist WHERE gm_wait_list_gm_id = {GmID} AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0")
            return wait_data

        else:
            raise Exception("Class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_Utc_Datetime(tZone, dTime):
    # parameter tZone ex :tZone="Europe/London"
    # parameter dTime ex :dTime="2022-10-21 12:30"
    # return ex: " 2022-10-21 11:30:00+01:00"
    try:
        if type(tZone) == str and tZone != '' and type(dTime) == str and dTime != '':
            dTimeDate = datetime.strptime(dTime, '%Y-%m-%d %H:%M')
            utc = dTimeDate.astimezone((pytz.timezone(tZone)))
            return utc
        else:
            raise Exception("tZone or dTime is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_zoom_user(PlyID):
    # parameter is array of PlyID ex:2305
    # return array of zoom_user ex: [{'id': 18, 'ply_id': 2305, 'zoom_user_id': 'klb-qV26AyzBPkHzOA', 'zoom_account_id': None, 'zoom_user_email': 'sally.muhammed2019@gmail.com', 'refresh_token': None, 'created_at': datetime.datetime(2020, 3, 23, 8, 7, 38)}]
    try:
        # check if GmID is not empty and type is int
        if PlyID and type(PlyID) == int:
            #                                    ## write your query here to get zoom_users
            zoom_user = execution.execute(f"SELECT * FROM zoom_users WHERE ply_id = {PlyID};")
            return zoom_user

        else:
            raise Exception("Class_id is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_ply_verified_methods(PlyID):
    # parameter is array of PlyID ex:"6"
    # return array of result ex:{ 'stripe' = "n"}
    try:
        # check if GmID is not empty and type is int
        if PlyID and type(PlyID) == int:
            if PlyID < 1:
                return dict()

            # prepare result data
            result = dict()
            result['stripe'] = "n"
            # check if he has connected stripe account
            player_data = execution.execute(f"SELECT * FROM stripe_users WHERE stripe_users_ply_id = {PlyID};")
            if player_data:
                # check if player is connected to Stripe
                if 'stripe_users_account_id' in player_data[0] and player_data[0]['stripe_users_account_id']:
                    result['stripe'] = "y"

            return result

        else:
            raise Exception("PlyID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def log_edit_action(EditField, newGmData, oldData):
    # parameter is dict of EditField ex:{"GmT": "%20nola1%20test"}
    # parameter is dict of Data ex:{"GmT": "%20nola1%20test"}
    # parameter is dict of oldData ex:{"GmT": "%20nola1%20test"}
    # return is  [{'action_log_id': 189179}]
    try:
        if not EditField or str(EditField['GmID']) == "":
            return {}

        # if Data['result'] == 'error':
        #     raise Exception(response.error(code=Data['code'],
        #                                    message=Data['message'],
        #                                    data=''))

        # newGmData = Data['data']
        # if not newGmData:
        #     return {}

        edits_notes = specify_game_edits_to_historyLog(EditField, oldData)
        if str(edits_notes).__contains__('Something happened:'):
            raise Exception(edits_notes)

        # add class to bundles

        if 'BundlesIds' in EditField and EditField['BundlesIds']:
            isRecurr = 0
            class_id = EditField['GmID']
            if 'ISRecurr' in EditField and newGmData['ISRecurr'] == 'True' and newGmData['RecurrID'] == 0:
                isRecurr = 1
                class_id = EditField['GmID']
            elif 'ISRecurr' in EditField and newGmData['ISRecurr'] == 'True' and newGmData['RecurrID'] > 0:
                isRecurr = 1
                class_id = newGmData['RecurrID']

            bundlesIds = json.dumps(EditField['BundlesIds'], sort_keys=True)
            addGmToBundles = add_class_to_bundles(EditField, class_id, bundlesIds, isRecurr)
            if str(addGmToBundles).__contains__('something happened:') or str(addGmToBundles).__contains__(
                    'Error') or str(addGmToBundles).__contains__('error'):
                raise Exception(addGmToBundles)

        logData = {}
        logNote = ""
        logData['GmID'] = newGmData['GmID']
        logData['OrgId'] = newGmData['OrgID']
        logData['UserId'] = newGmData['OrgID']
        logData['PayType'] = newGmData['PayType']
        logData['Cost'] = str(round(int(newGmData['Fees']), 2))
        logData['SubscriptionId'] = newGmData['STypeID']
        logData['source'] = EditField['source'] if 'source' in EditField else ""

        if ('ISRecurr' in newGmData and newGmData['ISRecurr'] == 'True' and 'RecurrID' in newGmData and int(
                newGmData['RecurrID']) >= 0):
            if 'modify' in EditField:
                if EditField["modify"] == 'all':
                    logNote = "This edit was made to all classes in the set from " + newGmData[
                        "GmDate"] + " onwards. \n"
                if EditField["modify"] == 'one':
                    logNote = "This edit was made to this class only. \n"

            actionLog = 17
        else:
            actionLog = 14
        if logNote or edits_notes:
            logData['Note'] = logNote + edits_notes
            logData['SrcType'] = EditField['source'] if 'source' in EditField else ""
            logData['LogType'] = actionLog
            log = common_utils.logAllActions(logData)
            if str(log).__contains__('something happened'):
                raise Exception(log)
            return log

        else:
            return {}
    except Exception as e:
        return "something happened:" + e.__str__()


def add_class_to_bundles(EditField, classId, bundlesIds, isRecurr):
    # parameter class_id = 6
    # parameter bundlesIds = {"BundlesIds": '676'}
    # parameter isRecurr = 0
    # parameter is dict of EditField ex:{"GmT": "%20nola1%20test"}
    # return   ex: {'result': 'success', 'data': {}, 'code': 200}

    try:
        if EditField and classId and bundlesIds and isRecurr >= 0:
            # params
            params = {'org_id': int(EditField['PlyID']) if 'PlyID' in EditField else 0, 'class_id': classId,
                      'bundles_ids': json.dumps(bundlesIds), 'is_recurr': isRecurr,
                      'dev_id': EditField['DevID'] if 'DevID' in EditField else "",
                      'tkn': EditField['Tkn'] if 'Tkn' in EditField else "",
                      'source': EditField['source'] if 'source' in EditField else "",
                      'ProjectKey': EditField['ProjectKey'] if 'ProjectKey' in EditField else "",
                      'ProjectSecret': EditField['ProjectSecret'] if 'ProjectSecret' in EditField else ""}
            BundleResponse = common_utils.bundle_curl('AddClassToBundles', params)

            return BundleResponse

        else:
            raise Exception("classId is required")

    except Exception as e:
        return "something happened:" + e.__str__()


def specify_game_edits_to_historyLog(EditField, OldData):
    # parameter is dict of EditField ex:{"GmT": "%20nola1%20test"}
    # parameter is dict of OldData ex:{"Gmt":"hhhh"}
    # return str  ex:return " Title : From hhhh to %20nola1%20test"
    try:
        log_note = ""
        if not EditField or type(EditField) != dict or not OldData or type(OldData) != dict:
            return log_note

        if 'GmT' in EditField and 'GmT' in OldData and OldData['GmT'] != EditField['GmT']:
            new_title = urllib.parse.quote(EditField['GmT'])
            old_title = urllib.parse.quote(OldData['GmT'])
            log_note += "Title : From " + old_title + " to " + new_title + "\n"

        if 'GmDate' in EditField and 'GmDate' in OldData and OldData['GmDate'] != EditField['GmDate']:
            olddTe = str(datetime.strptime(OldData["GmDate"], '%Y-%m-%d'))
            dTe = str(datetime.strptime(EditField["GmDate"], '%Y-%m-%d'))
            log_note += " Date : from " + olddTe + " to " + dTe + "\n"

        if 'STime' in EditField and 'STime' in OldData and OldData['STime'] != EditField['STime']:
            s_time = str(datetime.strptime(EditField["STime"], '%H:%M')).split(" ")[1]
            ss_time = OldData['SSTime'] if 'SSTime' in OldData else ""
            log_note += " Time : From " + ss_time + " to " + s_time + "\n"

        if 'AttendType' in EditField and 'attendType' in OldData and OldData['attendType'] != EditField['AttendType']:
            attendType = OldData['attendType'] if 'attendType' in OldData else ""
            log_note += " Attend Type : From " + attendType + " to " + EditField['AttendType'] + "\n"

        if 'STypeID' in EditField and 'STypeID' in OldData and OldData['STypeID'] != EditField['STypeID']:
            new_activity = get_stype_name(EditField['STypeID'])
            if str(new_activity).__contains__('something happened:'):
                raise Exception(new_activity)
            old_activity = get_stype_name(OldData['STypeID'])
            if str(old_activity).__contains__('something happened:'):
                raise Exception(old_activity)
            log_note += " Activity : From " + old_activity + " to " + new_activity + "\n"

        if 'CourtID' in EditField and 'CourtID' in OldData and OldData['CourtID'] != EditField['CourtID']:
            new_surface = "Indoors" if int(EditField['CourtID']) == 1 else "Outdoors"
            old_surface = "Indoors" if int(OldData['CourtID']) == 1 else "Outdoors"
            log_note += " Surface : From " + old_surface + " to " + new_surface + "\n"

        if 'LevelID' in EditField and 'LevelID' in OldData and OldData['LevelID'] != EditField['LevelID']:
            new_level = get_level_name(EditField['LevelID'])
            if str(new_level).__contains__('something happened:'):
                raise Exception(new_level)
            old_level = get_level_name(OldData['LevelID'])
            if str(old_level).__contains__('something happened:'):
                raise Exception(old_level)
            log_note += " Level : From " + old_level + " to " + new_level + "\n"

        if 'Minply' in EditField and 'MinPly' in OldData and OldData['MinPly'] != EditField['Minply']:
            log_note += " Minimum attendees : From " + str(OldData['MinPly']) + " to " + str(EditField['Minply']) + "\n"

        if 'Maxply' in EditField and 'MaxPly' in OldData and OldData['MaxPly'] != EditField['Maxply']:
            log_note += " Maximum attendees : From " + str(OldData['MaxPly']) + " to " + str(EditField['Maxply']) + "\n"

        if 'ETime' in EditField and 'ETime' in OldData and str(OldData['ETime']) != str(EditField['ETime']):
            log_note += " Duration : From " + str(OldData['ETime']) + " to " + str(EditField['ETime']) + "\n"

        if 'LocDesc' in EditField and 'LocDesc' in OldData and OldData['LocDesc'] != EditField['LocDesc']:
            EditField['LocDesc'] = urllib.parse.quote(EditField['LocDesc'])
            log_note += " Location Description : From " + OldData['LocDesc'] + " to " + EditField['LocDesc'] + "\n"

        if 'Desc' in EditField and 'Desc' in OldData and OldData['Desc'] != EditField['Desc']:
            EditField['Desc'] = urllib.parse.quote(EditField['Desc'])
            log_note += " Description : From " + OldData['Desc'] + " to " + EditField['Desc'] + "\n"

        if 'Scope' in EditField and EditField['Scope'] != "" and 'Scope' in OldData and OldData['Scope'] != EditField[
            'Scope']:
            showMem = "Privacy : From hidden to public" if (
                    EditField['Scope'] == "Open to public") else "Privacy : From public to hidden"
            log_note += showMem + "\n"

        new_payment_type = ""
        if 'PayType' in EditField and 'PayType' in OldData and str(OldData['PayType']).lower() != str(
                EditField['PayType']).lower():
            old_payment_type = "free" if OldData['PayType'] == "" else OldData['PayType']
            new_payment_type = "free" if EditField['PayType'] == "" else EditField['PayType']
            old_payment_type = "online" if str(old_payment_type).lower() == "stripe" else old_payment_type
            new_payment_type = "online" if str(new_payment_type).lower() == "stripe" else new_payment_type
            log_note += " Payment type : From " + old_payment_type + " to " + new_payment_type + "\n"

        if 'PolicyID' in EditField and 'PolicyID' in OldData and OldData['PolicyID'] != EditField[
            'PolicyID'] and new_payment_type != "free":
            new_policy = get_policy_title(EditField['PolicyID'])
            if str(new_policy).__contains__('something happened:'):
                raise Exception(new_policy)
            old_policy = get_policy_title(OldData['PolicyID'])
            if str(old_policy).__contains__('something happened:'):
                raise Exception(old_policy)
            log_note += " Refund policy : From " + old_policy + " to " + new_policy + "\n" if old_policy != "" else " Refund policy : To " + new_policy + "\n"

        if 'GmReqQues' in EditField and 'GmReqQues' in OldData and OldData['GmReqQues'] != EditField['GmReqQues'] and \
                EditField['GmReqQues'] != 0:
            log_note += " Medical questionnaire : From " + OldData['GmReqQues'] + " to " + EditField['GmReqQues'] + "\n"

        # check if currency changed with cost or not in history log.
        new_cost = 0
        symbol = 0

        if 'Symbol' in EditField and int(EditField['Symbol']) >= 0:
            symbol = int(EditField['Symbol'])

        currency_data = get_currency_data(int(symbol))
        if str(currency_data).__contains__('something happened:'):
            raise Exception(currency_data)

        new_currency = currency_data[0]['currency_symbol'] if 'currency_symbol' in currency_data[0] else ""
        old_currency = OldData['Symbol'] if 'Symbol' in OldData else ""
        # when currency changes with cost while edit game.
        if 'Fees' in EditField and 'Fees' in OldData and OldData['Fees'] != EditField['Fees']:
            new_cost = "Free" if int(EditField['Fees']) == 0 else EditField['Fees']
            log_note += " Cost : From " + str(old_currency) + "" + str(OldData['Fees']) + " to " + str(
                new_currency) + "" + str(new_cost) + "\n"

        if new_currency and old_currency and old_currency != new_currency and int(new_cost) != 0:
            log_note += " Currency : From " + str(old_currency) + " to " + str(new_currency) + "\n"

        if new_currency and not old_currency and int(new_cost) != 0:
            log_note += " Currency : To " + str(new_currency) + "\n"

        # check if image changed for history log.
        if 'imgChanged' in EditField and EditField['imgChanged'] is True:
            log_note += " Image got changed \n"

        # handle questionnaire questions for history log.
        oldQuestionnairQues = OldData['GmQues'] if 'GmQues' in OldData else ""
        newQuestionnairQues = EditField['QuesObj']['QuesDetails'] if 'QuesObj' in EditField else []
        sql_list = []

        if 'QuesObj' in EditField:
            oldQuesArr = [e['QuesID'] for e in oldQuestionnairQues]
            newQuesArr = [e['id'] for e in newQuestionnairQues]

            if str(OldData['GmReqQues']).lower() == "no" and str(EditField['GmReqQues']).lower() == "yes":
                # if there were no questions before then insert all new questions.
                log_note += " New question got added : \n"
                for value in newQuestionnairQues:
                    sql_list.append(value['id'])

                SqlArray = str(tuple([key for key in sql_list])).replace(',)', ')')
                quesRes = execution.execute(f"SELECT ques_title FROM questionnaire WHERE ques_id IN {SqlArray}")
                for ques in quesRes:
                    log_note += ques['ques_title'] + "\n"
            elif str(EditField['GmReqQues']).lower() == "yes":
                firstAddedQues = True
                firstDeletedQues = True
                for newVal in newQuesArr:
                    # check if an ID doesn't exist in oldArr , then this is a new Ques
                    if newVal not in oldQuesArr:
                        if firstAddedQues:
                            log_note += " New question got added : \n"
                            firstAddedQues = False

                        sql_list.append(newVal)

                for oldVal in oldQuesArr:
                    # check if an ID doesn't exist in newArr , then this Ques was deleted.
                    if oldVal not in newQuesArr:
                        if firstDeletedQues:
                            log_note += " Question got removed : \n"
                            firstDeletedQues = False

                        sql_list.append(oldVal)

                SqlArray = str(tuple([key for key in sql_list])).replace(',)', ')')
                quesRes = execution.execute(f"SELECT ques_title FROM questionnaire WHERE ques_id IN {SqlArray}")
                for ques in quesRes:
                    log_note += ques['ques_title'] + "\n"

        return log_note

    except Exception as e:
        return "something happened:" + e.__str__()


def get_stype_name(STypeID):
    # parameter is int of STypeID ex:6
    # return str  ex:"Baseball"
    try:
        # check if STypeID is not empty and type is int
        if STypeID and type(STypeID) == int:
            #                                    ## write your query here to get gm_s_type_name
            gm_s_type_name = execution.execute(f"SELECT gm_s_type_name FROM gm_s_types WHERE gm_s_type_id = {STypeID};")
            if gm_s_type_name:
                return gm_s_type_name[0]["gm_s_type_name"]
            else:
                return gm_s_type_name
        else:
            raise Exception("STypeID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_level_name(LevelID):
    # parameter is int of LevelID ex:6
    # return string level_title ex : "Intermediate"
    try:
        # check if LevelID is not empty and type is int
        if LevelID and type(LevelID) == int:
            #                                    ## write your query here to get level_title
            level_title = execution.execute(f"SELECT level_title FROM level WHERE level_id = {LevelID};")
            if level_title:
                return level_title[0]["level_title"]
            else:
                return level_title

        else:
            raise Exception("LevelID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_currency_data(symbol):
    # parameter is int of symbol ex:6
    # return string currency_data ex :  [{'currency_name': 'usd', 'currency_symbol': '$'}]
    try:
        # check if currency_data is not empty and type is int
        if symbol and type(symbol) == int:
            #                                    ## write your query here to get policy_title
            currency_data = execution.execute(
                f"SELECT currency_name,currency_symbol FROM currencies WHERE currency_id= {symbol};")
            return currency_data

        else:
            raise Exception("symbol is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def get_policy_title(PolicyID):
    # parameter is int of PolicyID ex:6
    # return string policy_title ex : "100 Percent (1 hour)"
    try:
        # check if PolicyID is not empty and type is int
        if PolicyID and type(PolicyID) == int:
            #                                    ## write your query here to get policy_title
            policy_title = execution.execute(f"SELECT policy_title FROM policy WHERE policy_id = {PolicyID};")
            if policy_title != "":
                return policy_title[0]['policy_title']
            else:
                return policy_title
        else:
            raise Exception("PolicyID is required")
    except Exception as e:
        return "something happened:" + e.__str__()


def check_friennd_req(pend_ply_frm_id, player_id, accept='p'):
    invitation = 0

    inv_row = execution.execute(f"SELECT * FROM invitations WHERE inv_gm_id = 0 AND \
                    inv_accept = '{accept}' AND ((inv_ply_frm_id = {pend_ply_frm_id} AND inv_ply_to_id = {player_id}) \
                    OR (inv_ply_to_id = {player_id} AND inv_ply_frm_id = {pend_ply_frm_id}))")
    if inv_row:
        invitation = inv_row['inv_id']
    return invitation


def bundle_details(class_id, org_id, contact_id=0, class_datetime="", ply_id=0, dev_id="", tkn="", new_client=0,
                   ProjectSecret="", ProjectKey=""):
    try:
        if (
                class_id > 0 and org_id > 0 and contact_id and class_datetime != "" and dev_id != "" and tkn != "" and ProjectKey != "" and ProjectKey != ""):
            params = {'class_id': class_id, 'org_id': org_id,
                      'class_datetime': class_datetime, 'ply_id': ply_id,
                      'contact_id': contact_id,
                      'dev_id': dev_id, 'tkn': tkn, 'new_client': new_client,
                      'ProjectSecret': ProjectSecret, 'ProjectKey': ProjectKey}
        else:
            raise Exception(response.error('Paramteres of bundle details missing'))

        return common_utils.bundle_curl('playerBundles', params=params)

    except Exception as e:
        return e


def updateCredit(class_id, bundle_id, ply_id=0, ply_email="", ProjectSecret="", ProjectKey=""):
    try:
        if (class_id > 0 and bundle_id > 0 and ProjectKey != "" and ProjectKey != ""):

            params = {'class_id': class_id, 'bundle_id': bundle_id,
                      'ply_id': ply_id, 'ply_email': ply_email, 'process': '-', 'ProjectSecret': ProjectSecret,
                      'ProjectKey': ProjectKey}
        else:
            raise Exception(response.error('Paramteres of Credit missing'))

        return common_utils.bundle_curl('updatePlayerCredit', params=params)

    except Exception as e:
        return e


def add_to_subs(class_id, ply_id=0, subs_id=0, mail=""):
    try:
        if class_id > 0 and subs_id:
            if ply_id > 0:
                execution.execute(
                    f"INSERT INTO games_subscriptions(game_id, subscription_id, member_id) VALUES ({class_id},{subs_id},{ply_id})")
            elif ply_id == 0 and mail != "":
                execution.execute(
                    f"INSERT INTO games_subscriptions(game_id, subscription_id, member_id,member_email) VALUES ({class_id},{subs_id},0,'{mail}')")
        else:
            raise Exception(response.error('Paramteres of Subscribition missing'))

    except Exception as e:
        return e


def handleClassCurrencySymbol(game_symbol="", currency_name="", ply_country_id=0, org_country_id=0):
    try:
        if (game_symbol == None or currency_name == None):
            return ''
        if (int(ply_country_id) != int(org_country_id) and currency_name != '' and currency_name != None):
            return currency_name.upper()
        else:
            return game_symbol
    except Exception as e:
        return e


def getGmLocalDateTime(time_zone, gm_attend_type, gm_utc_date_time):
    try:
        if (
                time_zone and time_zone != '' and gm_attend_type and gm_attend_type != '' and gm_utc_date_time and gm_utc_date_time != ''):
            if (gm_attend_type == 'zoom'):
                tz = gm_utc_date_time.replace(tzinfo=pytz.utc).astimezone(time_zone)
                gmDate = tz.strftime("%Y-%m-%d")
                gmTime = tz.strftime("%H:%M:%S")
                return [gmDate, gmTime]
        else:
            return []

    except Exception as e:
        return e


def preparePlyStatusWithGame(PlyID=0, game_table_alias=""):
    try:
        if (PlyID == 0):
            return ''
        else:
            if (game_table_alias != ""):
                game_table_alias = game_table_alias + "."
            memberInGm = f"IFNULL((SELECT gm_ply_id FROM gm_players WHERE gm_ply_gm_id = {game_table_alias} gm_id AND gm_ply_ply_id = {PlyID} AND gm_ply_status = 'y' LIMIT 1), 0)"
            invitedToGm = f"IFNULL((SELECT inv_id FROM invitations WHERE inv_gm_id = {game_table_alias} gm_id AND inv_ply_to_id = {PlyID} AND inv_approve = 'y' LIMIT 1), 0)"
            waitlistInGm = f"IFNULL((SELECT gm_wait_list_id FROM gm_waitlist WHERE gm_wait_list_gm_id = {game_table_alias} gm_id AND gm_wait_list_ply_id = {PlyID} AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0 LIMIT 1), 0)"
            requestBefore = f"IFNULL((SELECT inv_id FROM invitations WHERE inv_gm_id = {game_table_alias} gm_id AND inv_ply_frm_id = {PlyID} LIMIT 1), 0)"

        return (f"(CASE WHEN ({memberInGm}) > 0 THEN 'Mem' WHEN({waitlistInGm}) > 0 THEN 'Wait'\
        WHEN({invitedToGm}) > 0 THEN 'Inv' ELSE 'No' END) AS PlyStatus,\
        (CASE WHEN ({invitedToGm}) > 0 THEN 'True' ELSE 'False' END) AS InvGm,\
        (CASE WHEN ({requestBefore}) > 0 THEN 'True' ELSE 'False' END) AS Req,\
        (CASE WHEN ({memberInGm}) > 0 THEN 'True' ELSE 'False' END) AS Mem,\
        (CASE WHEN ({waitlistInGm}) > 0 THEN 'True' ELSE 'False' END) AS Wait")
    except Exception as e:
        return e


def remove_nulls(result):
    for k, v in result.items():
        if result[k] is None:
            result[k] = ""
    return result


def get_ply_images(img_name = '', player_s3_status = 0):
    try:
        if not img_name:
            img_name = 'ply.png'

        res_arr = {}
        res_arr['PlyImg'] = s3_bucket_url + 'backup/images/upload/ply/' + img_name
        res_arr['PlyImgThumb'] = s3_bucket_url + 'backup/images/upload/ply/' + img_name


        if int(player_s3_status == 1):
            thumb_image_path = img_name.str_replace("profile", "profile/thumb")

            res_arr['PlyImg'] = s3_bucket_url +  img_name
            res_arr['PlyImgThumb'] = s3_bucket_url +  thumb_image_path


        return res_arr

    except Exception as e:
        return "something happened:" + e.__str__()
