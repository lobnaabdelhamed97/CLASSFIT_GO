import base64
import json
from datetime import datetime
from json import JSONDecodeError
import requests
import hashlib
import database.response as response

import utils.game_utils as game_utils
import utils.player_utils as player_utils
from database import config, execution


def get_notification_flags(game_id, player_id):
    """"
    desc: get notification flags and checks(boolean values) that used in game_view
    input: game_id,player_id
    output: result[HasStopDays,NState,HaveReminder,RemindStat,RemindPeriod]
    """
    try:
        if game_id and game_id > 0 and player_id and int(player_id) > 0:
            recurr_id = execution.execute(
                f"SELECT recurr_notifications_id FROM recurr_notifications join game on gm_id={game_id} WHERE recurr_notifications_ply_id= {player_id} and recurr_notifications_recurred_gm_id={game_id} or recurr_notifications_recurred_gm_id=game.gm_recurr_id;")
            HasStopDays = 'n' if not recurr_id else 'y'
            state = 'off'
            Nsql = execution.execute(
                f"SELECT notifications_game_stop,notifications_state FROM notifications WHERE notifications_ply_id={player_id}")
            if Nsql:
                if Nsql[0]['notifications_state'] == 0:
                    state = 'off'
                elif Nsql[0]['notifications_state'] == 1:
                    state = 'on'
                if Nsql[0]['notifications_game_stop'] and int(game_id) > 0:
                    days = Nsql[0]['notifications_game_stop'].split(",")
                    if game_id in days:
                        state = 'off'
                    else:
                        state = 'on'
            else:
                state = 'on'
            HaveReminderSql = execution.execute(f"SELECT custom_notification_id FROM custom_notifications WHERE "
                                                f"custom_notification_gm_id {game_id} AND custom_notification_ply_id={player_id};")
            HaveReminder = 'n' if not HaveReminderSql else 'y'

            RemindStat = execution.execute(f"SELECT custom_notification_reminder_status as status , custom_notification_period as \
                               period FROM custom_notifications WHERE custom_notification_gm_id ={game_id} AND \
                               custom_notification_ply_id = {player_id};")
            if not RemindStat:
                RemindStat = [dict()]
                RemindStat[0]["status"] = ''
                RemindStat[0]["period"] = ''
            return {'HasStopDays': HasStopDays, 'NState': state, 'HaveReminder': HaveReminder,
                    'RemindStat': RemindStat[0]['status'], 'RemindPeriod': RemindStat[0]["period"]}
        else:
            raise Exception("Player and Game ID is required")

    except Exception as e:
        return e.__str__()


def decode_bytes(data):
    return data.decode('utf-8')


def adabt_notify_array(project_id, type, message, data=[]):
    """"
    desc: adapts the notfication according to the type of notfication
    input: project_id,type, message , data =[]
    output: result_data array which will be composed ot title , body message and action click
    """
    result_data = []

    project_domain = execution.execute(
        f"SELECT project_domain,project_short FROM projects  WHERE project_id= {project_id}")

    if project_domain[0]:
        domain = project_domain[0]['project_domain']
        project_short = project_domain[0]['project_short']

    if data['Gm']:
        game_data = data['Gm']
        # [0]
        # game_data = json.dumps(game_data, default=decode_bytes, indent=4)
        game_id = game_data['GmID']
        # for i in range(len(game_data)):
        #     game_data[i] = "app\helpers\Util::DecodeData"

        # player_data = 
        execution.execute(
            f"SELECT ply_fname,ply_lname,ply_email FROM players where ply_id={game_data['OrgID']}")

        # if player_data and not str(player_data).__contains__(
        #     'Something went wrong') and 'ply_fname' in player_data[0] \
        #     and 'ply_lname' in player_data[0] and 'ply_email' in player_data[0]:
        #     raise Exception(player_data)
        # player_data = player_data[0]
        # for i in range(len(player_data)):
        #     player_data[i] = "app\helpers\Util::DecodeData"
        # player_data = json.dumps(player_data, default=decode_bytes, indent=4)

        # game_date_represented = datetime.strptime(data['Gm'][0]["GmDate"], '%Y-%m-%d')

    # if data['AdmData']:
    #     player_data = data['AdmData']
    #     # for i in range(len(player_data)):
    #     #     player_data[i] = "app\helpers\Util::DecodeData"
    #     player_data = json.dumps(player_data, default=decode_bytes, indent=4)

    click_action = f'{domain}/index.php/{project_short}/Game/{game_id}'

    if type and message:
        if type == "InvFriToGm":
            result_data = {'title': 'Invitation received', 'body': message, 'click_action': click_action}
        if type == "MinReached":
            result_data = {'title': 'Minimum Reached', 'body': message, 'click_action': click_action}
        if type == "MaxReached":
            result_data = {'title': 'Maximum Reached', 'body': message, 'click_action': click_action}
        if type == "ReqToGm":
            result_data = {'title': 'Game is full', 'body': message, 'click_action': click_action}
        if type == "RegPly":
            result_data = {'title': 'Register Player', 'body': message, 'click_action': click_action}
        if type == "FrReq":
            result_data = {'title': 'Friend Request', 'body': message, 'click_action': click_action}
        if type == "FrRes":
            result_data = {'title': 'Good news', 'body': message, 'click_action': click_action}
        if type == "InvFriToGmFrmWait":
            result_data = {'title': 'Invitation Recieved', 'body': message, 'click_action': click_action}
        if type == "CancelGm":
            result_data = {'title': 'Game Cancelled', 'body': message, 'click_action': click_action}
        if type == "EditGm":
            result_data = {'title': 'Game Edited', 'body': message, 'click_action': click_action}
        if type == "GmMinNotReached":
            result_data = {'title': 'Minimum Not Reached', 'body': message, 'click_action': click_action}
        if type == "ReminderGm":
            result_data = {'title': 'Reminder', 'body': message, 'click_action': click_action}
        if type == "GameChat":
            result_data = {'title': 'Game Chat Message', 'body': message, 'click_action': click_action}
        if type == "FrChat":
            result_data = {'title': 'Friend Chat Message', 'body': message, 'click_action': click_action}

    return result_data


def handle_icon_image(project_id):
    """"
    desc: resposible for handling the icon image
    input: project_id
    output: result
    """
    project_short = execution.execute(f"SELECT project_short FROM projects WHERE project_id = {project_id}")

    if project_short:
        project_short = project_short[0]['project_short']

        if project_short == 'r':
            result = '/images/logo.png'
        if project_short == 'c' or project_short == 'i':
            result = '/images/classfit-notify-logo.png'
    return result


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


def handle_notification_typo(notfication_data):
    result = notfication_data
    for key in notfication_data:
        list = {"Type", "Mess", "title", "body", "click_action"}
        if key in list:
            value = str(value).replace(
                ["games", "Games", "game", "Game", "GmSearch", "Event", "Events", "event", "events"],
                ["classes", "Classes", "class", "Class", "SearchClass", "Class", "Classes", "class", "classes"])
    return result


def send_web_notification(token_ids, notfication):
    try:
        if token_ids:
            url = config.web_notification_url
            params = {
                'registration_ids': token_ids,
                'notification': notfication,
                'webpush': json.dumps({"headers": {'TTL': 60}}),
                'ProjectKey': '1234',
                'ProjectSecret': '1234'
            }
            payload = json.dumps(params)
            secret_key = key_sec(params)
            headers = {
                'Key-Sec': secret_key,
                'Content-Type': 'application/json; charset=utf-8'
            }

            responses = requests.request("POST", url, headers=headers, data=payload)
            # to know if it is working curl correctly use var dumps in php

            # return json.loads(responses.text.encode('utf8'))

            return responses
            # json.loads(responses.text.encode('utf8'))
    except ConnectionError:
        return 'callSendWebNotification: Error in Connection.'
    except JSONDecodeError:
        return 'callSendWebNotification: Error Json Decode.'
    # except Exception:
    #     return 'Error In callSendWebNotification.'
    except Exception as e:
        return e


def send_notification(regs_ids, message, params):
    try:

        fcm_arr = []
        gcm_arr = []

        for i in range(regs_ids):
            if regs_ids[i][11:1:":"]:
                fcm_arr.append(regs_ids[i])
            else:
                gcm_arr.append(regs_ids[i])

        url = config.web_notification_url
        google_api_key = params['pushkeys'][1]
        if gcm_arr:
            fields = {
                'registration_ids': gcm_arr,
                'data': {"message": message}
            }
            payload = json.dumps(fields)
            secret_key = key_sec(params)
            headers = {
                'Key-Sec': secret_key + google_api_key,
                'Content-Type': 'application/json; charset=utf-8'
            }

            responses = requests.request("POST", url, headers=headers, data=payload)

        if fcm_arr:
            fields = {
                'registration_ids': fcm_arr,
                'data': {"message": message}
            }
            payload = json.dumps(fields)
            secret_key = key_sec(params)
            headers = {
                'Key-Sec': secret_key + google_api_key,
                'Content-Type': 'application/json; charset=utf-8'
            }

            responses = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(responses.text.encode('utf8'))

    except ConnectionError:
        return 'callSendNotification: Error in Connection.'
    except JSONDecodeError:
        return 'callSendNotification: Error Json Decode.'
    except Exception:
        return 'Error In callSendNotification.'


def send_ios_notification(regs_ids, message, params):
    try:

        fcm_arr = []
        rids_arr = []

        for i in range(regs_ids):
            if regs_ids[i][11:1:":"]:
                fcm_arr.append(regs_ids[i])
            else:
                rids_arr.append(regs_ids[i])

        url = config.web_notification_url
        google_api_key = params['pushkeys'][1]

        if fcm_arr:
            fields = {
                'registration_ids': json.dumps(regs_ids),
                "message": message,
                'MD5': hashlib.md5('fastplayiosapns'.encode()),
                'filecert': params['applepushfile'][1],
                'mode': params['mode']
            }
            payload = json.dumps(fields)
            secret_key = key_sec(params)
            headers = {
                'Key-Sec': secret_key + google_api_key,
                'Content-Type': 'application/json; charset=utf-8'
            }

            responses = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(responses.text.encode('utf8'))

    except ConnectionError:
        return 'callSendIOSNotification: Error in Connection.'
    except JSONDecodeError:
        return 'callSendIOSNotification: Error Json Decode.'
    except Exception:
        return 'Error In callSendIOSNotification.'


def put_needed_keys(data=[]):
    game_keys = {
        'GmID', 'GmT', 'IsHis', 'OrgID', 'OrgName', 'OrgImg', 'DisOrg', 'Parent', 'TypeID', 'TypeName',
        'TypeImg', 'myType', 'STypeID', 'STypeName', 'STypeImg', 'CourtID', 'CourtT', 'LevelID',
        'LevelT', 'GmImg', 'Gdr', 'Age', 'MinPly', 'MaxPly', 'GmPlys', 'MemGm', 'Days', 'CurrencyID',
        'Symbol', 'GmDist', 'NState', 'ISRecurr', 'ParentState', 'IsStopRecurred', 'OrgMem',
        'GmStatus', 'GmDate', 'STime', 'ETime', 'CityID', 'CityName', 'Lat', 'Long', 'LocDesc', 'Scope',
        'HasGlly', 'IsFree', 'PayType', 'Fees', 'PolicyID', 'PolicyT', 'showMem', 'ChkPlyAns',
        'IsStopRecurred', 'RenewID', 'GmReqQues'
    }

    # clear game keys
    if data['Gm'][0]:
        for key in data['Gm'][0]:
            if key in game_keys: del data['Gm'][0][key]

    # allowed player keys
    player_keys = {
        'PlyID', 'PlyFname', 'PlyLname', 'PlyEmail', 'PlyBDate', 'PlyGdr', 'PlyHeight', 'H_Unt', 'PlyWeight', 'W_Unt',
        'PlyctyID',
        'PlyCty', 'PlyImgThumb', 'PlyImg', 'PlyAge', 'FrStatus', 'Privecy', 'PlyBDate', 'PlyGdr', 'CountryID',
        'CountryName'
    }

    # clear player keys
    if data['Ply'][0]:
        for key in data['Ply'][0]:
            if key in player_keys: del data['Ply'][0][key]

    if data['Fr'][0]:
        for key in data['Fr'][0]:
            if key in player_keys: del data['Fr'][0][key]

    return data


def checking_notification_for_player(data):
    # project_id , game_id , player_id  , typeo , message , data ,  ProjectKey, ProjectSecret, tkn, dev_id, title =""):
    """
    input : player_id , type , message , data , title
    description : - check game is recurr  or not 
                  - check player notification
                  - check notifications is stopped or not for this game with this player
    """
    try:
        if not data['project_id'] or data['project_id'] == "" or type(data['project_id']) != int:
            raise Exception("invalid project_id")
        if not data['game_id'] or data['game_id'] == "" or type(data['game_id']) != int:
            raise Exception("invalid game_id")
        if not data['player_id'] or data['player_id'] == "" or type(data['player_id']) != int:
            raise Exception("invalid player_id")
        if not data['typeo'] or data['typeo'] == "" or type(data['typeo']) != str:
            raise Exception("invalid type")
        if not data['message'] or data['message'] == "" or type(data['message']) != str:
            raise Exception("invalid message")
        if not data or data == "":
            raise Exception("invalid data")
        if not data['ProjectKey'] or data['ProjectKey'] == "" or type(data['ProjectKey']) != str:
            raise Exception("invalid project key")
        if not data['ProjectSecret'] or data['ProjectSecret'] == "" or type(data['ProjectSecret']) != str:
            raise Exception("invalid project secret")
        if not data['tkn'] or data['tkn'] == "" or type(data['tkn']) != str:
            raise Exception("invalid token")
        if not data['dev_id'] or data['dev_id'] == "" or type(data['dev_id']) != str:
            raise Exception("invalid device_id")

        title = "game"
        result_array = []
        recurr_id = data['Gm']['RecurrID']

        if data['player_id']:
            # and int(player_id) > 0 and type and str(type) == "" and message and str(message) == "" and title and str(title) == ""   :
            if recurr_id > 0:
                recurr_notification = execution.execute(
                    f"SELECT recurr_notifications_stop_days FROM recurr_notifications WHERE recurr_notifications_ply_id = {data['player_id']}  AND recurr_notifications_recurred_gm_id = {recurr_id}"
                )
            else:
                recurr_notification = execution.execute(
                    f"SELECT recurr_notifications_stop_days FROM recurr_notifications WHERE recurr_notifications_ply_id = {data['player_id']}  AND recurr_notifications_recurred_gm_id = {data['game_id']}"
                )

            if recurr_notification:

                days_array = recurr_notification['recurr_notifications_stop_days'].split(',')
                game_date = datetime.strptime(data['Gm'][0]["GmDate"], '%Y-%m-%d')
                game_day = game_date.day
                check_member_game = execution.execute(
                    f" SELECT * FROM gm_players WHERE gm_ply_gm_id = {data['game_id']}  \
                            AND gm_ply_status = 'y' \
                            AND (gm_ply_leave IS NULL OR gm_ply_leave = '')\
                            AND gm_ply_ply_id = {data['player_id']} ")

                # check if player waitlist in this game
                check_if_waitlist = execution.execute(
                    f"SELECT gm_wait_list_id FROM gm_waitlist \
                        WHERE gm_wait_list_gm_id={data['game_id']} \
                        AND gm_wait_list_ply_id={data['player_id']}\
                        AND gm_wait_list_withdrew = 0 \
                        AND gm_wait_list_removed_by_admin = 0")

                if game_day in days_array and check_member_game == False and check_if_waitlist == False:
                    return result_array
        # check if the notifications is stopped or not for this player
        if data['player_id'] and data['player_id'] > 0:
            notify_data = execution.execute(
                f"SELECT notifications_state FROM notifications WHERE notifications_ply_id = {data['player_id']}"
            )
            if notify_data:
                for notify_data_row in notify_data:
                    if notify_data_row['notifications_state'] and notify_data_row['notifications_state'] == 0:
                        return result_array
        # check if the notifications is stopped or not for this game with this player
        if data['Gm']['GmID']:
            notify_data = execution.execute(
                f"SELECT notifications_game_stop FROM notifications WHERE notifications_ply_id= {data['player_id']}"
            )
            notify_data_array = notify_data[0]['notifications_game_stop']
            # .split(',')

            if notify_data_array:
                if data['Gm']["GmID"] in notify_data_array:
                    return result_array
        if data['Gm']:
            # prevent invitation notifications if admin not connected 
            is_connected = game_utils.get_ply_verified_methods(data['Gm']['OrgID'])
            if ((data['typeo'] == "InvFriToGmFrmWait" or data['typeo'] == "InvFriToGm") and (
            data['Gm']['PayType']).lower() == 'gc' and is_connected['GoCardless'] != 'y'):
                return result_array

                # filter data to minimize its size
            data['Gm']['Req'] = ''
            data['Gm']['Notes'] = ''
            data['Gm']['Rules'] = ''
            data['Gm']['Kits'] = ''

            # check type of device to send notification according to it  
            android_reg_arr = player_utils.android_players_regs(data['project_id'], data['player_id'])
            web_reg_arr = player_utils.web_players_regs(data['project_id'], data['player_id'])
            ios_reg_arr = player_utils.ios_players_regs(data['project_id'], data['player_id'])

            # params = {'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret, 'DevID': dev_id,
            #           'PlyID': data['Gm'][0]['OrgID'], 'Tkn': tkn}
            # print(params)

            if web_reg_arr:
                if data['Gm']:
                    ply_data = execution.execute(
                        f"SELECT ply_fname,ply_lname from players where ply_id = {data['player_id']}")

                    data['AdmData'] = ply_data
                    data['AdmData'] = data['AdmData'][0]
                # if data['Fr']:
                #     data['AdmData'] = data['Fr']
                #     data['AdmData'] = data['AdmData'][0]
                notify_data_array = adabt_notify_array(data['project_id'], data['typeo'], data['message'], data)
                # result_notification = send_web_notification(web_reg_arr ,notify_data_array)

                notify_data_array['icon'] = handle_icon_image(data['project_id'])
                # result_notification = 
                send_web_notification(web_reg_arr, notify_data_array)
                result_array = {'Result': 'True'}
                # {"output": "true"}
                # {'Result' :'true'}
            if android_reg_arr:
                notify_data_array = []
                notify_data_array['Type'] = data['typeo']
                notify_data_array['Mess'] = data['message']

                data['Gm'][0]['Recurr'] = ''
                data['Gm'][0]['Wait'] = ''
                data['AdmData'] = ''

                notify_data_array['Data'] = data

                # filter data to minimize its size 
                notify_data_array['Data'] = put_needed_keys(notify_data_array['Data'])
                params = {'ProjectKey': data['ProjectKey'], 'ProjectSecret': data['ProjectSecret'],
                          'DevID': data['dev_id'],
                          'PlyID': data['Gm'][0]['OrgID'], 'Tkn': data['tkn']}
                # result_notification = 
                send_notification(android_reg_arr, data['message'], params)
                result_array = {'Result': 'True'}
                # {"output": "true"}
                # {'Result' :'true'}
                # 'Result' => 'True'

            if ios_reg_arr:
                notify_data_array = []
                notify_data_array['Type'] = data['typeo']
                notify_data_array['Mess'] = data['message']
                notify_data_array['Data'] = data
                notify_data_array['Title'] = title

                if data['Gm'][0]['GmID'] and data['Gm'][0]['Fees'] and data['Gm'][0]['PayType']:
                    game_id = data['Gm'][0]['GmID']
                    fees = data['Gm'][0]['Fees']
                    pay_type = data['Gm'][0]['PayType']

                if data['Members']:
                    members = data['Members']

                if data['frChat']:
                    fr_chat = data['frChat']

                if data['Fr']:
                    frs = data['Fr']

                notify_data_array['Data'] = {
                    'GmID': game_id,
                    'Fees': fees,
                    'PayType': pay_type,
                    'Frs': frs,
                    'Members': members,
                    'frChat': fr_chat
                }

                # result_notification = 
                send_ios_notification(ios_reg_arr, data['message'], params)

            # return result_array
            return result_array

        else:
            raise Exception("Player and Game ID is required")
    except Exception as e:
        return e.__str__()

# def checking_notification_for_playerrrrrrrrrr(project_id , game_id , player_id  , typeo , message , data ,  ProjectKey, ProjectSecret, tkn, dev_id, title =""):

# def checking_notification_for_player(project_id, game_id, player_id, typeo, message, data, ProjectKey, ProjectSecret,
#                                      tkn, dev_id, title=""):
#     """
#     input : player_id , type , message , data , title
#     description : - check game is recurr  or not 
#                   - check player notification
#                   - check notifications is stopped or not for this game with this player
#     """
#     try:
#         if not project_id or project_id == "" or type(project_id) != int:
#             raise Exception("invalid project_id")
#         if not game_id or game_id == "" or type(game_id) != int:
#             raise Exception("invalid game_id")
#         if not player_id or player_id == "" or type(player_id) != int:
#             raise Exception("invalid player_id")
#         if not typeo or typeo == "" or type(typeo) != str:
#             raise Exception("invalid type")
#         if not message or message == "" or type(message) != str:
#             raise Exception("invalid message")
#         if not data or data == "":
#             raise Exception("invalid data")
#         if not ProjectKey or ProjectKey == "" or type(ProjectKey) != str:
#             raise Exception("invalid project key")
#         if not ProjectSecret or ProjectSecret == "" or type(ProjectSecret) != str:
#             raise Exception("invalid project secret")
#         if not tkn or tkn == "" or type(tkn) != str:
#             raise Exception("invalid token")
#         if not dev_id or dev_id == "" or type(dev_id) != str:
#             raise Exception("invalid device_id")

#         title = "game"
#         result_array = []
#         recurr_id = data['Gm']['RecurrID']
#         # [0]
#         # ['RecurrID']

#         if player_id:
#             # and int(player_id) > 0 and type and str(type) == "" and message and str(message) == "" and title and str(title) == ""   :
#             if recurr_id > 0:
#                 recurr_notification = execution.execute(
#                     f"SELECT recurr_notifications_stop_days FROM recurr_notifications WHERE recurr_notifications_ply_id = {player_id}  AND recurr_notifications_recurred_gm_id = {recurr_id}"
#                 )
#             else:
#                 recurr_notification = execution.execute(
#                     f"SELECT recurr_notifications_stop_days FROM recurr_notifications WHERE recurr_notifications_ply_id = {player_id}  AND recurr_notifications_recurred_gm_id = {game_id}"
#                 )

#             if recurr_notification:

#                 days_array = recurr_notification['recurr_notifications_stop_days'].split(',')
#                 game_date = datetime.strptime(data['Gm'][0]["GmDate"], '%Y-%m-%d')
#                 game_day = game_date.day
#                 check_member_game = execution.execute(
#                     f" SELECT * FROM gm_players WHERE gm_ply_gm_id = {game_id}  \
#                             AND gm_ply_status = 'y' \
#                             AND (gm_ply_leave IS NULL OR gm_ply_leave = '')\
#                             AND gm_ply_ply_id = {player_id} ")

#                 # check if player waitlist in this game
#                 check_if_waitlist = execution.execute(
#                     f"SELECT gm_wait_list_id FROM gm_waitlist \
#                         WHERE gm_wait_list_gm_id={game_id} \
#                         AND gm_wait_list_ply_id={player_id}\
#                         AND gm_wait_list_withdrew = 0 \
#                         AND gm_wait_list_removed_by_admin = 0")

#                 if game_day in days_array and check_member_game is False and check_if_waitlist is False:
#                     return result_array
#         # check if the notifications is stopped or not for this player
#         if player_id and player_id > 0:
#             notify_data = execution.execute(
#                 f"SELECT notifications_state FROM notifications WHERE notifications_ply_id = {player_id}"
#             )
#             if notify_data:
#                 for notify_data_row in notify_data:
#                     if notify_data_row['notifications_state'] and notify_data_row['notifications_state'] == 0:
#                         return result_array
#         # check if the notifications is stopped or not for this game with this player
#         if data['Gm']['GmID']:
#             notify_data = execution.execute(
#                 f"SELECT notifications_game_stop FROM notifications WHERE notifications_ply_id= {player_id}"
#             )
#             notify_data_array = notify_data[0]['notifications_game_stop']
#             # .split(',')

#             if notify_data_array:
#                 if data['Gm']["GmID"] in notify_data_array:
#                     return result_array
#         if data['Gm']:
#             # prevent invitation notifications if admin not connected 
#             is_connected = game_utils.get_ply_verified_methods(data['Gm']['OrgID'])
#             if ((typeo == "InvFriToGmFrmWait" or typeo == "InvFriToGm") and (data['Gm']['PayType']).lower() == 'gc' and
#                     is_connected['GoCardless'] != 'y'):
#                 return result_array

#                 # filter data to minimize its size
#             data['Gm']['Req'] = ''
#             data['Gm']['Notes'] = ''
#             data['Gm']['Rules'] = ''
#             data['Gm']['Kits'] = ''

#             # check type of device to send notification according to it  
#             android_reg_arr = player_utils.android_players_regs(project_id, player_id)
#             web_reg_arr = player_utils.web_players_regs(project_id, player_id)
#             ios_reg_arr = player_utils.ios_players_regs(project_id, player_id)

#             # params = {'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret, 'DevID': dev_id,
#             #           'PlyID': data['Gm'][0]['OrgID'], 'Tkn': tkn}
#             # print(params)

#             if web_reg_arr:
#                 if data['Gm']:
#                     ply_data = execution.execute(
#                         f"SELECT ply_fname,ply_lname from players where ply_id = {player_id}")

#                     data['AdmData'] = ply_data
#                     data['AdmData'] = data['AdmData'][0]
#                 # if data['Fr']:
#                 #     data['AdmData'] = data['Fr']
#                 #     data['AdmData'] = data['AdmData'][0]
#                 notify_data_array = adabt_notify_array(project_id, typeo, message, data)
#                 # result_notification = send_web_notification(web_reg_arr ,notify_data_array)

#                 notify_data_array['icon'] = handle_icon_image(project_id)
#                 # result_notification = 
#                 send_web_notification(web_reg_arr, notify_data_array)
#                 result_array = {'Result': 'true'}
#             if android_reg_arr:
#                 notify_data_array = []
#                 notify_data_array['Type'] = typeo
#                 notify_data_array['Mess'] = message

#                 data['Gm'][0]['Recurr'] = ''
#                 data['Gm'][0]['Wait'] = ''
#                 data['AdmData'] = ''

#                 notify_data_array['Data'] = data

#                 # filter data to minimize its size 
#                 notify_data_array['Data'] = put_needed_keys(notify_data_array['Data'])
#                 params = {'ProjectKey': ProjectKey, 'ProjectSecret': ProjectSecret, 'DevID': dev_id,
#                           'PlyID': data['Gm'][0]['OrgID'], 'Tkn': tkn}
#                 # result_notification = 
#                 send_notification(android_reg_arr, message, params)
#                 result_array = {'Result': 'true'}

#             if ios_reg_arr:
#                 notify_data_array = []
#                 notify_data_array['Type'] = typeo
#                 notify_data_array['Mess'] = message
#                 notify_data_array['Data'] = data
#                 notify_data_array['Title'] = title

#                 if data['Gm'][0]['GmID'] and data['Gm'][0]['Fees'] and data['Gm'][0]['PayType']:
#                     game_id = data['Gm'][0]['GmID']
#                     fees = data['Gm'][0]['Fees']
#                     pay_type = data['Gm'][0]['PayType']

#                 if data['Members']:
#                     members = data['Members']

#                 if data['frChat']:
#                     fr_chat = data['frChat']

#                 if data['Fr']:
#                     frs = data['Fr']

#                 notify_data_array['Data'] = {
#                     'GmID': game_id,
#                     'Fees': fees,
#                     'PayType': pay_type,
#                     'Frs': frs,
#                     'Members': members,
#                     'frChat': fr_chat
#                 }

#                 # result_notification = 
#                 send_ios_notification(ios_reg_arr, message, params)

#             return result_array

#         else:
#             raise Exception("Player and Game ID is required")
#     except Exception as e:
#         return e.__str__()
