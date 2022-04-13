import base64
import binascii
import json
import os
import urllib
import urllib.parse
from datetime import datetime
from urllib.request import urlopen
from database import config
import pytz
import controllers.admin_controller as admin_controller
import database.execution as execution
import database.response as response
import utils.game_utils as game_utils
import utils.notification_utils as notification_utils
import utils.payment_utils as payment_utils
import utils.player_utils as player_utils
import utils.questionnaire_utils as questionnaire_utils
import utils.waitlist_utils as waitlist_utils
import utils.common_utils as common_utils
import utils.validation_utils as validation_utils

s3_bucket_url = config.s3_bucket_url


def join_class(data):
    # check game exists, game cancelled,game expired,game pause , age accept player date
    # data={'class_id': 240292, 'org_id': 1928,
    #                  'ply_id': 1598, 'ProjectKey': 1234,
    #                  'ProjectSecret': 1234, 'source': "web", "coupon_code": "12151512154484", "contact_email": "23j",
    #                  'tkn': 'fa0161bc5d8d5a8ae81a08f41fe cdf ab03db1f7b', 'dev_id': 'fcc78fd5d99ead13', 'pay_choice': 0,'pay_type':'stripe',
    #                   'fees': 50.0, 'sub_id': 0,'currency_id':1,'join_type':"credit"}
    try:
        if 'ply_id' in data and type(data['ply_id']) == int and data['ply_id'] >= 0 and 'class_id' in data and type(
                data['class_id']) == int and data['class_id'] >= 0 and 'org_id' in data and type(
            data['org_id']) == int and data['org_id'] >= 0:
            # gm_age = execution.execute(
            #     f"SELECT  gm_id AS GmID ,gm_age FROM game  WHERE  gm_utc_datetime >NOW() and (gm_status is NULL or gm_status ='' or gm_status = 'admin') and gm_id={data['class_id']};")
            # if str(gm_age).__contains__('Something went wrong'):
            #     log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
            #                 'Note': "player age not valid to the game age range", 'SrcType': data['source'],
            #                 'LogType': 0}
            #     raise Exception(response.error(message=gm_age, data=log_dict))
            # if not gm_age or 'GmID' not in gm_age[0] or 'gm_age' not in gm_age[0]:
            #     log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
            #                 'Note': "player age not valid to the game age range", 'SrcType': data['source'],
            #                 'LogType': 0}
            #
            #     raise Exception(response.error(message='gm_age not found', data=log_dict))
            # if gm_age:
            #     ply_age = execution.execute(
            #         f"SELECT distinct TIMESTAMPDIFF(YEAR, ply_brithdate, CURDATE()) AS ply_age FROM players where ply_id={data['ply_id']};")
            #     if str(ply_age).__contains__('Something went wrong'):
            #         raise Exception(response.error(message=ply_age))
            #     if ply_age is not None:
            #         if gm_age[0]['gm_age'] == 3:
            #             gm_valid = True
            #         elif "ply_age" in ply_age[0] and gm_age[0]['gm_age'] == 2 and ply_age[0]['ply_age'] < 18:
            #             gm_valid = True
            #         elif "ply_age" in ply_age[0] and gm_age[0]['gm_age'] == 1 and ply_age[0]['ply_age'] >= 18:
            #             gm_valid = True
            #         else:
            #             log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
            #                         'Note': "player age not valid to the game age range", 'SrcType': data['source'],
            #                         'LogType': 0}
            #             raise Exception(response.error(code=119, message="player age not valid to the game age range",
            #                                            data=log_dict))
            #     else:
            #         log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
            #                     'Note': "player age is required must be entered", 'SrcType': data['source'],
            #                     'LogType': 0}
            #         raise Exception(response.error(code=624, message='Missing Player BirthDate', data=log_dict))
            # else:
            #     log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
            #                 'Note': "Class have problem", 'SrcType': data['source'], 'LogType': 2}
            #     raise Exception(response.error(code=115, message='Class have problem', data=log_dict))
            # if gm_valid is True:
            capacity = game_utils.class_capacity(data['class_id'], data['org_id'], data['ply_id'], data['pay_type'],
                                                 data['coupon_code'], data['tkn'], data['dev_id'],
                                                 data['pay_choice'],
                                                 data['ProjectKey'], data['ProjectSecret'], data['join_type'],
                                                 data['fees'],
                                                 data['currency_id'])
            if str(capacity).__contains__("something happened:"):
                log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
                            'Note': capacity, 'SrcType': data['source'], 'LogType': 2}
                raise Exception(response.error(message=capacity, data=log_dict))
            else:
                ply_data = execution.execute(
                    f"SELECT ply_fname,ply_lname from players where ply_id = {data['ply_id']}")
                if str(ply_data).__contains__('Something went wrong'):
                    raise Exception(ply_data)
                if not ply_data or 'ply_fname' not in ply_data[0] or 'ply_lname' not in ply_data[0]:
                    raise Exception('invalid player data')
                gm_data = execution.execute(f"SELECT gm_title from game where gm_id = {data['class_id']}")
                email_notification = {'class_id': data['class_id'], 'player_id': data['ply_id'],
                                      "organizer_id": data['org_id'],
                                      'player_name': str(ply_data[0]['ply_fname']) + str(ply_data[0]['ply_lname']),
                                      'class_title': gm_data[0]['gm_title'], 'class_date': data['gm_date']}
                log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
                            'Note': capacity, 'SrcType': data['source']}
                if str(capacity).__contains__('waiting'):
                    log_dict['LogType'] = 3
                    email_notification['message_text'] = "you are in the waiting list"
                    email_notification['wait_list'] = True
                else:
                    log_dict['LogType'] = 1
                    email_notification['message_text'] = "you are member now"
                    email_notification['wait_list'] = False
                return response.success(result_data=capacity, email_notifications=email_notification)
        else:
            log_dict = {'UserId': data['ply_id'], 'GmID': data['class_id'], 'OrgId': data['org_id'],
                        'Note': "org_id,class_id and ply_id are required", 'SrcType': data['source'], 'LogType': 2}
            raise Exception(
                response.error(message="org_id,class_id and ply_id are required in correct format", data=log_dict))
    except Exception as e:
        return e


def withdrew(data):
    """"
                desc: withdrew member/guest from game or wait list
                input: class_id, ply_id, source, ProjectKey, ProjectSecret
                output: return true if action is done or false when error is raised
    """
    try:
        if data['class_id'] and int(data['class_id']) > 0 and data['ply_id'] and int(data['ply_id']) > 0:
            class_data = game_utils.getClassData(SqlArray=f"({data['class_id']})")
            check_if_waitlist = execution.execute(
                f"SELECT gm_wait_list_id,gm_wait_list_withdrew,gm_wait_list_removed_by_admin FROM gm_waitlist WHERE gm_wait_list_gm_id={data['class_id']} AND gm_wait_list_ply_id={data['ply_id']};")
            if check_if_waitlist and check_if_waitlist[0]['gm_wait_list_id'] != []:
                if check_if_waitlist[0]['gm_wait_list_withdrew'] != 1 and check_if_waitlist[0][
                    'gm_wait_list_removed_by_admin'] != 1:
                    execution.execute(
                        f"UPDATE gm_waitlist SET gm_wait_list_withdrew = 1 WHERE gm_wait_list_gm_id={data['class_id']} AND gm_wait_list_ply_id={data['ply_id']};")
                    invitation = execution.execute(
                        f"SELECT inv_id FROM invitations WHERE inv_gm_id = {data['class_id']} AND inv_ply_to_id = {data['ply_id']};")
                    if invitation and invitation[0]['inv_id']:
                        execution.execute(
                            f"DELETE FROM invitations WHERE inv_gm_id ={data['class_id']} AND inv_ply_to_id = {data['ply_id']};")
                    return True
                else:
                    raise Exception('User already withrdawn from waitlist')
            elif not check_if_waitlist:
                if_guest = execution.execute(
                    f"SELECT guest_id FROM guests WHERE guest_gm_id={data['class_id']} and guest_ply_id={data['ply_id']};")
                if if_guest and if_guest[0]['guest_id'] != []:
                    execution.execute(
                        f"UPDATE gm_players SET gm_ply_status = 'r' , gm_ply_leave=CURRENT_TIMESTAMP WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                    execution.execute(
                        f"DELETE FROM guests WHERE guest_ply_id={data['ply_id']} and guest_gm_id={data['class_id']};")
                    execution.execute(
                        f"DELETE FROM games_subscriptions WHERE game_id ={data['class_id']} AND member_id={data['ply_id']};")
                    check_guest_pay_type = execution.execute(
                        f"SELECT id FROM subscriptions_classes WHERE ply_id={data['ply_id']} and class_id={data['class_id']};")
                    if check_guest_pay_type:
                        game_utils.check_refund_policy(class_id=data['class_id'], ply_id=data['ply_id'],
                                                       source=data['source'],
                                                       ProjectSecret=data['ProjectSecret'],
                                                       ProjectKey=data['ProjectKey'])
                    class_data = game_utils.getClassData(SqlArray=f"({data['class_id']})")
                    game_utils.informWaitlist(ClassesData=class_data, SqlArray=f"({data['class_id']})")
                else:
                    if_member = execution.execute(
                        f"SELECT gm_ply_id,gm_ply_status,gm_ply_refunded,gm_ply_pay_type FROM gm_players WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                    if if_member and if_member != []:
                        if if_member[0]['gm_ply_status'] == 'r':
                            raise Exception("You are not a member")
                        elif if_member and if_member[0]['gm_ply_status'] == 'y':
                            execution.execute(
                                f"UPDATE gm_players SET gm_ply_status = 'r' , gm_ply_leave=CURRENT_TIMESTAMP WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                            execution.execute(
                                f"DELETE FROM games_subscriptions WHERE game_id ={data['class_id']} AND member_id={data['ply_id']};")
                            if if_member[0]['gm_ply_pay_type'] != 'no' or if_member[0]['gm_ply_refunded'] != 1:
                                game_utils.check_refund_policy(class_id=data['class_id'], ply_id=data['ply_id'],
                                                               source=data['source'],
                                                               ProjectSecret=data['ProjectSecret'],
                                                               ProjectKey=data['ProjectKey'])
                                execution.execute(
                                    f"UPDATE gm_players SET gm_ply_refunded =1 WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                            game_utils.informWaitlist(ClassesData=class_data, SqlArray=f"({data['class_id']})")
                    else:
                        raise Exception('You are not a member')
        else:
            raise Exception("Game and Player id are required")
    except Exception as e:
        return response.error(e.__str__())
    else:
        return response.success(result_data={"GmData": json.dumps(class_data, indent=4, sort_keys=True, default=str),
                                             "showMoreLink": 'False',
                                             "WithSuccMess": "You have withdrawn from this class."})


def view_game(data):
    try:
        # validate data parameter with schema
        # validate_payload_schema(view_game_schema, data)
        # check game and player are existed
        # data["GmID"],data["PlyID"],data['tkn'],data['dev_id'],data['ProjectKey'],data['ProjectSecret']
        game_info = game_utils.get_game_player_data(game_id=int(data["GmID"]), player_id=int(data["PlyID"]),
                                                    tkn=data['tkn'],
                                                    dev_id=data['dev_id'], ProjectKey=data['ProjectKey'],
                                                    ProjectSecret=data['ProjectSecret'])
        if type(game_info) == str:
            raise Exception(response.error(message=game_info))
        game_flags = game_utils.get_game_flags(int(data["GmID"]), int(data["PlyID"]))
        if type(game_flags) == str:
            raise Exception(response.error(message=game_flags))
        player_flags = player_utils.get_player_flags(int(data["GmID"]), int(data["PlyID"]))
        if type(player_flags) == str:
            raise Exception(response.error(message=player_flags))
        notification_flags = notification_utils.get_notification_flags(int(data["GmID"]), int(data["PlyID"]))
        if type(notification_flags) == str:
            raise Exception(response.error(message=notification_flags))
        game_pay_methods = payment_utils.get_player_payment_methods()
        if type(game_pay_methods) == str:
            raise Exception(response.error(message=game_pay_methods))
        player_pay_methods = payment_utils.get_game_payment_methods()
        if type(player_pay_methods) == str:
            raise Exception(response.error(message=player_pay_methods))
        game_questions = questionnaire_utils.get_game_questionnaire_data(int(data["GmID"]))
        if type(game_questions) == str:
            raise Exception(response.error(message=game_questions))
        player_answers = questionnaire_utils.get_player_questionnaire_answers(int(data["GmID"]), int(data["PlyID"]))
        if type(player_answers) == str:
            raise Exception(response.error(message=player_answers))
        waitlist_players = waitlist_utils.get_game_waitlist_players(int(data["GmID"]))
        if type(waitlist_players) == str:
            raise Exception(response.error(message=waitlist_players))
        result = {**game_info, **game_flags, **player_flags, **notification_flags, **game_pay_methods,
                  **player_pay_methods, **game_questions, **player_answers, **waitlist_players}
        for k, v in result.items():
            if result[k] is None:
                result[k] = ""
        return response.success(result)
    except Exception as e:
        return e


def view_game_org_view(data):
    try:
        game_info = game_utils.get_game_info_to_org_view(game_id=int(data["game_id"]), player_id=int(data["player_id"]),
                                                         token=data["token"], dev_id=data["dev_id"])

        if type(game_info) == str:
            raise Exception(response.error(message=game_info))

        # result = {**game_info}
        result = game_info
        return response.success(result)
    except Exception as e:
        return e


# ##################### work for rewnew game ###########################

def renew_game(data):
    # game_id, game_date, game_date_utc ,project_id ,player_id, ProjectKey, ProjectSecret, tkn, dev_id , modify_type):
    """
    description : renew a game with renewal date using game id and renewal date
    param: game id 
    param: renew game date 
    param: renew game date utc
    return: game id
    """
    try:
        # check data 
        if type(data["game_id"]) != int or data["game_id"] < 1:
            raise Exception("Invalid game id ")
        if data["game_date"] == "":
            raise Exception("Invalid game date ")
        if data["game_date_utc"] == "":
            raise Exception("Invalid game date utc")
        # get game data 
        game_data = game_utils.get_game_player_data(data["game_id"], data["player_id"], data["ProjectKey"],
                                                    data["ProjectSecret"], data["tkn"], data["dev_id"])
        ply_id = game_data['OrgID']

        # get game flags ( parent and recurr )
        game_flags = game_utils.get_game_flags(data["game_id"], ply_id)
        is_recurr = game_flags["ISRecurr"]
        is_parent = game_flags["Parent"]
        if is_recurr is True and is_parent is True:
            raise Exception("Class can\'t be renewed")

        currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "%Y-%m-%d %H:%M:%S")

        try:
            game_date_time_utc = data["game_date_utc"]
            datetime_object = datetime.strptime(game_date_time_utc, '%Y-%m-%d %H:%M:%S')
            new_game_date = datetime_object.date()
        except:
            game_date_time_utc = data["game_date"] + " " + game_data['STime']
            datetime_object = datetime.strptime(game_date_time_utc, '%Y-%m-%d %H:%M:%S')
            new_game_date = datetime_object.date()

        if currentTime > datetime_object:
            raise Exception("Select upcoming time please")

        # for online class
        if game_data['attendType'] != "" and game_data['attendType'] == "zoom":
            zoom_user = execution.execute(
                f"SELECT * FROM zoom_users WHERE ply_id={ply_id}")

            if zoom_user == "" or zoom_user['refresh_token'] == "":
                raise Exception("You are not connected in zoom service , please go to tools and connect it!")

            zoom_user_id = zoom_user['zoom_user_id']
            timeZone = game_data['timeZone'] if game_data['timeZone'] != "" else game_data['timeZone'] == 'UTC'
            startTime = datetime.strptime(game_date_time_utc, "%Y-%m-%d %H:%M:%S")

            meeting_data = {'topic': urllib.parse.quote(game_data[0]['GmT']), 'agenda': "", 'type': 2,
                            'start_time': startTime, 'timezone': timeZone, 'duration': game_data[0]['ETime']}

        # refresh token 

        # create meeting
        zoom_meeting_id = ""
        zoom_url = ""
        zoom_pwd = ""
        # insert row for game with renew date but old data
        old_game_data = execution.execute(
            f"SELECT * FROM game WHERE gm_id={data['game_id']}")
        try:
            execution.execute(
                f"INSERT INTO game (gm_title, gm_org_id, gm_display_org, gm_sub_type_id,gm_court_id,\
                gm_level_id,gm_img,gm_gender,\
                gm_age,gm_age_min,gm_age_max,gm_min_players,gm_max_players,gm_max_players_orig,gm_date,gm_start_time,gm_end_time,gm_utc_datetime,gm_unix_utc_datetime,\
                gm_unix_utc_end_datetime,gm_zip_code,gm_city_id,gm_country_id,gm_loc_lat,gm_loc_long,gm_loc_desc,gm_scope,gm_has_gallery,gm_desc,gm_requirements,gm_notes,gm_rules,\
                gm_kits,gm_is_free,gm_payment_type,attend_type,zoom_url,zoom_meeting_id,zoom_pwd,gm_fees,gm_currency_symbol,gm_policy_id,gm_recurr_times,\
                gm_recurr_type,gm_copy_id,gm_copy_ques_from,gm_renew_id,gm_showMem,gm_reqQues,gm_end_pause,gm_status,gm_recurr_cancel_type,\
                gm_pid,gm_recurr_days_times,gm_time_zone)\
                Values ('{old_game_data[0]['gm_title']}', {old_game_data[0]['gm_org_id']},\
                '{old_game_data[0]['gm_display_org']}',{old_game_data[0]['gm_sub_type_id']}, {old_game_data[0]['gm_court_id']},{old_game_data[0]['gm_level_id']},\
                '{old_game_data[0]['gm_img']}','{old_game_data[0]['gm_gender']}', \
                {old_game_data[0]['gm_age']},{old_game_data[0]['gm_age_min']},{old_game_data[0]['gm_age_max']},\
                {old_game_data[0]['gm_min_players']},{old_game_data[0]['gm_max_players']},\
                {old_game_data[0]['gm_max_players_orig']},'{new_game_date}','{old_game_data[0]['gm_start_time']}',{old_game_data[0]['gm_end_time']},'{datetime_object}',\
                {old_game_data[0]['gm_unix_utc_datetime']},{old_game_data[0]['gm_unix_utc_end_datetime']},'{old_game_data[0]['gm_zip_code']}',{old_game_data[0]['gm_city_id']},\
                {old_game_data[0]['gm_country_id']},{old_game_data[0]['gm_loc_lat']},{old_game_data[0]['gm_loc_long']},'{old_game_data[0]['gm_loc_desc']}','{old_game_data[0]['gm_scope']}',\
                '{old_game_data[0]['gm_has_gallery']}','{old_game_data[0]['gm_desc']}','{old_game_data[0]['gm_requirements']}','{old_game_data[0]['gm_notes']}','{old_game_data[0]['gm_rules']}', \
                '{old_game_data[0]['gm_kits']}','{old_game_data[0]['gm_is_free']}','{old_game_data[0]['gm_payment_type']}','{old_game_data[0]['attend_type']}','{zoom_url}','{zoom_meeting_id}', \
                '{zoom_pwd}',{old_game_data[0]['gm_fees']},'{old_game_data[0]['gm_currency_symbol']}',{old_game_data[0]['gm_policy_id']},{old_game_data[0]['gm_recurr_times']},\
                '{old_game_data[0]['gm_recurr_type']}',{old_game_data[0]['gm_copy_id']},{old_game_data[0]['gm_copy_ques_from']},{old_game_data[0]['gm_renew_id']},\
                {old_game_data[0]['gm_showMem']},{old_game_data[0]['gm_reqQues']},{old_game_data[0]['gm_end_pause']},\
                '{old_game_data[0]['gm_status']}','{old_game_data[0]['gm_recurr_cancel_type']}',\
                {old_game_data[0]['gm_pid']},'{old_game_data[0]['gm_recurr_days_times']}','{old_game_data[0]['gm_time_zone']}')"
            )

        except Exception as e:
            return "something happened:" + e.__str__()
            # add instructor data to game if found
        instructor_data = game_utils.get_game_instructor_data(data["game_id"], 0, True)
        if instructor_data != "" and instructor_data['id'] != "":
            game_utils.handle_game_instructor(int(data['game_id']), int(game_data['RecurrID']),
                                              instructor_data['id'])

        # execution.execute( f"SELECT last_insert_id()")

        game_id = execution.execute(
            f"SELECT gm_id FROM game WHERE gm_title = '{old_game_data[0]['gm_title']}' and  gm_org_id = {old_game_data[0]['gm_org_id']} and\
                gm_display_org = '{old_game_data[0]['gm_display_org']}' and gm_sub_type_id = {old_game_data[0]['gm_sub_type_id']} and gm_court_id = {old_game_data[0]['gm_court_id']} and \
                gm_level_id = {old_game_data[0]['gm_level_id']} and gm_img = '{old_game_data[0]['gm_img']}' and gm_gender = '{old_game_data[0]['gm_gender']}' and \
                gm_age = {old_game_data[0]['gm_age']} and gm_age_min = {old_game_data[0]['gm_age_min']} and gm_age_max = {old_game_data[0]['gm_age_max']} and gm_min_players = {old_game_data[0]['gm_min_players']} and \
                gm_max_players = {old_game_data[0]['gm_max_players']} and gm_max_players_orig = {old_game_data[0]['gm_max_players_orig']} and gm_date = '{data['game_date']}' and \
                gm_utc_datetime = '{game_date_time_utc}' and gm_unix_utc_datetime = {old_game_data[0]['gm_unix_utc_datetime']} and\
                gm_unix_utc_end_datetime = {old_game_data[0]['gm_unix_utc_end_datetime']} and gm_zip_code = '{old_game_data[0]['gm_zip_code']}' and gm_city_id = {old_game_data[0]['gm_city_id']} and \
                gm_country_id = {old_game_data[0]['gm_country_id']} and gm_loc_lat = '{old_game_data[0]['gm_loc_lat']}' and gm_loc_long = {old_game_data[0]['gm_loc_long']} and gm_loc_desc = '{old_game_data[0]['gm_loc_desc']}' and \
                gm_scope = '{old_game_data[0]['gm_scope']}' and gm_has_gallery = '{old_game_data[0]['gm_has_gallery']}' and gm_desc = '{old_game_data[0]['gm_desc']}' and gm_requirements = '{old_game_data[0]['gm_requirements']}' and gm_notes = '{old_game_data[0]['gm_notes']}' and gm_rules = '{old_game_data[0]['gm_rules']}' and\
                gm_kits = '{old_game_data[0]['gm_kits']}' and gm_is_free = '{old_game_data[0]['gm_is_free']}' and gm_payment_type = '{old_game_data[0]['gm_payment_type']}' and attend_type = '{old_game_data[0]['attend_type']}' and zoom_url = '{zoom_url}' and zoom_meeting_id = '{zoom_meeting_id}' and zoom_pwd = '{zoom_pwd}' and \
                gm_fees = {old_game_data[0]['gm_fees']} and gm_currency_symbol = '{old_game_data[0]['gm_currency_symbol']}' and gm_policy_id = {old_game_data[0]['gm_policy_id']} and gm_recurr_times = {old_game_data[0]['gm_recurr_times']} and \
                gm_recurr_type = '{old_game_data[0]['gm_recurr_type']}' and gm_copy_id = {old_game_data[0]['gm_copy_id']} and gm_copy_ques_from = {old_game_data[0]['gm_copy_ques_from']} and gm_renew_id = {old_game_data[0]['gm_renew_id']} and gm_showMem = {old_game_data[0]['gm_showMem']} and gm_reqQues = {old_game_data[0]['gm_reqQues']} and \
                gm_end_pause = {old_game_data[0]['gm_end_pause']} and gm_status = '{old_game_data[0]['gm_status']}' and gm_recurr_cancel_type = {old_game_data[0]['gm_recurr_cancel_type']} and\
                gm_pid = {old_game_data[0]['gm_pid']} and gm_recurr_days_times = '{old_game_data[0]['gm_recurr_days_times']}' and gm_time_zone = '{old_game_data[0]['gm_time_zone']}'")
        if not game_id:
            raise Exception("Insertion Error ")
        else:
            return response.success(result_data={"output": "true"})

    except Exception as e:
        return "something happened:" + e.__str__()


# ########### edit game
def edit_class(EditField):
    # parameter is array of EditField  ex: {"GmT":"%20nola1%20test"}
    # return json array of  {'Result': '{"result": "True", "data": {"GmID": 6, "GmT": "%2520nola1%2520test", "OrgID": 852, "OrgEmail": "ma9300179@gmail.com", "OrgName": "meroo moo", "OrgGdr": "f", "OrgBusiness": "", "STypeID": 464, "STypeName": "Fitness", "CourtID": 1, "CourtT": "Indoors", "LevelID": 8, "LevelT": "All levels", "ImgName": "05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg", "Gdr": "mf", "Age": "All ages", "MinPly": 1, "MaxPly": 3, "STime": "14:40:00", "ETime": 30, "timeZone": "Europe/London", "CountryID": 66, "CountryIso": "EG", "CountryName": "Egypt", "CityID": 0, "CityName": "", "Lat": "30.8760568", "Long": "29.742604", "LocDesc": "Alexandria%2520Governorate%252C%2520Egypt", "Scope": "Open to public", "HasGlly": "n", "Desc": "", "Req": "ReqReqReqReqReq", "Notes": "NoteNoteNoteNote", "Rules": "RulesRulesRules", "Kits": "KitsKitsKitsKits", "IsFree": "n", "attendType": "inPerson", "zoomUrl": "", "zoomMeetingId": "", "PlyBirthDate": "1993-4-4", "GmRecurrDaysTimes": "", "PayType": "Stripe", "showMem": "False", "CurrencyID": 61, "CurrencyName": "egp", "currency_symbol": "\\u00a3", "PolicyID": 1, "PolicyT": "Refund available (If replaced)", "RecurrID": 0, "IsStopRecurred": "", "gm_recurr_times": 0, "gm_recurr_type": "", "RenewID": 0, "ply_img": "de435fe61549b33e6f5069397c3116c9.jpeg", "s3_profile": 0, "gm_s3_status": "0", "GmOrgDate": "2021-05-17", "gm_img": "05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg", "Fees": 80.0, "UTCDateTime": "2021-05-17 13:40:00", "STypeImg": "gm_s_types/Fitness-class.png", "IsHis": "y", "ply_country_id": 235, "FeedStatus": "", "FeedPlyID": "", "GmDist": "", "zoomPwd": "", "OrgImg": "https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg", "OrgImgThumb": "https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg", "GmImg": "https://classfit-assets.s3.amazonaws.com/images/upload/gm/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg", "GmImgThumb": "https://classfit-assets.s3.amazonaws.com/images/upload/gm/thumb/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg", "GmDate": "2021-05-17", "SSTime": "01:40 PM", "Day": "Monday", "EETime": "02:10 PM", "orgOfflineStatus": "", "Days": "", "EndRecurr": "", "gm_time_zone": "(Utc+00:00)", "GmStatus": "", "ISRecurr": "False", "Parent": "False", "GmReqQues": "no", "GmReported": "", "Withdrawable": false, "OrgMem": false, "InvGm": false, "PlyStatus": "No", "IsPly": "n", "RequestedBefore": "n", "HasStopDays": "y", "NState": "on", "HaveReminder": "y", "RemindStat": "", "RemindPeriod": "", "GmQues": [], "PlyAnswers": [], "Wait": []}, "emaildata": "", "code": 200}', 'PaymentMethod': ''}
    try:
        # check if OrgId and PlayerID is not empty and type is int and >=0
        if EditField and type(EditField) is dict:
            if 'Tkn' in EditField and EditField['Tkn'] == "":
                raise Exception("invalid Token")
            if 'GmID' in EditField and int(EditField['GmID']) <= 0 and type(EditField['GmID'] != int):
                raise Exception("invalid GmID")
            if 'PlyID' in EditField and int(EditField['PlyID']) <= 0 and type(EditField['PlyID'] != int):
                raise Exception("invalid PlyID")
            if 'DevID' in EditField and EditField['DevID'] == "":
                raise Exception("invalid DevID")
            if 'ProjectKey' in EditField and EditField['ProjectKey'] == "":
                raise Exception("invalid ProjectKey")
            if 'ProjectSecret' in EditField and EditField['ProjectSecret'] == "":
                raise Exception("invalid ProjectSecret")

            EditChange = game_utils.validation_field_to_edit(EditField)
            if str(EditChange).__contains__("something happened:"):
                raise Exception(EditChange)
            if EditChange:
                data = {'GmID': EditField['GmID'], 'PlyID': EditField['PlyID'], 'tkn': EditField['Tkn'],
                        'dev_id': EditField['DevID'], 'ProjectKey': EditField['ProjectKey'],
                        'ProjectSecret': EditField['ProjectSecret']}
                oldData = view_game(data)
                if str(oldData).__contains__("something happened:"):
                    raise Exception(oldData)
                payMethodMessage = ''
                if oldData:
                    res_old_data = json.loads(oldData)
                    access_old_data = res_old_data["data"]
                    # write your query here to update field
                    SetID = 0
                    if 'modify' in EditField:
                        if EditField['modify'] and type(EditField['modify']) == str and access_old_data[
                            'ISRecurr'] == 'True' and int(access_old_data['RecurrID']) == 0:
                            SetID = EditField['GmID']
                        elif EditField['modify'] and type(EditField['modify']) == str and access_old_data[
                            'ISRecurr'] == 'True' and int(access_old_data['RecurrID']) > 0:
                            SetID = access_old_data['RecurrID']
                        else:
                            SetID = EditField['GmID']

                        if EditField['modify'] and type(EditField['modify']) == str and str(
                                EditField['modify']).lower() == "all":
                            # update = execution.execute(f"UPDATE game SET {EditChange} WHERE gm_id = {SetID} OR gm_recurr_id = {SetID} AND(gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP;")
                            update = execution.execute(
                                f"UPDATE game SET {EditChange} WHERE gm_id = {SetID} OR gm_recurr_id = {SetID};")
                        else:
                            update = execution.execute(
                                f"UPDATE game SET {EditChange} WHERE gm_id = {EditField['GmID']};")

                    else:
                        update = execution.execute(f"UPDATE game SET {EditChange} WHERE gm_id = {EditField['GmID']};")

                    if update:
                        raise Exception(update)
                    # check admin is connected to pay method or not
                    if 'PayType' in EditField and str(EditField['PayType']).lower() == 'stripe':
                        PlyMethods = game_utils.get_ply_verified_methods(EditField['PlyID'])
                        if PlyMethods['stripe'] != 'y':
                            payMethodMessage = 'Your class has been successfully edited however as you have opted for electronic payments, you will not be able to accept bookings until you have finished setting up a payment method.'

                    # update instructor data
                    if 'instructorId' in EditField and int(EditField['instructorId']) > 0:
                        modifyType = EditField['modify'] if 'modify' in EditField else ""
                        RecurrID_parentId_Data = game_utils.get_game_recur_id(int(EditField['GmID']))
                        if str(RecurrID_parentId_Data).__contains__("something happened:"):
                            raise Exception(RecurrID_parentId_Data)
                        if RecurrID_parentId_Data:
                            RecurrID = RecurrID_parentId_Data[0]['gm_recurr_id'] if 'gm_recurr_id' in \
                                                                                    RecurrID_parentId_Data[
                                                                                        0] else 0
                            handle = game_utils.handle_game_instructor(int(EditField['GmID']), RecurrID,
                                                                       int(EditField['instructorId']), modifyType)
                            if str(handle).__contains__("something happened:"):
                                raise Exception(handle)

                    # remove old gm_players if old game was onsite and new game is stripe
                    if 'PayType' in EditField and EditField['PayType'] and type(EditField['PayType']) == str and \
                            EditField['PayType'] == "stripe":
                        if 'modify' in EditField:
                            if EditField['modify'] == 'all':
                                gmPGsql = execution.execute(
                                    f"SELECT gm_id FROM game WHERE (gm_id = {EditField['GmID']} OR gm_recurr_id = {EditField['GmID']}) AND (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP")
                                if str(gmPGsql).__contains__("something happened:"):
                                    raise Exception(gmPGsql)
                                if gmPGsql:
                                    ids = []
                                    for id in gmPGsql:
                                        ids.append(id['gm_id'])

                                    sql = execution.execute(
                                        f"DELETE FROM gm_players WHERE gm_ply_gm_id IN {ids} AND gm_ply_status='r' AND gm_ply_refunded=0 ")
                                    if str(sql).__contains__("something happened:"):
                                        raise Exception(sql)
                        else:
                            sql = execution.execute(
                                f"DELETE FROM gm_players WHERE gm_ply_gm_id = {EditField['GmID']} AND gm_ply_status='r' AND gm_ply_refunded=0 ")
                            if str(sql).__contains__("something happened:"):
                                raise Exception(sql)

                    res_new_data = game_utils.get_new_data(EditField, access_old_data)
                    if str(res_new_data).__contains__("something happened:"):
                        raise Exception(res_new_data)

                    log = game_utils.log_edit_action(EditField, res_new_data, access_old_data)
                    if str(log).__contains__("something happened:"):
                        raise Exception(log)


                    if 'PayType' in EditField and EditField['PayType'] and type(EditField['PayType']) == str and \
                            EditField['PayType'] == "stripe":
                        if 'modify' in EditField and EditField['modify']:
                            if EditField['modify'] == 'all':
                                where_condition = "WHERE (gm_id = " + str(SetID) + "OR gm_recurr_id =" + str(SetID) + ""

                        else:
                            where_condition = "WHERE gm_id = " + str(EditField['GmID']) + ""


                        gm_res = execution.execute(f"""SELECT gm_id as class_id, gm_title AS class_title, gm_recurr_id as parent_id, gm_utc_datetime as UTCDateTime, gm_org_id as Org_id, gm_date AS class_date, gm_start_time AS class_time
                                                    FROM game {where_condition}
                                                    AND gm_payment_type != 'onsite'
                                                    AND(gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP""")
                        if str(gm_res).__contains__("something happened:"):
                            raise Exception(gm_res)

                        if gm_res:
                            params = {'classes': json.dumps(gm_res)}
                            BundleResponse = common_utils.bundle_curl('cron/recur_autoenroll', params)

                    return response.success(result_data=res_new_data, email_notifications=payMethodMessage)

            else:
                raise Exception("No field is change")
        else:
            raise Exception("invalid data")
    except Exception as e:
        return response.error(e.__str__())


# ################## pending player ############
def pending_player(pending_data):
    """
    parameters : pending data as project_id , player_email 
    description : pending player in a specific game using the player email
    """
    try:
        if not pending_data['player_email'] or pending_data['player_email'] is None or pending_data[
            'player_email'] == '' or type(pending_data['player_email']) != str:
            return Exception("invalid email")
        if not pending_data['ProjectKey'] or pending_data['ProjectKey'] is None or type(
                pending_data['ProjectKey']) != str:
            raise Exception("invalid project key")
        if not pending_data['ProjectSecret'] or pending_data['ProjectSecret'] is None or type(
                pending_data['ProjectSecret']) != str:
            raise Exception("invalid project secret")
        if not pending_data['ProjectKey'] or pending_data['ProjectKey'] is None or type(
                pending_data['ProjectKey']) != str:
            raise Exception("invalid project key")

        if not pending_data['ProjectSecret'] or pending_data['ProjectSecret'] is None or type(
                pending_data['ProjectSecret']) != str:
            raise Exception("invalid project secret")
        if not pending_data['tkn'] or pending_data['tkn'] is None or type(pending_data['tkn']) != str:
            raise Exception("invalid token")

        if not pending_data['dev_id'] or pending_data['dev_id'] is None or type(pending_data['dev_id']) != str:
            raise Exception("invalid device id")
        if not pending_data['project_id'] or pending_data['project_id'] is None or type(
                pending_data['project_id']) != int:
            raise Exception("invalid project id")

        pending_player_data_sql = execution.execute(
            f"SELECT * FROM pendinreg_players \
                LEFT JOIN players ON LOWER(pend_ply_to_email)=LOWER('{pending_data['player_email']}') \
                WHERE LOWER(pend_ply_to_email) =LOWER('{pending_data['player_email']}') \
                AND ply_pid = {pending_data['project_id']} AND pend_pid = {pending_data['project_id']} limit 5")
        if pending_player_data_sql:
            for pend_player_data in pending_player_data_sql:

                # check that he is in the same project

                player_data_sql = execution.execute(
                    f"SELECT ply_id FROM players WHERE ply_id= {pend_player_data['pend_ply_frm_id']} \
                    AND ply_pid= {pending_data['project_id']}"
                )

                if not pend_player_data['ply_id'] and pend_player_data['ply_id'] < 0 and player_data_sql[0]:
                    raise Exception(response.error(message=pend_player_data['ply_id']))
                if pend_player_data['pend_gm_id']:
                    # check if game exists and upcoming game or not
                    check_game = execution.execute(f"SELECT * from game where gm_id = {pend_player_data['pend_gm_id']}")
                    if check_game:
                        # data = {'GmID': pending_data['game_id'], 'PlyID': pending_data['player_id'], 'tkn': pending_data['tkn'],
                        #     'dev_id': pending_data['dev_id'], 'ProjectKey': pending_data['ProjectKey'],
                        #     'ProjectSecret': pending_data['ProjectSecret']}

                        # game_data = game_utils.get_game_player_data(game_id=int(data["GmID"]), player_id=int(data["PlyID"]), tkn=data['tkn'],
                        #                             dev_id=data['dev_id'], ProjectKey=data['ProjectKey'],
                        #                             ProjectSecret=data['ProjectSecret'])
                        game_data = game_utils.get_game_player_data(pend_player_data['pend_gm_id'],
                                                                    pend_player_data['ply_id'],
                                                                    pending_data["ProjectKey"],
                                                                    pending_data["ProjectSecret"], pending_data["tkn"],
                                                                    pending_data["dev_id"])
                        # view_game(data)
                        if str(game_data).__contains__("something happened:"):
                            raise Exception(game_data)

                        if game_data['Scope'] == 'Open to public':
                            # check if player is invited before
                            check_invitation_frnd = execution.execute(
                                f"SELECT * FROM invitations WHERE inv_gm_id = {pend_player_data['pend_gm_id']} \
                                AND inv_ply_to_id = {pend_player_data['ply_id']} AND (inv_approve = 'y' || inv_approve = 'p')")

                            # check if player member in this game
                            check_member_game = execution.execute(
                                f"SELECT * FROM gm_players WHERE gm_ply_gm_id = {pend_player_data['pend_gm_id']}  \
                                AND gm_ply_status = 'y' \
                                AND (gm_ply_leave IS NULL OR gm_ply_leave = '')\
                                AND gm_ply_ply_id = {pend_player_data['ply_id']} ")
                            # check if player waitlist in this game
                            check_if_waitlist = execution.execute(
                                f"SELECT gm_wait_list_id FROM gm_waitlist \
                                WHERE gm_wait_list_gm_id={pend_player_data['pend_gm_id']}  \
                                AND gm_wait_list_ply_id={pend_player_data['ply_id']}\
                                AND gm_wait_list_withdrew = 0 \
                                AND gm_wait_list_removed_by_admin = 0")

                            if check_member_game is []:
                                check_member_game = False
                            if check_invitation_frnd is []:
                                check_invitation_frnd = False
                            if check_if_waitlist is []:
                                check_if_waitlist = False
                            # print('hhh')
                            notify_array = {}
                            notify_array['Type'] = 'InvFriToGm'
                            notify_array['Mess'] = str(game_data['OrgName']) + " has invited you to join " + str(
                                game_data['GmT']) + ' on ' + str(datetime.strptime(game_data["GmDate"], '%Y-%m-%d'))
                            notify_array['Data'] = {"Gm": game_data}

                            if check_invitation_frnd is False and check_member_game is False and check_if_waitlist is False:
                                # insert new invitation to this member for these classes
                                execution.execute(
                                    f"INSERT INTO invitations (inv_gm_id, inv_ply_frm_id, inv_ply_to_id, inv_approve) "
                                    f"VALUES({pend_player_data['pend_gm_id']}, {pend_player_data['pend_ply_frm_id']}, {pend_player_data['ply_id']}, 'y')")
                                # log this invitation
                                execution.execute(f"INSERT INTO invitations_log (inv_log_gm_id, inv_log_ply_id) "
                                                  f"VALUES({pend_player_data['pend_gm_id']},{pend_player_data['ply_id']})")

                                # notification_check_player = notification_utils.checking_notification_for_player(int(pending_data['project_id']),int(pend_player_data["GmID"]), int(pend_player_data["PlyID"]))
                                # if type(notification_check_player) == str:
                                #     raise Exception(response.error(message=notification_check_player))

                                # comment for now
                                # notification_utils.checking_notification_for_player(pending_data['project_id']  ,pend_player_data['pend_gm_id'] ,pend_player_data['ply_id'],notify_array['Type'], notify_array['Mess'],notify_array['Data'],
                                # pending_data['ProjectKey'] ,pending_data['ProjectSecret'],pending_data['tkn'] ,pending_data['dev_id'])

                                # send mail to invite player as friend

                            # delete pending invitation
                            execution.execute(
                                f"DELETE FROM pendinreg_players WHERE pend_ply_frm_id = {pend_player_data['pend_ply_frm_id']} \
                                AND pend_ply_to_email = {pending_data['player_email']} AND pend_gm_id = {pend_player_data['pend_gm_id']}")

                    check_frnd_req = game_utils.check_friennd_req(pend_player_data['pend_ply_frm_id'],
                                                                  pend_player_data['ply_id'], accept='p')
                    # print("d5lt mn hna")

                    if check_frnd_req == 0:

                        # invite to be friend
                        execution.execute(
                            f"INSERT INTO invitations (inv_gm_id , inv_ply_frm_id, inv_ply_to_id, inv_accept) "
                            f"VALUES({pend_player_data['pend_gm_id']} ,{pend_player_data['pend_ply_frm_id']}, {pend_player_data['ply_id']}, 'p')")

                        ply_data = execution.execute(
                            f"SELECT ply_email_sett,ply_brithdate_sett,ply_city_sett from players \
                            where ply_id = {pend_player_data['pend_ply_frm_id']} AND ply_pid= {pending_data['project_id']} ")
                        if str(ply_data).__contains__('Something went wrong'):
                            raise Exception(ply_data)
                        if not ply_data or 'ply_email_sett' not in ply_data[0] or 'ply_brithdate_sett' not in ply_data[
                            0] or 'ply_city_sett' not in ply_data[0]:
                            raise Exception('invalid player data')

                        # # send mail to invite player as friend
                        # data_for_notification = {pending_data['project_id']  ,pend_player_data['pend_gm_id'] ,pend_player_data['ply_id'],
                        # notify_array['Type'], notify_array['Mess'],notify_array['Data'],
                        # pending_data['ProjectKey'] ,pending_data['ProjectSecret'],pending_data['tkn'] ,pending_data['dev_id']}
                        # print("ooo")
                        # notification_utils.checking_notification_for_player(pending_data)
                        #     # pending_data['project_id']  ,pend_player_data['pend_gm_id'] ,pend_player_data['ply_id'],notify_array['Type'], notify_array['Mess'],notify_array['Data'], 
                        # # pending_data['ProjectKey'] ,pending_data['ProjectSecret'],pending_data['tkn'] ,pending_data['dev_id'])

                        notification_utils.checking_notification_for_player(pending_data['project_id'],
                                                                            pend_player_data['pend_gm_id'],
                                                                            pend_player_data['ply_id'],
                                                                            notify_array['Type'], notify_array['Mess'],
                                                                            notify_array['Data'],
                                                                            pending_data['ProjectKey'],
                                                                            pending_data['ProjectSecret'],
                                                                            pending_data['tkn'], pending_data['dev_id'])
                        # return True

            # return response.success(result_data={"output": "true"})

        # return True
        return response.success(result_data={"output": "true"})
    except Exception as e:
        return e


#  ##### cron wait list part ####
def cron_waitlist(data):
    # parameter ex:{'project_id':1}
    # get classes ids and check if array not empty
    # get the classes data  and check if not empty or not array
    # inform wait list
    # return True or False
    try:
        if data and type(data) is dict:
            if 'project_id' in data and data['project_id'] == "":
                raise Exception("invalid project_id")

            project_id = data['project_id'] if 'project_id' in data else 0
            if project_id and type(project_id) == int and int(project_id) > 0:
                Classes_ids = game_utils.getClassIds(project_id)
                if str(Classes_ids).__contains__("something happened:"):
                    raise Exception(Classes_ids)
                if Classes_ids and type(Classes_ids) == list:
                    sql_list = []
                    for cLassId in Classes_ids:
                        sql_list.append(cLassId['gm_id'])
                    SqlArray = str(tuple([key for key in sql_list])).replace(',)', ')')
                    Classes_data = game_utils.getClassData(SqlArray)
                    if str(Classes_data).__contains__("something happened:"):
                        raise Exception(Classes_data)
                    if Classes_data and type(Classes_data) == list:
                        inform_wait_list = game_utils.informWaitlist(Classes_data, SqlArray)
                        if str(inform_wait_list).__contains__("something happened:"):
                            raise Exception(inform_wait_list)
                        return response.success(result_data=inform_wait_list)

                    else:
                        raise Exception("listdata is empty")
                else:
                    raise Exception("list is empty")
            else:
                raise Exception("invalid project_id")
        else:
            raise Exception("project_id is required")
    except Exception as e:
        return response.error(e.__str__())


def notifications(gm_id=0, ply_id=0, period=0, period_type='h', remindstate=1):
    try:
        if gm_id and gm_id > 0 and ply_id and ply_id > 0 and period and period_type and remindstate:
            gm_data = execution.execute(
                f"SELECT gm_status,gm_recurr_id,gm_recurr_times,gm_is_stop_recurred FROM game WHERE gm_id={gm_id} AND (gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP")
            if gm_data and gm_data != []:
                if gm_data[0]['gm_status'] == 'cancel':
                    return Exception(response.error(code='115', message="Game Canceled"))
                else:
                    if period_type == 'd':
                        period = period * 24
                    elif period_type == 'w':
                        period = period * 24 * 7
                    elif period_type == 'm':
                        period = period * 24 * 30
                    gm_ids = [{'gm_id': gm_id}]
                    # child class
                    if ((gm_data[0]['gm_recurr_id'] != 0 and gm_data[0]['gm_recurr_times'] == 0) and gm_data[0][
                        'gm_is_stop_recurred'] == 'n'):
                        gm_ids = execution.execute(
                            f"SELECT gm_id FROM game WHERE (gm_recurr_id={gm_data[0]['gm_recurr_id']} and (gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP")
                    # parent class
                    elif (gm_data[0]['gm_recurr_id'] == 0 and gm_data[0]['gm_recurr_times'] == 1 and gm_data[0][
                        'gm_is_stop_recurred'] == 'n'):
                        gm_ids = execution.execute(
                            f"SELECT gm_id FROM game WHERE (gm_recurr_id={gm_id} and (gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP")
                    ids = []
                    updated = []
                    for i in range(len(gm_ids)):
                        ids.append(gm_ids[i]['gm_id'])
                    if len(ids) > 1:
                        where = f'and custom_notification_gm_id IN {tuple(ids)}'
                    else:
                        where = f'and custom_notification_gm_id = {gm_id}'
                    notification_id = execution.execute(
                        f"SELECT custom_notification_gm_id FROM custom_notifications WHERE custom_notification_ply_id={ply_id} {where} ;")
                    notified_ids = []
                    for i in range(len(notification_id)):
                        notified_ids.append(notification_id[i]['custom_notification_gm_id'])
                    if len(ids) > 1:
                        for key in ids:
                            if key in tuple(notified_ids):
                                updated.append(key)
                            else:
                                execution.execute(
                                    f"INSERT INTO custom_notifications(custom_notification_ply_id,custom_notification_period,custom_notification_gm_id) VALUES ({ply_id},{period},{key})")
                        if len(updated) > 0:
                            execution.execute(
                                f"UPDATE custom_notifications SET custom_notification_period={period},custom_notification_updated=NOW() WHERE custom_notification_ply_id={ply_id} AND custom_notification_gm_id IN {tuple(updated)}")
                    elif len(ids) == 1:
                        if notification_id is []:
                            execution.execute(
                                f"INSERT INTO custom_notifications(custom_notification_ply_id,custom_notification_period,custom_notification_gm_id , custom_notification_reminder_status) VALUES ({ply_id},{period},{gm_id},{remindstate})")
                        else:
                            execution.execute(
                                f"UPDATE custom_notifications SET custom_notification_period={period},custom_notification_reminder_status={remindstate},custom_notification_updated=NOW() WHERE custom_notification_gm_id={gm_id} AND custom_notification_ply_id={ply_id}")
            else:
                return Exception(response.error(code='631', message="Game Not Found In Upcoming Games"))
        else:
            raise Exception("Data is required")

    except Exception as e:
        return e


def handleRefundPolicyMsg(data):
    try:
        policyTitle = ""
        if data and type(data) is dict:
            if 'IsFree' in data and data['IsFree'] == "" or not isinstance(data['IsFree'], str):
                raise Exception("invalid input")
            if 'PayType' in data and data['PayType'] == "" or not isinstance(data['PayType'], str):
                raise Exception("invalid PayType")
            if 'PolicyT' in data and data['PolicyT'] == "" or not isinstance(data['PolicyT'], str):
                raise Exception("invalid Policy Title")
            if 'Symbol' in data and data['Symbol'] == "" or not isinstance(data['Symbol'], str):
                raise Exception("invalid Symbol")
            try:
                if 'PolicyID' in data and int(data['PolicyID']) <= 0:  # or type(data['PolicyID'] != int)) :
                    raise Exception("invalid Policy ID")
                if 'GmPlys' in data and int(data['GmPlys']) < 0:  # or type(data['GmPlys'] != int)):
                    raise Exception("invalid GmPlys")
                if 'MaxPly' in data and int(data['MaxPly']) < 0:  # or type(data['MaxPly'] != int)):
                    raise Exception("invalid MaxPly")
                if 'Fees' in data and int(data['Fees']) <= 0:  # or type(data['Fees'] != int)):
                    raise Exception("invalid Fees")
            except Exception:
                raise Exception("Error in input")
            UTC = datetime.strptime(data['UTCDateTime'], '%Y-%m-%d %H:%M:%S')
            hourdiff = (datetime.now() - UTC).total_seconds() / 3600

            if (data['IsFree'] == "y" or data['PayType'] == "onsite"):
                policyTitle = "Full refund"
                return response.success(
                    result_data={"policyMsg": "We are sorry you could not make it!", "policyTitle": policyTitle})

            def P1(data):
                if int(data['GmPlys']) < int(data['MaxPly']):
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or credit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = "Refund if replaced"
                    policyMsg = "This class operates a 'refund if replaced' policy. <br> if your place is filled, you will be given a full refund"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P2(data):
                policyTitle = "No refund"
                policyMsg = "This class operates a 'no refund policy'"
                return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P3(data):
                policyTitle = "50% refund"
                policyMsg = "You are due a partial refund of " + data[
                    'Symbol'] + " %s <br /> This will be credited back in 3-5 business days" % data['Fees']
                return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P5(data):
                if hourdiff > 24:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside of the [24 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P6(data):
                if hourdiff > 1:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside )of the [1 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P7(data):
                if hourdiff > 3:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside of the [3 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P8(data):
                if hourdiff > 6:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside of the [6 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P9(data):
                if hourdiff > 12:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside of the [12 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def P10(data):
                if hourdiff > 48:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "Unfortunately you have withdrawn outside of the [48 hour] cancellation period so no refund is due"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}
                else:
                    policyTitle = str(data['PolicyT'])
                    policyMsg = "You will be refunded in the same way you payed for the class i.e. via Stripe or crdeit <br /> this will be credited back within 3-5 business days"
                    return {"policyMsg": policyMsg, "policyTitle": policyTitle}

            def default(data):
                raise Exception("Incorrect Policy input")

            pid = int(data['PolicyID'])

            def switch(pid):
                switcher = {
                    1: P1,
                    2: P2,
                    3: P3,
                    5: P5,
                    6: P6,
                    7: P7,
                    8: P8,
                    9: P9,
                    10: P10
                }
                return switcher.get(pid, default)(data)

            res = switch(pid)
            return response.success(result_data=res)
        else:
            raise Exception("Error in input")

    except Exception as e:
        return response.error(e.__str__())


'''def SetMemcachedData():
    try:
        if memcache.get("Memcached"):
            # initialaize Memcache
            if(get server list is empty):
                client = memcache.Client([('localhost',11211)])
                CountryData = execution.execute(
                    "SELECT country_id,country_name,iso FROM countryview")
                CityData = execution.execute(
                    "SELECT DISTINCT city_id,city_name,city_code FROM cityview ORDER BY city_name DESC"
                )
                GmSTypes = execution.execute(
                    "SELECT gm_s_type_id AS GmSTypeID, gm_s_type_name AS GmSTypeName FROM gm_s_typesview"
                )
                setData = []
                for item in CountryData:
                    setD = {'CountryData':None}
                    setD['CountryData']= item
                    setData.append(setD)
                for item in CityData:
                    setD = {'CityData':None}
                    setD['CityData']= item
                    setData.append(setD)
                for item in GmSTypes:
                    setD = {'GmSTypes':None}
                    setD['GmSTypes']= item
                    setData.append(setD)
                client.set('CachedData',setData)
                cacheTest = client.get('CachedData')
                if cacheTest:
                    resArr = "True",

                    return json.dumps(resArr, default=str)
                else:
                    resArr = client.get('CachedData')

                    raise Exception (json.dumps(resArr, default=str))

            else:
                resArr = "Data set before"

                raise Exception (json.dumps(resArr, default=str))
        else:
            resArr = "Memcached not set"

            raise Exception (json.dumps(resArr, default=str))

    except Exception as e:
        return response.error(e.__str__())
'''


# implementation of social#
def social(player_arr):
    try:
        if not player_arr['project_id'] or player_arr['project_id'] is None or type(
                player_arr['project_id']) != str:
            raise Exception("invalid project id")

        if not player_arr['ProjectKey'] or player_arr['ProjectKey'] is None or type(
                player_arr['ProjectKey']) != str:
            raise Exception("invalid project key")

        if not player_arr['ProjectSecret'] or player_arr['ProjectSecret'] is None or type(
                player_arr['ProjectSecret']) != str:
            raise Exception("invalid project secret")

        if not player_arr['tkn'] or player_arr['tkn'] is None or type(player_arr['tkn']) != str:
            raise Exception("invalid token")

        if not player_arr['dev_id'] or player_arr['dev_id'] is None or type(player_arr['dev_id']) != str:
            raise Exception("invalid device id")

        if not player_arr['source'] or player_arr['source'] is None or type(player_arr['source']) != str:
            raise Exception("invalid source")

        if not ('Email' in player_arr) or not player_arr['Email'] or player_arr['Email'] is None or player_arr[
            'Email'] == '' or type(player_arr['Email']) != str:
            raise Exception("invalid Email")
        if not ('GcmReg' in player_arr):
            player_arr['GcmReg'] = ''
        if not ('Gdr' in player_arr):
            player_arr['Gdr'] = ''
        if not ('CtyID' in player_arr):
            player_arr['CtyID'] = '0'
        if not ('CountryID' in player_arr):
            player_arr['CountryID'] = '0'
        if not ('FName' in player_arr) or not player_arr['FName'] or player_arr['FName'] is None or player_arr[
            'FName'] == '' or type(player_arr['FName']) != str \
                or not ('LName' in player_arr) or not player_arr['LName'] or player_arr['LName'] is None or player_arr[
            'LName'] == '' or type(player_arr['LName']) != str:
            raise Exception("Error Empty First Name Or Last Name")
        check_email = player_utils.check_mail(player_arr['Email'], player_arr['project_id'])
        if type(check_email) == str:
            raise Exception('Error in database at check mail')
        elif check_email > 0:
            check_suspended = player_utils.check_suspended_mail(player_arr['Email'], player_arr['project_id'])
            if type(check_suspended) == str:
                raise Exception('Error in database at check suspended mail')
            elif player_utils.check_suspended_mail(player_arr['Email'], player_arr['project_id']) > 0:
                raise Exception('Suspended Email')
            output = execution.execute(
                f"UPDATE players SET ply_status ='' WHERE ply_email = '{player_arr['Email']}' AND ply_pid='{player_arr['project_id']}'")
            if output:
                raise Exception(output)
            PlayerRow = execution.execute(
                f"SELECT * FROM players WHERE ply_email = '{player_arr['Email']}' AND ply_status = '' AND ply_pid='{player_arr['project_id']}'")
            if str(PlayerRow).__contains__('Something went wrong'):
                raise Exception(PlayerRow)
            if player_arr['source'] == 'Web' or player_arr['source'] == 'Android' or player_arr['source'] == 'IOS':
                source = str(player_arr['source'])[0]
                token = player_utils.add_player_token(player_id=PlayerRow[0]["ply_id"], dev_id=player_arr['dev_id'],
                                                      gcm_reg=player_arr['GcmReg'], source=source)
            else:
                token = player_utils.add_player_token(player_id=PlayerRow[0]["ply_id"], dev_id=player_arr['dev_id'])
            update_attributes = "ply_fname = " + "'" + str(
                urllib.parse.quote(player_arr['FName'])) + "'" + ",ply_lname = " + "'" + str(
                urllib.parse.quote(player_arr['LName'])) + "'"
            if 'Gdr' in player_arr:
                update_attributes = update_attributes + ",ply_gender = " + "'" + str(player_arr['Gdr']) + "'"
            if 'CtyID' in player_arr:
                update_attributes = update_attributes + ",ply_city_id = " + "'" + str(player_arr['CtyID']) + "'"
            if 'CountryID' in player_arr:
                update_attributes = update_attributes + ",ply_country_id = " + "'" + str(player_arr['CountryID']) + "'"
            output = execution.execute(
                f"UPDATE players SET {update_attributes} WHERE ply_id = '{PlayerRow[0]['ply_id']}'")
            if output:
                raise Exception(output)
            player_utils.player_rem_Qcode(PlayerRow[0]['ply_id'])
            ply_array = player_utils.player_view(PlayerRow[0]['ply_id'], token, player_arr['dev_id'])

            if 'TimeZone' in player_arr and player_arr['TimeZone'] and player_arr['TimeZone'] != '' and ply_array[0][
                'PlyTimeZone'] == '':
                player_utils.saveTimeZone(PlayerRow['ply_id'], player_arr['TimeZone'])
            if player_arr['source'] == 'IOS':
                return json.dumps({'result': "True", "PArr": ply_array})
            else:
                if ply_array['LastGms']:
                    ply_array['LastGms'][0]['GmDate'] = ply_array['LastGms'][0]['GmDate'].__str__()
                    ply_array['LastGms'][0]['GDate'] = ply_array['LastGms'][0]['GDate'].__str__()
                    ply_array['LastGms'][0]['STime'] = ply_array['LastGms'][0]['STime'].__str__()
                if ply_array['PlyCreatedAt']:
                    ply_array['PlyCreatedAt'] = ply_array['PlyCreatedAt'].__str__()
                return json.dumps({'result': ply_array})
        else:
            social_Img = ''
            if 'PlyImg' in player_arr and player_arr['PlyImg'] is not None and 'addimg' in player_arr and player_arr[
                'addimg']:
                img_name = str(binascii.hexlify(os.urandom(16))) + '.png'
                responses = urlopen(player_arr['PlyImg'])
                image = base64.b64encode(responses.read())
                params = {"imgName": img_name, "Secret": "", 'image': image,
                          'oldimg': '', 'Type': 'setplyimg'}
                curl_result = common_utils.internal_curl("https://classfit-assets.s3.amazonaws.com/backup/index.php",
                                                         params)
                if curl_result['Result'] == 'true':
                    social_Img = curl_result['ImageName']
                    PlyImg = social_Img
                else:
                    raise Exception('curl failed')
            if social_Img == '':
                if player_arr['Gdr'] == 'm':
                    PlyImg = 'male-user.jpg'
                elif player_arr['Gdr'] == 'f':
                    PlyImg = 'female-user.jpg'
                else:
                    PlyImg = 'ply.png'
            output = execution.execute(
                f"INSERT INTO players(ply_fname , ply_lname , ply_email , ply_password , ply_height , ply_h_unit , ply_weight , ply_w_unit, ply_country_id, ply_city_id,ply_img,ply_status,ply_pid) VALUES ('{player_arr['FName']}', '{player_arr['LName']}', '{player_arr['Email']}', '','0', '', '0', '', '{player_arr['CountryID']}', '{player_arr['CtyID']}', '{PlyImg}', '', '{player_arr['project_id']}')")
            if output:
                raise Exception('error into insertion to players')
            ply_id = execution.execute(
                f"SELECT ply_id from players where ply_fname='{player_arr['FName']}' and ply_lname='{player_arr['LName']}' and ply_email='{player_arr['Email']}'")
            if str(ply_id).__contains__('Something went wrong'):
                raise Exception('Error in selection of player id')
            output = execution.execute(
                f"INSERT INTO notifications (notifications_ply_id,notifications_state,notifications_game_stop)VALUES ('{ply_id[0]['ply_id']}',1,'')")
            if output:
                raise Exception(output)
            if ply_id[0]['ply_id'] > 0:
                token = ''
                if player_arr['source'] == 'Web' or player_arr['source'] == 'Android' or player_arr['source'] == 'IOS':
                    source = str(player_arr['source'])[0]
                    token = player_utils.add_player_token(player_id=ply_id[0]['ply_id'], dev_id=player_arr['dev_id'],
                                                          gcm_reg=player_arr['GcmReg'], source=source)
                admin_controller.up_inv_contacts(
                    {'first_name': player_arr['FName'], 'last_name': player_arr['LName'], 'email': player_arr['Email'],
                     'ply_id': ply_id[0]['ply_id'], 'project_id': player_arr['project_id']})

                admin_controller.guest_After_Reg_Updates(Ply_ID=ply_id[0]['ply_id'], Ply_Email=player_arr['Email'],
                                                         Ply_FName=player_arr['FName'], Ply_LName=player_arr['LName'])
                ply_array = player_utils.player_view(ply_id[0]['ply_id'], token, player_arr['dev_id'])
                pending_player({'player_email': player_arr['Email'], "ProjectKey": player_arr['ProjectKey'],
                                'ProjectSecret': player_arr['ProjectSecret'], 'tkn': token,
                                'dev_id': player_arr['dev_id'], 'project_id': player_arr['project_id']})
                if ply_array['PlyBDate']:
                    ply_array['PlyBDate'] = ply_array['PlyBDate'].__str__()
                if ply_array['LastGms']:
                    ply_array['LastGms'][0]['GmDate'] = ply_array['LastGms'][0]['GmDate'].__str__()
                    ply_array['LastGms'][0]['GDate'] = ply_array['LastGms'][0]['GDate'].__str__()
                    ply_array['LastGms'][0]['STime'] = ply_array['LastGms'][0]['STime'].__str__()
                if ply_array['PlyCreatedAt']:
                    ply_array['PlyCreatedAt'] = ply_array['PlyCreatedAt'].__str__()
                return json.dumps({'result': "True", "PArr": ply_array})

    except Exception as e:
        return response.error(e.__str__())


def getLastClassesAttendedWithOrganizer(data):
    patch = 1
    if 'organizerId' in data and type(data['organizerId']) == int and data['organizerId'] >= 0:

        if 'patch' in data and type(data['patch']) == int and data['patch'] >= 0:
            patch = data['patch']

        patch_classes = 50
        offset = (patch - 1) * patch_classes

        if 'playerId' in data and type(data['playerId']) == int and data['playerId'] >= 0:
            player_classes = player_utils.getPlyLastClassesAttendedWithOrganizer(data['organizerId'], data['playerId'],
                                                                                 patch_classes, offset)
            if player_classes and len(player_classes) > 0:
                return response.success(result_data=player_classes)

        if 'contactId' in data and type(data['contactId']) == int and data['contactId'] >= 0:
            contact_classes = player_utils.getContactLastClassesAttendedWithOrganizer(data['organizerId'],
                                                                                      data['contactId'], patch_classes,
                                                                                      offset)
            if contact_classes and len(contact_classes) > 0:
                return response.success(result_data=contact_classes)

    return response.success(result_data=[])


def ViewGmsCal(data):
    try:
        valid = validation_utils.ViewGmsCalValidation(data=data)
        if valid['status'] == "ok":
            pid = data['pid']
            PlyId = int(data['PlyId'])
            GmDate = str(data['GmDate'])
            aid = int(data['aid'])
            daygroup = int(data['daygroup'])
            # m = valid['m']
            date = int(valid['date'])
            gm = int(valid['gm'])
            limit_start = int(valid['limit_start'])
            Number = int(valid['Number'])
            a = int(valid['a'])
            Lat = 0
            Long = 0
            try:
                if ('Lat' in data and int(data['Lat'])) >= 0 and ('Long' in data and int(data['Long'])) >= 0:
                    sql = 1
                    Lat = data['Lat']
                    Long = data['Long']
                else:
                    sql = 2
            except:
                sql = 2
            timeZone = execution.execute(f"SELECT id,timezone FROM ply_timezone WHERE player_id={PlyId}")
            plyTimeZone = " "
            Date = " "
            if len(timeZone) > 0:
                plyTimeZone = "UTC"
            if date == 2:
                Month = data['Month']
                Year = data['Year']
                Date = str(Year) + "-" + str(Month) + "-%"
            elif (gm == 1):
                Date = GmDate
            if sql == 1:
                query = execution.execute(f"SELECT gm_recurr_id as RecurrID,gm_id , gm_title , gm_org_id , ply_fname , ply_lname , ply_gender , ply_img , gm_display_org , gm_s_type_id , gm_s_type_name,\
                                            gm_s_type_img , court_id , court_title , level_id , level_title , gm_img , gm_gender , gm_age , gm_min_players , gm_max_players ,\
                                            gm_status , gm_date , gm_start_time , gm_end_time , gm_utc_datetime , gm_end_pause , gm_city_id , city_name , gm_loc_lat , gm_loc_long,\
                                            gm_loc_desc , gm_scope , gm_has_gallery , gm_desc , gm_fees , gm_currency_symbol , currency_symbol , currency_id , gm_ages_text ,\
                                            gm_requirements , gm_notes , gm_rules , gm_kits , gm_showMem , gm_is_free , gm_payment_type , gm_policy_id , policy_title , attend_type , zoom_url,\
                                            (CASE WHEN ((gm_utc_datetime + INTERVAL gm_end_time MINUTE) > CURRENT_TIMESTAMP) THEN 'n' ELSE 'y' END)AS IsHis,\
                                            gm_reqQues , gm_status , gm_recurr_id , gm_is_stop_recurred , gm_recurr_times , gm_recurr_type , gm_renew_id , country_id,iso,country_name,\
                                            (((acos(sin(({Lat}*pi()/180)) * sin((gm_loc_lat*pi()/180)) + cos(({Lat}*pi()/180)) * cos((gm_loc_lat*pi()/180)) * cos((({Long}- gm_loc_long)* pi()/180))))*180/pi())*60*1.609344) as GmDist \
                        FROM gm_players \
                            LEFT JOIN game ON  gm_id=gm_ply_gm_id \
                            LEFT JOIN players ON  gm_org_id = ply_id \
                            LEFT JOIN gm_s_types ON  gm_sub_type_id = gm_s_type_id \
                            LEFT JOIN court ON gm_court_id = court_id \
                            LEFT JOIN level ON  gm_level_id = level_id \
                            LEFT JOIN country ON gm_country_id = country_id \
                            LEFT JOIN city ON gm_city_id = city_id \
                            LEFT JOIN policy ON gm_policy_id = policy_id \
                            LEFT JOIN currencies ON currency_id=gm_currency_symbol \
                            LEFT JOIN gm_ages ON gm_ages_id=gm_age \
                            LEFT JOIN ply_bans on (ply_ban_ply_frm=gm_org_id and ply_ban_ply_to={PlyId})or(ply_ban_ply_frm={PlyId} and ply_ban_ply_to=gm_org_id) \
                        WHERE \
                            ply_ban_id IS NULL AND \
                            gm_ply_ply_id = {PlyId} \
                            AND gm_ply_gm_id > 0 AND gm_status IS NULL \
                            AND gm_pid={pid} \
                            AND gm_ply_status = 'y' \
                            AND (CASE \
                            WHEN attend_type = 'zoom' THEN  DATE(CONVERT_TZ(gm_utc_datetime, 'UTC', '{plyTimeZone}')) LIKE '{Date}' \
                            WHEN attend_type != 'zoom' THEN gm_date LIKE '{Date}' \
                            END) \
                            ORDER BY gm_date DESC,gm_start_time DESC ,(CASE WHEN {Lat} IS NOT NULL AND {Long} IS NOT NULL THEN GmDist END ) \
                            LIMIT {limit_start},{Number}")

            else:
                query = execution.execute(f"SELECT gm_recurr_id as RecurrID,gm_id , gm_title , gm_org_id , ply_fname , ply_lname , ply_gender , ply_img , gm_display_org , gm_s_type_id , gm_s_type_name,\
                                  gm_s_type_img , court_id , court_title , level_id , level_title , gm_img , gm_gender , gm_age , gm_min_players , gm_max_players ,\
                                  gm_status , gm_date , gm_start_time , gm_end_time , gm_utc_datetime , gm_end_pause , gm_city_id , city_name , gm_loc_lat , gm_loc_long,\
                                  gm_loc_desc , gm_scope , gm_has_gallery , gm_desc , gm_fees , gm_currency_symbol , currency_symbol , currency_id , gm_ages_text ,\
                                  gm_requirements , gm_notes , gm_rules , gm_kits , gm_showMem , gm_is_free , gm_payment_type , gm_policy_id , policy_title , attend_type , zoom_url,\
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
                                LEFT JOIN gm_ages ON gm_ages_id=gm_age\
                                LEFT JOIN ply_bans on (ply_ban_ply_frm=gm_org_id and ply_ban_ply_to={PlyId})or(ply_ban_ply_frm={PlyId} and ply_ban_ply_to=gm_org_id)\
                         WHERE\
                         ply_ban_id IS NULL AND\
                         gm_ply_ply_id = {PlyId}\
                         AND gm_ply_gm_id > 0 AND gm_status IS NULL\
                         AND gm_pid={pid}\
                         AND gm_ply_status = 'y'\
                         AND (CASE\
                             WHEN attend_type = 'zoom' THEN  DATE(CONVERT_TZ(gm_utc_datetime, 'UTC', '{plyTimeZone}')) LIKE '{Date}'\
                             WHEN attend_type != 'zoom' THEN gm_date LIKE '{Date}'\
                         END)\
                         ORDER BY gm_date DESC,gm_start_time DESC\
                         LIMIT {limit_start},{Number}")

            if str(query).__contains__("Something went wrong"):
                raise Exception(str(query))
            GmData = [{}]
            gmcnt = 0
            if a == 1 and len(query) > 0:
                for row in range(len(query)):
                    if (int(aid) == int(query[row]['gm_org_id'])):
                        GmData[gmcnt] = query[row]
                        gmcnt += 1
                if gmcnt == 0:
                    raise Exception("Admin not found")
            elif len(query) <= 0:
                raise Exception("The query did not return values")
            else:
                for row in range(len(query)):
                    GmData[gmcnt] = (query[row])
                    gmcnt += 1

            resArr = [{}]
            if date == 2:
                GamesArray = []
                GmDatee = ''
                if (gmcnt > 0):
                    for row in range(len(GmData)):
                        if plyTimeZone != "" and str(GmData[row]['attend_type']) == 'zoom':
                            localDateTime = GmData[row]['gm_utc_datetime'].replace(tzinfo=pytz.utc).astimezone(
                                plyTimeZone)
                            localDateTime = datetime.strptime(localDateTime, '%Y-%m-%d %I:%M %p')
                            GmData[row]['gm_date'] = localDateTime
                        if int(daygroup) == 1:
                            if GmDatee != GmData[row]['gm_date']:
                                GmDatee = GmData[row]['gm_date']
                                GamesArray = str(GmData[row]['gm_s_type_name'])
                        else:
                            resArr[row].update({"games": GmData[row]['gm_s_type_name']})
                        if len(GamesArray) > 0:
                            resArr[row].update({"date": GmDatee, "games": GamesArray})
            else:
                GamesArray = {}
                GmDatee = ''
                if len(GmData) > 0:
                    for row in range(len(GmData)):
                        game_info = game_utils.get_game_player_data(str(GmData[row]["gm_id"]), str(PlyId),
                                                                    data['ProjectKey'], data['ProjectSecret'],
                                                                    data['Tkn'], data['dev_id'], gmcals=1)
                        if type(game_info) == str:
                            raise Exception(response.error(message=game_info))
                        game_flags = game_utils.get_game_flags(int(GmData[row]["gm_id"]), int(PlyId))
                        if type(game_flags) == str:
                            raise Exception(response.error(message=game_flags))
                        player_flags = player_utils.get_player_flags(int(GmData[row]["gm_id"]), int(PlyId))
                        if type(player_flags) == str:
                            raise Exception(response.error(message=player_flags))
                        notification_flags = notification_utils.get_notification_flags(int(GmData[row]["gm_id"]),
                                                                                       int(PlyId))
                        if type(notification_flags) == str:
                            raise Exception(response.error(message=notification_flags))
                        game_pay_methods = payment_utils.get_player_payment_methods()
                        if type(game_pay_methods) == str:
                            raise Exception(response.error(message=game_pay_methods))
                        player_pay_methods = payment_utils.get_game_payment_methods()
                        if type(player_pay_methods) == str:
                            raise Exception(response.error(message=player_pay_methods))
                        game_questions = questionnaire_utils.get_game_questionnaire_data(int(GmData[row]["gm_id"]))
                        if type(game_questions) == str:
                            raise Exception(response.error(message=game_questions))
                        player_answers = questionnaire_utils.get_player_questionnaire_answers(int(GmData[row]["gm_id"]),
                                                                                              int(PlyId))
                        if type(player_answers) == str:
                            raise Exception(response.error(message=player_answers))
                        waitlist_players = waitlist_utils.get_game_waitlist_players(int(GmData[row]["gm_id"]))
                        if type(waitlist_players) == str:
                            raise Exception(response.error(message=waitlist_players))
                        GmArr = {**game_info, **game_flags, **player_flags, **notification_flags, **game_pay_methods,
                                 **player_pay_methods, **game_questions, **player_answers, **waitlist_players}
                        for k, v in GmArr.items():
                            if GmArr[k] is None:
                                GmArr[k] = ""
                        localDateTime = ""

                        if plyTimeZone != '' and str(GmData[row]['attend_type']) == 'zoom':
                            localDateTime = GmData[row]['gm_utc_datetime'].replace(tzinfo=pytz.utc).astimezone(
                                plyTimeZone)
                            localDateTime = datetime.strptime(localDateTime, '%Y-%m-%d %I:%M %p')
                        if localDateTime != "":
                            GmData[row]['gm_date'] = str(localDateTime)
                            GmArr['GmDate'] = str(localDateTime).split(" ")[0]
                            GmArr['SSTime'] = str(localDateTime).split(" ")[1]
                        if int(daygroup) == 1:
                            if GmDatee != GmData[row]['gm_date']:
                                GmDatee = GmData[row]['gm_date']
                                GamesArray.update(GmArr)
                            elif GmDatee == GmData[row]['gm_date']:
                                GamesArray.update(GmArr)
                        if len(GamesArray) > 0:
                            resArr[row].update({"date": GmDatee, "games": GamesArray})
            ResArr = [{}]
            for key in resArr:
                for key1, val in key.items():
                    if val is not None:
                        ResArr[0].update({key1: val})
            return response.success(result_data=ResArr)
        else:
            raise Exception(valid['status'])
    except Exception as e:
        return response.error(e.__str__())


def invitations_tab(data):
    try:
        if 'PlyID' in data or 'Type' in data or 'Limit' in data or 'Lat' in data or 'Long' in data:
            where = f" And inv_ply_to_id ={data['PlyID']} " if (
                        data['Type'] == 'Rec') else f" And inv_ply_frm_id ={data['PlyID']} "
            limit = 1 if (int(data['Limit']) < 1) else data['Limit']
            if limit == '':
                raise Exception(response.error(message='Limit needed', data=data))
            number = 50 if 'Number' not in data else data['Number']
            if number == '':
                raise Exception(response.error(message='Number should not be empty', data=data))
            limit_start = (limit - 1) * number
            limit_start = 0 if limit_start == 0.0 else limit_start
            ResArr = []
            adminSql = f"AND gm_org_id" if ('adminId' in data and int(data['adminId']) > 0) else ""
            status = game_utils.preparePlyStatusWithGame(data['PlyID'])
            games_data = execution.execute(f"SELECT invitations.*,\
                    (((acos(sin(({data['Lat']} * pi()/180)) * sin((gm_loc_lat*pi()/180)) + cos(({data['Lat']} * pi()/180)) *\
                    cos((gm_loc_lat*pi()/180)) * cos((({data['Long']} - gm_loc_long)* pi()/180))))*180/pi())*60*1.609344 ) AS GmDist,\
                    gm_id AS GmID,\
                    gm_title AS GmT,\
                    gm_org_id AS OrgID,\
                    {data['PlyID']} AS 'PlyID',\
                    (CASE WHEN gm_org_id = {data['PlyID']} THEN 'true' ELSE 'false'END) AS IsAdmin,gm_img AS GmImg,gm_img AS GmImgThumb,gm_s3_status,gm_max_players AS MaxPly,(\
                        (SELECT COUNT(gm_ply_id) FROM gm_players WHERE gm_id = gm_ply_gm_id AND gm_ply_status = 'y') + (SELECT COUNT(guest_id)FROM guests WHERE gm_id = guest_gm_id AND guests.guest_ply_id = 0)) AS GmPlys,\
                    gm_date AS GmDate,\
                    gm_start_time AS STime,\
                    DATE_FORMAT(gm_start_time, '%l:%i %p') AS SSTime,\
                    gm_end_time AS ETime,\
                    gm_utc_datetime AS UTCDateTime,\
                    gm_country_id AS CountryID,\
                    gm_loc_desc AS LocDesc,\
                    gm_is_free AS IsFree,\
                    gm_policy_id AS PolicyID,\
                    gm_is_stop_recurred AS IsStopRecurred,\
                    (CASE WHEN (gm_recurr_id = 0 AND gm_recurr_times = 1 AND gm_recurr_type IS NOT NULL AND gm_is_stop_recurred = 'n') THEN 'True'\
                        WHEN (gm_recurr_id > 0 AND gm_is_stop_recurred = 'n') THEN 'True' ELSE 'False' END) AS ISRecurr,\
                    (CASE WHEN (gm_recurr_times = 1 AND gm_recurr_type IS NOT NULL AND gm_is_stop_recurred = 'n' AND gm_recurr_id = 0) THEN 'p'\
                        WHEN gm_recurr_id > 0 THEN 'c' ELSE '' END) AS ParentState,\
                    gm_payment_type AS PayType,\
                    gm_fees AS Fees,\
                    currencies.currency_symbol AS Symbol,\
                    currencies.currency_name AS currencyName,\
                    attend_type AS attendType,\
                    IFNULL(gm_status, '') AS GmStatus,\
                    gm_end_pause AS GmEndPause, \
                    {status},\
                    gm_s_type_name AS STypeName\
                    FROM invitations\
                    JOIN game ON inv_gm_id = gm_id\
                    LEFT JOIN gm_s_types ON gm_sub_type_id = gm_s_type_id\
                    LEFT JOIN policy ON gm_policy_id = policy_id\
                    LEFT JOIN currencies ON currency_id=gm_currency_symbol\
                    WHERE (inv_approve = 'y' OR inv_approve = 'p')\
                    AND (gm_status is NULL  OR gm_status = '')\
                    AND (gm_is_free = 'y' OR (gm_is_free = 'n' AND LOWER(gm_payment_type) = 'onsite')\
                        OR (gm_is_free = 'n' AND LOWER(gm_payment_type) = 'stripe' AND gm_org_id IN (SELECT stripe_users_ply_id FROM stripe_users WHERE  stripe_users_account_id IS NOT NULL AND stripe_users_account_id != ''))\
                        OR (gm_is_free='n' AND LOWER(gm_payment_type)='gc' AND gm_org_id IN (SELECT ply_id FROM players WHERE ply_gc_token IS NOT NULL AND ply_gc_oid != '' AND ply_gc_oid IS NOT NULL)))\
                    AND (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP\
                     {where} {adminSql} ORDER BY gm_date ASC LIMIT {limit_start}, 50 ;")

            if games_data and len(games_data) != 0:
                country_id = execution.execute(
                    f"SELECT ply_country_id FROM players WHERE ply_id= {int(data['PlyID'])} AND (ply_status IS NULL OR ply_status = '') ")
                player_country_id = country_id[0]['ply_country_id'] if country_id and len(country_id) > 0 else 0
                ply_time_zone = execution.execute(
                    f"SELECT timezone FROM ply_timezone WHERE player_id={int(data['PlyID'])};")
                time_zone = ply_time_zone[0]['timezone'] if ply_time_zone and len(ply_time_zone) > 0 else ''
                currPlyMethods = game_utils.get_ply_verified_methods(int(data['PlyID']))
                lastDate = ''
                lastDateGms = []
                games = []
                for row in games_data:
                    local_time = game_utils.getGmLocalDateTime(time_zone.encode("UTF-8"), row['attendType'],
                                                               row['UTCDateTime'])
                    if (len(local_time) > 0):
                        row['GmDate'] = local_time[0]
                        row['SSTime'] = local_time[1]
                    row['Symbol'] = game_utils.handleClassCurrencySymbol(row['Symbol'], row['currencyName'],
                                                                         player_country_id, row['CountryID'])
                    row['currPlyMethods'] = currPlyMethods
                    if (int(row['gm_s3_status']) == 1):
                        row['GmImg'] = s3_bucket_url + str(row['GmImg'])
                        row['GmImgThumb'] = s3_bucket_url + str(row['GmImg'].replace("classes", "classes/thumb"))
                    else:
                        row['GmImg'] = s3_bucket_url + "backup/images/upload/gm/" + str(row['GmImg'])
                        row['GmImgThumb'] = s3_bucket_url + "backup/images/upload/gm/thumb/" + row['GmImgThumb']
                    if ('DayGroup' in data and data['DayGroup'] == 1):
                        if (lastDate != row['GmDate']):
                            lastDate = row['GmDate']
                            lastDateGms.append({"date": lastDate, "games": row})
                        else:
                            leng = len(lastDateGms) - 1
                            games[leng]['games'] = games.append(row)
                            lastDateGms[leng]['games'] = games
                        ResArr = lastDateGms
                    else:
                        ResArr.append(row)
                for i in ResArr:
                    for key, value in i.items():
                        if value == None or value == ' ':
                            i[key] = ''
                return response.success(result_data=ResArr)
            else:
                return response.success(result_data=ResArr)
        else:
            raise Exception(response.error(message='Input is missing'))
    except Exception as e:
        return response.error(e.__str__())


def check_notification(data):
    try:
        check = notification_utils.checking_notification_for_player(data)
        if type(check) == str:
            raise Exception(response.error(message=check))
        else:
            return response.success(result_data=check)
    except Exception as e:
        return e


###  gm_plys part ###
def gm_plys(data):
    try:
        if 'gm_id' not in data and not data['gm_id'] and int(data['gm_id']) <= 0:
            raise Exception("invalid gm_id")
        # if 'limit_start' not in data and not data['limit_start'] and int(data['limit_start']) <= 0:
        #     raise Exception("invalid limit_start")
        # if 'limit_number' not in data and not data['limit_number'] and int(data['limit_number']) <= 0:
        #     raise Exception("invalid limit_number")
        # if 'project_id' not in data and not data['project_id'] and int(data['project_id']) <= 0:
        #     raise Exception("invalid project_id")

        gm_id = data['gm_id']
        limit_start = data['limit_start'] if 'limit_start' in data else 0
        limit_number = data['limit_number'] if 'limit_number' in data else 0
        project_id = data['project_id'] if 'project_id' in data else 1

        gm_ply_arr = []
        result = []
        res_arr_dict = {}
        guest_mail_array = []
        contact_ply_id_array = []
        new_dict = {}
        contactID = []

        game_player_data = execution.execute(f"CALL", call_name="GamePlayers",
                                             args=(gm_id, project_id, limit_start, limit_number))
        if str(game_player_data).__contains__("Something went wrong"):
            raise Exception(game_player_data)

        all_guests = player_utils.get_all_guest(gm_id)
        if str(all_guests).__contains__("Something went wrong"):
            raise Exception(all_guests)

        gm_ply_arr = player_utils.set_ply_data(game_player_data, gm_id, project_id)
        if str(gm_ply_arr).__contains__("something happened:"):
            raise Exception(gm_ply_arr)

        gm_PlyD = execution.execute(f"""SELECT * FROM guests
                     LEFT JOIN players ON players.ply_id = guests.guest_ply_id
                     LEFT JOIN city ON city.city_id = players.ply_city_id
                     LEFT JOIN country ON country.country_id = players.ply_country_id
                     WHERE guest_gm_id = {gm_id} Limit {limit_start},{limit_number}""")
        if str(gm_PlyD).__contains__('Something went wrong'):
            raise Exception(gm_PlyD)

        if not gm_PlyD:
            return gm_ply_arr

        for gm_Prow in gm_PlyD:
            # Check if player img exists or not
            PlyImages = {}
            if 'ply_img' in gm_Prow and gm_Prow['ply_img']:
                PlyImages = game_utils.get_ply_images(gm_Prow['ply_img'],gm_Prow['s3_profile'])

            gstGender = ""
            if 'ply_gender' in gm_Prow and gm_Prow['ply_gender']:
                if gm_Prow['ply_gender'] == 'm':
                    gm_Prow['ply_gender'] = "Male"
                elif gm_Prow['ply_gender'] == 'f':
                    gm_Prow['ply_gender'] = "Female"

            if 'ply_id' in gm_Prow and not gm_Prow['ply_id']:
                if 'guest_mail' in gm_Prow:
                    guest_mail_array.append(gm_Prow['guest_mail'])

        if guest_mail_array:
            Id_guest_mail_array = str(tuple([key for key in guest_mail_array])).replace(',)', ')')
            contact_data = execution.execute(f"""SELECT contact_id,contact_ply_id FROM contacts
                                         LEFT JOIN game ON contacts.contact_org_id = game.gm_org_id
                                        WHERE game.gm_id = {gm_id}
                                        AND contacts.contact_email IN {Id_guest_mail_array}""")
            if str(contact_data).__contains__('Something went wrong'):
                raise Exception(contact_data)
            if contact_data:
                for row in contact_data:
                    if 'contact_ply_id' in row and row['contact_ply_id'] and int(row['contact_ply_id']) > 0:
                        contact_ply_id_array.append(row['contact_ply_id'])
                    elif 'contact_id' in row and row['contact_id']:
                        contactID.append(row['contact_id'])

            Id_contact_array = str(tuple([key for key in contact_ply_id_array])).replace(',)', ')')
            playe_data_sql = execution.execute(f"""SELECT * FROM players
                            LEFT JOIN city ON city.city_id = players.ply_city_id
                            LEFT JOIN country ON country.country_id = players.ply_country_id
                            WHERE ply_id IN {Id_contact_array} """)
            if str(playe_data_sql).__contains__('Something went wrong'):
                raise Exception(playe_data_sql)

            if playe_data_sql:
                for gm_Prow in gm_PlyD:
                    for player in playe_data_sql:
                        if 'ply_id' in player and player['ply_id'] and int(player['ply_id']) > 0:
                            gm_Prow['ply_id'] = player['ply_id']
                            gm_Prow['ply_city_id'] = player['ply_city_id']
                            gm_Prow['city_name'] = player['city_name']
                            gm_Prow['ply_country_id'] = player['ply_country_id']
                            gm_Prow['country_name'] = player['country_name']
                            gm_Prow['ply_email_sett'] = player['ply_email_sett']
                            gm_Prow['ply_brithdate_sett'] = player['ply_brithdate_sett']
                            gm_Prow['ply_gender_sett'] = player['ply_gender_sett']
                            gm_Prow['ply_city_sett'] = player['ply_city_sett']
                        if player['ply_gender']:
                            if player['ply_gender'] == 'm':
                                player['ply_gender'] = "Male"
                            elif player['ply_gender'] == 'f':
                                player['ply_gender'] = "Female"
                        gm_Prow['ply_gender'] = player['ply_gender']

        for gm_Prow in gm_PlyD:
            res_arr_dict['PlyID'] = gm_Prow['ply_id'] if gm_Prow['ply_id'] else gm_Prow['guest_id'],
            res_arr_dict['PlyFname'] = urllib.parse.unquote(gm_Prow['guest_fname']),
            res_arr_dict['PlyLname'] = urllib.parse.unquote(gm_Prow['guest_fname']),
            res_arr_dict['PlyEmail'] = gm_Prow['guest_mail'],
            res_arr_dict['PlyGdr'] = gm_Prow['ply_gender'],
            res_arr_dict['PlyHeight'] = "",
            res_arr_dict['H_Unt'] = "",
            res_arr_dict['PlyWeight'] = "",
            res_arr_dict['W_Unt'] = "",
            res_arr_dict['PlyctyID'] = gm_Prow['ply_city_id'] if gm_Prow['ply_city_id'] else "",
            res_arr_dict['PlyCty'] = gm_Prow['city_name'] if gm_Prow['city_name'] else "",
            res_arr_dict['PlyCountryID'] = gm_Prow['ply_country_id'] if gm_Prow['ply_country_id'] else "",
            res_arr_dict['PlyCountry'] = gm_Prow['country_name'] if gm_Prow['country_name'] else "",
            res_arr_dict['PImg'] = 'ply/' + gm_Prow['ply_img'] if gm_Prow['ply_img'] else "",
            res_arr_dict['LastGm'] = [],
            res_arr_dict['Privecy'] = {'mail': "True" if gm_Prow['ply_email_sett'] == "y" else "False",
                                       'birthdate': "True" if gm_Prow['ply_brithdate_sett'] == "y" else "False",
                                       'gender': "True" if gm_Prow['ply_gender_sett'] == "y" else "False",
                                       'city': "True" if gm_Prow['ply_city_sett'] == "y" else "False"
                                       },
            res_arr_dict['FrStatus'] = "",
            res_arr_dict['FrStatusAdmin'] = "",
            res_arr_dict['PlyImg'] = gm_Prow['PlyImg'] if PlyImages else "",
            res_arr_dict['PlyImgThumb'] = gm_Prow['PlyImgThumb'] if PlyImages else "",
            res_arr_dict['PlyType'] = "member" if gm_Prow['ply_id'] else "guest",
            res_arr_dict['IsCheckedIn'] = gm_Prow['guest_checkedIn'],
            for id in contactID:
                res_arr_dict['ContactID'] = id
            result.append(res_arr_dict)

        return response.success(result_data=result)


    except Exception as e:
        return response.error(e.__str__())
