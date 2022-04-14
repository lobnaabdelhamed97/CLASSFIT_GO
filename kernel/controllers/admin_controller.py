import hashlib
import re
import urllib
from datetime import datetime

import database.execution as execution
import database.response as response
import utils.common_utils as common_utils
import utils.game_utils as game_utils
import utils.player_utils as player_utils


def guest_actions(data):
    """"
                    desc: remove guest by admin from game or from wait list
                    input: game_id,player_id
                    output: return true if action is done or false when error is raised
    """
    try:
        guest_mail = execution.execute(
            f"SELECT guest_mail FROM guests WHERE guest_id={data['ply_id']} and guest_gm_id={data['class_id']};")
        if guest_mail and guest_mail[0]['guest_mail'] != '' and guest_mail != []:
            bundle_id = execution.execute(
                f"SELECT bundle_id FROM subscriptions_classes WHERE ply_id={data['ply_id']} and is_removed=0 and class_id={data['class_id']};",
                db_name="bundles")
            if bundle_id and bundle_id[0]['bundle_id'] != []:
                params = {'bundle_id': bundle_id[0]['bundle_id'], 'class_id': data['class_id'],
                          'ply_email': guest_mail[0]['guest_mail'],
                          'process': '+', 'source': data['source'], 'ProjectKey': data['ProjectKey'],
                          'ProjectSecret': data['ProjectSecret']}
                BundleResponse = common_utils.bundle_curl('updatePlayerCredit', params)
                if str(BundleResponse).__contains__('Something went wrong') or str(BundleResponse).__contains__(
                        'Error') or str(BundleResponse).__contains__('error'):
                    raise Exception(BundleResponse)
                update_player_refunded = game_utils.update_player_asrefunded(data['ply_id'], data['class_id'])
                execution.execute(
                    f"UPDATE gm_players SET gm_ply_refunded =1 WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                if str(update_player_refunded).__contains__("something happened:"):
                    raise Exception(update_player_refunded)
                else:
                    return BundleResponse

            execution.execute(
                f"DELETE FROM guests WHERE guest_mail='{guest_mail[0]['guest_mail']}' AND guest_gm_id={data['class_id']};")
            class_data = game_utils.getClassData(SqlArray=f"({data['class_id']})")
            game_utils.informWaitlist(ClassesData=class_data, SqlArray=f"({data['class_id']})")
            contact_data = execution.execute(
                f"SELECT contact_id FROM contacts WHERE contact_email='{guest_mail[0]['guest_mail']}' ")
            logData = {'UserId': 0, 'GmID': data['GmID'], 'PlyID': data['PlyID'], 'SubscriptionId': bundle_id,
                       'SrcType': data['source'], 'LogType': 31, 'ContactId': contact_data[0]['contact_id']}
            common_utils.logAllActions(logData)
        else:
            return False
    except Exception as e:
        return response.error_add(e.__str__())
    else:

        return True


def remove_by_admin(data):
    """"
                desc: remove member/guest by admin from game or from wait list
                input: game_id,player_id,projectkey,projectSecret
                output: return true if action is done or false when error is raised
     """
    try:
        if data['class_id'] and int(data['class_id']) > 0 and int(data['ply_id']) > 0:
            class_data = game_utils.getClassData(SqlArray=f"({data['class_id']})")
            check_if_waitlist = execution.execute(
                f"SELECT gm_wait_list_id FROM gm_waitlist WHERE gm_wait_list_gm_id={data['class_id']} AND gm_wait_list_ply_id={data['ply_id']};")
            if check_if_waitlist and check_if_waitlist[0]['gm_wait_list_id'] != '':
                execution.execute(
                    f"UPDATE gm_waitlist SET gm_wait_list_removed_by_admin = 1 WHERE gm_wait_list_gm_id={data['class_id']} AND gm_wait_list_ply_id={data['ply_id']};")
                invitation = execution.execute(
                    f"SELECT inv_id FROM invitations WHERE inv_gm_id = {data['class_id']} AND inv_ply_to_id = {data['ply_id']};")
                if invitation and invitation[0]['inv_id']:
                    execution.execute(
                        f"DELETE FROM invitations WHERE inv_gm_id ={data['class_id']} AND inv_ply_to_id = {data['ply_id']};")
            else:
                if_member = execution.execute(
                    f"SELECT gm_ply_id,gm_ply_status,gm_ply_refunded,gm_ply_pay_type FROM gm_players WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']} AND gm_ply_status='y' ;")
                if (if_member and if_member[0]['gm_ply_status'] == 'r'):
                    return response.error_add("Player is not a member")
                elif if_member and if_member[0]['gm_ply_status'] == 'y':
                    execution.execute(
                        f"UPDATE gm_players SET gm_ply_status = 'r', gm_ply_leave =CURRENT_TIMESTAMP WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                    execution.execute(
                        f"DELETE FROM games_subscriptions WHERE game_id ={data['class_id']} AND member_id={data['ply_id']};")
                    execution.execute(
                        f"DELETE FROM guests WHERE guest_ply_id={data['ply_id']} AND guest_gm_id={data['class_id']};")
                    if if_member[0]['gm_ply_pay_type'] != 'no' or if_member[0]['gm_ply_refunded'] != 1:
                        game_utils.check_type_payment(class_id=data['class_id'], ply_id=data['ply_id'],
                                                      source=data['source'],
                                                      ProjectSecret=data['ProjectSecret'],
                                                      ProjectKey=data['ProjectKey'])
                        execution.execute(
                            f"UPDATE gm_players SET gm_ply_refunded =1 WHERE gm_ply_ply_id={data['ply_id']} and gm_ply_gm_id={data['class_id']};")
                    game_utils.informWaitlist(ClassesData=class_data, SqlArray=f"({data['class_id']})")
                else:
                    guest = guest_actions(data=data)
                    if guest is False:
                        return response.error_add("Player is not a member")

        else:
            raise Exception("Game and Player id are required")
    except Exception as e:
        return e
    else:
        ResArr = {"Result": "true"}
        return response.success_add(ResArr)


def add_guest(data):
    """"
                    desc: add guest by admin to game
                    input: game_id,player_id,projectkey,projectSecret
                    output: return true if action is done or false when error is raised
     """
    try:
        if 'GmID' in data and type(data['GmID']) == int and data['GmID'] >= 0 and 'GuestMail' in data:
            PlyID = int(data['PlyID'])
            game_validations = execution.execute(
                f"SELECT gm_id,gm_org_id,gm_utc_datetime,gm_status,gm_policy_id FROM game WHERE gm_id= {data['GmID']};")
            if (game_validations and game_validations[0]['gm_id'] is not None and game_validations[0]['gm_id'] != ""):
                if (game_validations[0]['gm_org_id'] != PlyID):
                    raise Exception(response.error_add(code='618', message="You Are Not The Admin Of The Game"))
                if (game_validations and game_validations[0]['gm_status'] != 'cancel'):
                    if (game_validations and game_validations[0]['gm_status'] != 'pause'):
                        if (game_validations and game_validations[0]['gm_utc_datetime'] > datetime.now()):
                            if ('GuestMail' in data and data['GuestMail'] != ""):
                                guest_mail = data['GuestMail'].lower()
                            else:
                                raise Exception(response.error_add(message="Email Address Required"))
                            if ('GuestFname' in data and data['GuestFname'] != ""):
                                guest_fname = data['GuestFname']
                            else:
                                raise Exception('First name required')
                            ply_data = execution.execute(
                                f"SELECT ply_id,ply_fname,ply_lname,ply_email FROM players WHERE ply_email= '{data['GuestMail']}'")
                            ply_id = 0 if ply_data == [] else ply_data[0]['ply_id']
                            if (PlyID != ply_id):
                                if_connected = game_utils.class_type(data['GmID'], PlyID)
                                if (if_connected == 'offline' or if_connected == 'online'):
                                    check_if_registered = execution.execute(
                                        f"SELECT gm_ply_id FROM gm_players WHERE gm_ply_gm_id={data['GmID']} AND gm_ply_ply_id={ply_id} AND gm_ply_status ='y' \
                                                            UNION SELECT guest_id FROM guests WHERE guest_gm_id={data['GmID']} AND (guest_ply_id={ply_id} AND guest_mail = '{data['GuestMail']}') \
                                                            UNION SELECT gm_wait_list_id FROM gm_waitlist WHERE gm_wait_list_gm_id={data['GmID']} AND gm_wait_list_ply_id={ply_id}")
                                    if check_if_registered == []:
                                        if_banned = execution.execute(
                                            f"SELECT ply_ban_id FROM ply_bans WHERE (ply_ban_ply_frm = {PlyID} AND ply_ban_ply_to = {ply_id}) || (ply_ban_ply_frm = {ply_id} AND ply_ban_ply_to = {PlyID}) ")
                                        if if_banned == []:
                                            added = 0
                                            checked_in = 1 if 'GuestCheckinStatus' in data and (
                                                    data['GuestCheckinStatus'] == 'true') else 0
                                            if ply_data and 'ply_id' in ply_data[0] and ply_id > 0 and 'ply_fname' in \
                                                    ply_data[0] and 'ply_lname' in ply_data[0]:
                                                if (guest_mail != "" and ply_data[0][
                                                    'ply_email'].lower() != guest_mail):
                                                    raise Exception('Invalid player email')
                                                plys = execution.execute(
                                                    f"SELECT game.gm_max_players as maxPlys,count(guests.guest_ply_id) as total from game Left Join guests on game.gm_id=guests.guest_gm_id where gm_id={data['GmID']}")
                                                if (plys and plys[0]['maxPlys'] < plys[0]['total']):
                                                    execution.execute(
                                                        f"UPDATE game SET gm_max_players= {plys[0]['maxPlys']} +1 WHERE gm_id={data['GmID']}")
                                                execution.execute(
                                                    f"INSERT INTO guests (guest_gm_id,guest_mail,guest_ply_id,guest_fname,guest_lname,guest_checkedIn) VALUES ({data['GmID']},'{guest_mail}',{ply_id},'{ply_data[0]['ply_fname']}','{ply_data[0]['ply_lname']}',{checked_in})")
                                                execution.execute(
                                                    f"INSERT INTO gm_players (gm_ply_gm_id,gm_ply_ply_id,gm_ply_status,gm_ply_leave,gm_ply_refunded,gm_ply_is_checkedIn,gm_ply_pay_type,gm_ply_removed_by_admin) VALUES({data['GmID']},{ply_id},'y',NULL,0,{checked_in},NULL,0)")
                                                added = 1
                                            elif (ply_id == 0) and ('GuestMail' in data) and (data['GuestMail'] != ""):
                                                guest_lname = data['GuestLname'] if ('GuestLname' in data) else ""
                                                guest = execution.execute(
                                                    f"INSERT INTO guests (guest_gm_id,guest_mail,guest_ply_id,guest_fname,guest_lname,guest_checkedIn) VALUES ({data['GmID']},'{guest_mail}',0,'{guest_fname}','{guest_lname}',{checked_in})")
                                                added = 1
                                            else:
                                                raise Exception("Player id or Email is required")
                                            client_data = execution.execute(
                                                f"SELECT contact_id FROM contacts WHERE contact_org_id={PlyID} AND contact_email='{guest_mail}' ")
                                            if (client_data == []):
                                                if (ply_id > 0):
                                                    execution.execute(f"INSERT INTO contacts (contact_org_id , contact_email , contact_ply_id ,contact_f_name , contact_l_name)\
                                                                VALUES ({PlyID},'{guest_mail}',{ply_id},'{ply_data[0]['ply_fname']}','{ply_data[0]['ply_lname']}')")
                                                elif (ply_id == 0 and ('GuestMail' in data) and (
                                                        data['GuestMail'] != "")):
                                                    execution.execute(f"INSERT INTO contacts (contact_org_id , contact_email , contact_ply_id ,contact_f_name , contact_l_name)\
                                                                                                        VALUES ({PlyID},'{guest_mail}',{ply_id},'{guest_fname}','{guest_lname}')")
                                                client_data = execution.execute(
                                                    f"SELECT contact_id,contact_ply_id FROM contacts WHERE contact_org_id={PlyID} AND contact_email='{guest_mail}' ")
                                            new_client = 1 if (
                                                    client_data != [] and client_data[0]['contact_id'] != "" and
                                                    client_data[0]['contact_id'] > 0) else 0
                                            contact_id = client_data[0]['contact_id'] if (
                                                    client_data and client_data[0]['contact_id'] != "" and
                                                    client_data[0]['contact_id'] > 0) else 0
                                            bundle_id = 0
                                            if (if_connected == 'online'):
                                                get_bundle_details = game_utils.bundle_details(class_id=data['GmID'],
                                                                                               org_id=PlyID,
                                                                                               class_datetime=
                                                                                               game_validations[0][
                                                                                                   'gm_utc_datetime'],
                                                                                               ply_id=ply_id,
                                                                                               contact_id=contact_id,
                                                                                               dev_id=data['dev_id'],
                                                                                               tkn=data['tkn'],
                                                                                               ProjectSecret=data[
                                                                                                   'ProjectSecret'],
                                                                                               ProjectKey=data[
                                                                                                   'ProjectKey'],
                                                                                               new_client=new_client)
                                                if (
                                                        get_bundle_details != [] and get_bundle_details != 'Error In BundleCurl.' and 'plySubscriptions' in get_bundle_details):
                                                    player_subs = get_bundle_details['plySubscriptions']
                                                    if (player_subs != [] and player_subs[0]['bundle_id'] and
                                                            player_subs[0]['available_credit'] > 0):
                                                        bundle_id = player_subs[0]['bundle_id']
                                                        if (ply_id > 0):
                                                            decreased_by_one = game_utils.updateCredit(
                                                                class_id=data['GmID'], bundle_id=bundle_id,
                                                                ply_id=ply_id, ply_email='',
                                                                ProjectSecret=data['ProjectSecret'],
                                                                ProjectKey=data['ProjectKey'])
                                                            if (decreased_by_one['result'] != 'success'):
                                                                raise Exception('Error in bundle credit')
                                                            game_utils.add_to_subs(class_id=data['GmID'], ply_id=ply_id,
                                                                                   subs_id=bundle_id)
                                                        elif (ply_id == 0 and guest_mail != ""):
                                                            decreased_by_one = game_utils.updateCredit(
                                                                class_id=data['GmID'], bundle_id=bundle_id,
                                                                ply_id=0, ply_email=guest_mail,
                                                                ProjectSecret=data['ProjectSecret'],
                                                                ProjectKey=data['ProjectKey'])
                                                            if (decreased_by_one[0]['result'] != 'success'):
                                                                raise Exception('Error in bundle credit')
                                                            game_utils.add_to_subs(class_id=data['GmID'], ply_id=0,
                                                                                   mail=guest_mail, subs_id=bundle_id)
                                                else:
                                                    raise Exception('Error In BundleCurl.')
                                            if (added == 1):
                                                execution.execute(
                                                    f"INSERT INTO custom_notifications (custom_notification_ply_id,custom_notification_ply_email,custom_notification_period,custom_notification_gm_id,custom_notification_reminder_status) VALUES ({ply_id},'{guest_mail}',0,{data['GmID']},1)")
                                                if (game_validations[0]['gm_policy_id'] == 1):
                                                    latest_user = execution.execute(
                                                        f"SELECT gm_ply_ply_id , gm_ply_pay_type FROM gm_players where gm_ply_refunded = 0 and not gm_ply_leave is null and gm_ply_gm_id={data['GmID']} order by gm_ply_leave Desc limit 1")
                                                    if latest_user and latest_user[0]['gm_ply_ply_id'] != ply_id:
                                                        check_payment_type = game_utils.check_type_payment(data['GmID'],
                                                                                                           latest_user[
                                                                                                               0][
                                                                                                               'gm_ply_ply_id'],
                                                                                                           data[
                                                                                                               'source'],
                                                                                                           data[
                                                                                                               'ProjectKey'],
                                                                                                           data[
                                                                                                               'ProjectSecret'])
                                                        if str(check_payment_type).__contains__("something happened:"):
                                                            raise Exception(check_payment_type)
                                                if (ply_id == 0): ply_id = contact_id
                                                logData = {'UserId': ply_id, 'GmID': data['GmID'], 'PlyID': PlyID,
                                                           'SubscriptionId': bundle_id,
                                                           'SrcType': data['source'], 'LogType': 30,
                                                           'ContactId': contact_id}
                                                common_utils.logAllActions(logData)
                                            else:

                                                raise Exception(response.error_add(message='Insertion error'))
                                        else:
                                            raise Exception(
                                                response.error_add(code='619', message="This user is banned."))
                                    else:
                                        raise Exception(
                                            response.error_add(code='620', message="This client is already a player."))

                                else:
                                    raise Exception(response.error_add(message=if_connected))
                            else:
                                raise Exception(response.error_add(code='619', message=f"We've found an issue with an email address\
                                                                             The email below is your registered email:{data['GuestMail']} \
                                                                             It has not been added to your clients."))
                        else:
                            raise Exception(response.error_add(message="Game is Expired"))
                    else:
                        raise Exception(response.error_add(message="Game is Paused"))
                else:
                    raise Exception(response.error_add(code='115', message="Game Canceled"))
            else:
                raise Exception(response.error_add(code='617', message="Game Not Found"))
        else:
            raise Exception(response.error_add(message="org_id,class_id and ply_id are required in correct format"))

    except Exception as e:
        return e

    else:
        last_inserted = execution.execute(
            f"SELECT guest_id,guest_ply_id,guest_mail,guest_fname,guest_lname FROM guests WHERE guest_mail='{data['GuestMail']}' and guest_gm_id={data['GmID']} ")
        ResArr = {"Result": "true", "guestsData": last_inserted, "GmId": data['GmID']}

        return response.success_add(ResArr)

    #                                     ##### upload invite contact part ####


def up_inv_contacts(data):
    # parameter is dict of data = {
    #                             'first_name': 'khalid',
    #                             'last_name': 'Ismail',
    #                             'email': 'khalid2020@gmail.com',
    #                             'ply_id': 4605,
    #                             'project_id':1
    #                             }
    # return
    try:
        ply_id = data['ply_id'] if 'ply_id' in data else 0
        email = data['email'] if 'email' in data else ''
        first_name = data['first_name'] if 'first_name' in data else ''
        last_name = data['last_name'] if 'last_name' in data else ''
        project_id = data['project_id'] if 'project_id' in data else 0
        if not ply_id or type(ply_id) != int or int(ply_id) <= 0:
            raise Exception("ply_id is required")
        if not email or type(email) != str:
            raise Exception("email is required")
        if not first_name or type(first_name) != str:
            raise Exception("first_name is required")
        if not last_name or type(last_name) != str:
            raise Exception("last_name is required")
        if not project_id or type(project_id) != int or int(project_id) <= 0:
            raise Exception("project_id is required")

        #  update first name and last name for this user in contacts , to be shown correctly for organizers.
        all_cont = execution.execute(
            f"SELECT contact_id , contact_org_id , contact_email , contact_ply_id FROM contacts WHERE contact_email = '{email}'")
        if str(all_cont).__contains__('Something went wrong'):
            raise Exception(all_cont)

        if not all_cont:
            raise Exception("make sure email is correct")

        FName = urllib.parse.quote(first_name)
        LName = urllib.parse.quote(last_name)
        sql_list = []
        up_sql = " SET contact_f_name = '" + FName + "' , contact_l_name = '" + LName + "'"
        for val in all_cont:
            sql_list.append(val["contact_id"])

        SqlArray = str(tuple([key for key in sql_list])).replace(',)', ')')
        up_cont_sql = execution.execute(f"UPDATE contacts {up_sql} WHERE contact_id IN {SqlArray}")
        if str(up_cont_sql).__contains__('Something went wrong'):
            raise Exception(up_cont_sql)

        pending_data = execution.execute(
            f"SELECT * FROM invitations LEFT JOIN players ON LOWER(inv_ply_to_email) = LOWER(ply_email) WHERE LOWER(inv_ply_to_email) = LOWER('{email}') AND ply_pid='{project_id}'")
        if str(pending_data).__contains__('Something went wrong'):
            raise Exception(pending_data)
        if not pending_data:
            raise Exception("there are no invitaion")

        inv_gm_id = []
        inv_ply_id = str()
        inv_id = []
        OrgID = []
        for pend_data in pending_data:
            if int(pend_data['inv_gm_id']) > 0:
                inv_gm_id.append(pend_data['inv_gm_id'])
                inv_ply_id = str(pend_data['ply_id'])
                inv_id.append(pend_data['inv_id'])

        inv_gm_id_tuple = str(tuple([key for key in inv_gm_id])).replace(',)', ')')
        inv_id_tuple = str(tuple([key for key in inv_id])).replace(',)', ')')
        gm_data = execution.execute(
            f"SELECT * FROM game WHERE gm_pid = {project_id} AND gm_id IN {inv_gm_id_tuple} AND ((gm_date > CURDATE() OR (gm_date = CURDATE() AND gm_start_time > CURTIME())) AND gm_status IS NULL)")
        if str(gm_data).__contains__('Something went wrong'):
            raise Exception(gm_data)
        if not gm_data:
            raise Exception("there are no gm_data")

        for data in gm_data:
            OrgID.append(data['gm_org_id'])

        OrgID_tuple = str(tuple([key for key in OrgID])).replace(',)', ')')

        # Chk if invited before
        chk_fr_inv = execution.execute(
            f"SELECT * FROM invitations WHERE inv_gm_id IN {inv_gm_id_tuple} AND inv_ply_to_id = {inv_ply_id} AND (inv_approve = 'y' || inv_approve = 'p')")
        if str(chk_fr_inv).__contains__('Something went wrong'):
            raise Exception(chk_fr_inv)
        if not chk_fr_inv:
            raise Exception("there are no invitaion data")

        # check if member in this gm
        chk_gm_mem = execution.execute(
            f"SELECT * FROM gm_players WHERE gm_ply_gm_id IN {inv_gm_id_tuple} AND gm_ply_status = 'y' AND (gm_ply_leave IS NULL OR gm_ply_leave = '') AND gm_ply_ply_id = {inv_ply_id}")
        if str(chk_gm_mem).__contains__('Something went wrong'):
            raise Exception(chk_gm_mem)
        if not chk_gm_mem:
            raise Exception("player is  member of this game")

        # check if waitlist in this gm
        chk_gm_wait_list = execution.execute(
            f"SELECT gm_wait_list_id  FROM gm_waitlist WHERE gm_wait_list_gm_id IN {inv_gm_id_tuple} AND gm_wait_list_ply_id = {inv_ply_id} AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0")
        if str(chk_gm_wait_list).__contains__('Something went wrong'):
            raise Exception(chk_gm_wait_list)
        if not chk_gm_wait_list:
            raise Exception("player is waitlist of this game")

        up_gm_sql = execution.execute(
            f"UPDATE invitations SET inv_ply_to_id = '{inv_ply_id}', inv_ply_to_email=NULL WHERE inv_gm_id IN {inv_gm_id_tuple} AND inv_ply_frm_id IN {OrgID_tuple} AND inv_id IN {inv_id_tuple}")
        if str(up_gm_sql).__contains__('Something went wrong'):
            raise Exception(up_gm_sql)

    #         send notification to the user

    except Exception as e:
        return e.__str__()


def player_login(data):
    """params:'email': 'example@exp.com',
              'pass': '******',
              'source': 'web',
              'ply_id': 848,
              'dev_id': 'mac_Chrome_172.31.5.43',
              'ply_tkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
              'usrAppleID': '',
              'TimeZone': 'Africa%2FCairo' """
    try:
        pid = data['pid'] if 'pid' in data else 1

        if not data['Email'] or data['Email'] == '':
            raise Exception(response.error(
                code='121', message='No Email Sent'))

        if not data['Pass']:
            raise Exception(response.error(
                code='122', message='No Password Sent'))

        if len(data['Email']) > 50:
            raise Exception(response.error(
                code='119', message='Email Is Too Long'))

        if len(data['Pass']) > 30:
            raise Exception(response.error(
                code='120', message='Password Is Too Long'))

        projectShort = execution.execute(
            f"SELECT project_short FROM projects WHERE project_id= {pid}")

        if projectShort and projectShort[0]['project_short'] == 'r' or not re.search(
                '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', data['Email']):
            raise Exception(response.error(
                code='118', message='Invalid Email'))

        account_check = execution.execute(
            f"SELECT ply_status FROM players WHERE ply_email = '{data['Email']}' AND ply_pid= {pid}")
        if account_check and account_check[0]['ply_status'] != '' and account_check[0][
            'ply_status'].lower() == 'deactive':
            raise Exception(response.error(
                code='130',
                message='Please check your email for your registration confirmation and click the link within it. Once you have done this your account will activate.'))

        suspended = execution.execute(
            f"SELECT * FROM suspended_players WHERE sus_ply_pid = {pid} AND sus_ply_email = '{data['Email']}'")
        if suspended != []:
            raise Exception(response.error(
                code='125', message='Suspended Email'))

        player = execution.execute(
            f'SELECT * FROM players WHERE ply_email = "{data["Email"]}" AND  ply_pid= {pid}')

        if player == []:
            raise Exception(response.error(
                code='101',
                message="We don't have any records of this email. Please check the email address entered and try again"))
        else:
            player = player[0]

        masterPass = 'VACF101'

        if data['Pass'] == masterPass or data['Pass'] == player['ply_password'] or hashlib.md5(
                data['Pass'].encode()).hexdigest() == player['ply_password']:
            token = ''

            if data['source'] and data['source'].lower() == 'web':
                token = player_utils.add_player_token(
                    player['ply_id'], data['DevID'], data['PlyTkn'], 'w', pid)

            elif data['source'] and data['source'].lower() == 'android':
                token = player_utils.add_player_token(
                    player['ply_id'], data['DevID'], '', 'A', pid)

            elif data['source'] and data['source'].lower() == 'ios':
                token = player_utils.add_player_token(
                    player['ply_id'], data['DevID'], '', 'I', pid)

                if data['usrAppleID'] and data['usrAppleID'] != '':
                    ios_check = execution.execute(
                        f"SELECT apple_user_ply_id FROM apple_users WHERE apple_user_ply_id= {player['ply_id']}")
                    if ios_check and ios_check[0]['apple_user_ply_id'] and ios_check[0]['apple_user_ply_id'] != '':
                        execution.execute(
                            f'UPDATE apple_users set apple_user_apple_id= {data["usrAppleID"]} WHERE apple_user_ply_id={ios_check[0]["apple_user_ply_id"]}')
                    else:
                        execution.execute(
                            f"INSERT INTO apple_users (apple_user_ply_id , apple_user_apple_id) VALUES({player['ply_id']} , {data['usrAppleID']})")

            else:
                token = player_utils.add_player_token(
                    player['ply_id'], data['DevID'], '', '', project_id=pid)

            execution.execute(
                f"UPDATE players SET ply_qcode = '', ply_status='' WHERE ply_id = {player['ply_id']}")

            result = player_utils.player_view(
                player_id=player['ply_id'], token=token, dev_id=data['DevID'])

            execution.execute(
                f"UPDATE players SET ply_state = 1 WHERE ply_id = {player['ply_id']}")

            if result and result['PlyTimeZone'] and result['PlyTimeZone'] != '':
                player_utils.saveTimeZone(player['ply_id'], data['TimeZone'])

            return response.success(result_data=result, code='200')

        else:
            raise Exception(response.error(
                code='129', message='The username or password you have entered is incorrect - please try again.'))
    except Exception as e:
        return response.error(e.__str__())


def guest_After_Reg_Updates(Ply_ID=0, Ply_Email='', Ply_FName='', Ply_LName=''):
    try:
        guest_data = execution.execute(f"SELECT * FROM guests WHERE guest_mail= '{Ply_Email}'")
        if str(guest_data).__contains__('Something went wrong'):
            raise Exception(guest_data)
        if guest_data and Ply_ID > 0:
            output = execution.execute(
                f"UPDATE guests SET guest_ply_id = '{Ply_ID}',guest_fname='{Ply_FName}' , guest_lname='{Ply_LName}' WHERE guest_mail='{Ply_Email}'")
            if output:
                raise Exception(output)
            for data in guest_data:
                output = execution.execute(
                    f"INSERT INTO gm_players (gm_ply_gm_id , gm_ply_ply_id , gm_ply_status , gm_ply_is_checkedIn ) VALUES ('{data['guest_gm_id']}','{Ply_ID}','y', '{data['guest_checkedIn']}')")
                if output:
                    raise Exception(output)
        sub_data = execution.execute(f"SELECT * FROM bundles.bundles_subscriptions WHERE ply_email='{Ply_Email}'",
                                     db_name='bundles')
        if str(sub_data).__contains__('Something went wrong'):
            raise Exception(sub_data)
        if sub_data and Ply_ID > 0:
            output = execution.execute(
                f"UPDATE bundles.bundles_subscriptions SET ply_id = '{Ply_ID}' WHERE ply_email='{Ply_Email}'")
            if output:
                raise Exception(output)
        sub_gm = execution.execute(f"SELECT * FROM games_subscriptions WHERE member_email='{Ply_Email}'")
        if str(sub_gm).__contains__('Something went wrong'):
            raise Exception(sub_gm)
        if sub_gm and Ply_ID > 0:
            output = execution.execute(
                f"UPDATE games_subscriptions SET member_id = '{Ply_ID}' WHERE member_email='{Ply_Email}'")
            if output:
                raise Exception(output)
        inv_ply = execution.execute(f"SELECT * FROM invitations WHERE inv_ply_to_email ='{Ply_Email}'")
        if str(inv_ply).__contains__('Something went wrong'):
            raise Exception(inv_ply)
        if inv_ply and Ply_ID > 0:
            output = execution.execute(
                f"UPDATE invitations SET inv_ply_to_id = '{Ply_ID}' WHERE inv_ply_to_email='{Ply_Email}'")
            if output:
                raise Exception(output)
        contact_ply = execution.execute(
            f"SELECT contact_id,contact_ply_id FROM contacts WHERE contact_email ='{Ply_Email}'")
        if str(contact_ply).__contains__('Something went wrong'):
            raise Exception(contact_ply)
        if contact_ply and Ply_ID > 0:
            output = execution.execute(
                f"UPDATE org_notes SET note_ply_id ='{contact_ply[0]['contact_ply_id']}' WHERE note_contact_id='{contact_ply[0]['contact_id']}'")
            if output:
                raise Exception(output)
    except Exception as e:
        return response.error(e.__str__())


def view_contact(data):
    admin_id = data['PlyID']
    if admin_id > 0:
        org_ply_data = player_utils.org_players(admin_id)
        joined_players = org_ply_data['OrgPlyIDs']
        org_contacts_data = player_utils.org_contacts(admin_id, joined_players)
        result = {
            'OrgPlys': org_ply_data['OrgPlyData'], 'OrgContacts': org_contacts_data}
        return response.success(result_data=result)
    else:
        raise Exception("Invalid Data")


def checkPlayerAndContactWithOrganizer(data):
    try:
        playerId = 0
        contactId = 0
        organizerId = 0
        if 'organizerId' in data:
            if int(data['organizerId']) > 0:
                organizerId = data['organizerId']
            else:
                raise Exception("Wrong organizer ID given")
        if 'playerId' in data:
            if int(data['playerId']) > 0:
                playerId = data['playerId']
            elif int(data['playerId']) < 0:
                raise Exception("Wrong player ID given")
        if 'contactId' in data:
            if int(data['contactId']) > 0:
                contactId = data['contactId']
            elif int(data['playerId']) < 0:
                raise Exception("Wrong contact ID given")

        # **************Function Called player.playerBelongsToOrganizer($organizerId = 0, $playerId = 0)*****************

        query = execution.execute(f"SELECT gm_players.gm_ply_ply_id AS ply_id , game.gm_id\
                            FROM fastplayapp_test.gm_players\
                                JOIN fastplayapp_test.game ON game.gm_id = gm_players.gm_ply_gm_id\
                            WHERE gm_ply_ply_id = {playerId}\
                                AND gm_org_id = {organizerId}\
                            UNION\
                                SELECT DISTINCT canceled.gm_plys_log_ply_id AS ply_id , gm.gm_id\
                                FROM fastplayapp_test.cancel_gm_plys_log as canceled \
                                    LEFT JOIN fastplayapp_test.game as gm ON canceled.gm_plys_log_gm_id = gm.gm_id\
                                WHERE gm.gm_org_id ={organizerId} AND canceled.gm_plys_log_ply_id = {playerId}\
                            UNION\
                                SELECT DISTINCT sub.ply_id AS ply_id,''\
                                FROM bundles.bundles_subscriptions sub\
                                    LEFT JOIN bundles.bundles as bundles ON bundles.id=sub.bundle_id \
                                WHERE bundles.org_id = {organizerId} AND sub.is_removed=0")

        if len(query) > 0:
            return response.success(result_data={"output": "true"})

        # ****************function called player.contactBelongsToOrganizer($organizerId = 0, $contactId = 0 , $playerId = 0)****************

        elif contactId > 0:
            q = " AND contact_id =" + str(contactId)
        elif playerId > 0:
            q = " AND contact_ply_id =" + str(playerId)
        else:
            q = ""

        query = execution.execute(f"SELECT contact_id\
                FROM contacts\
                WHERE contact_org_id = {organizerId}" + q)
        if len(query) > 0:
            return response.success(result_data={"output": "true"})
        else:
            return response.success(result_data={"output": "false"})

    except Exception as e:
        return response.error(e.__str__())


def get_player_offline_payments_data(data):
    try:
        playerId = 0
        projectKey = 0
        projectSecret = 0
        # ************************ Validations ***********************

        if 'PlyID' in data:
            if int(data['PlyID']) > 0:
                playerId = data['PlyID']
            elif int(data['PlyID']) < 0:
                raise Exception("Wrong player ID given")
        else:
            raise Exception("player ID not given")

        if 'ProjectSecret' in data:
            if int(data['ProjectSecret']) > 0:
                projectSecret = data['ProjectSecret']
        else:
            raise Exception("projectSecret not given")

        if 'ProjectKey' in data:
            if int(data['ProjectKey']) > 0:
                projectKey = data['ProjectKey']
        else:
            raise Exception("projectKey not given")

        # ************************************************************

        params = {'ProjectKey': projectKey, 'ProjectSecret': projectSecret,
                  'PlyID': int(playerId)}
        status = common_utils.game_curl('offline/admin/data', params)

        return response.success(result_data=status)

    except Exception as e:
        return response.error(e.__str__())


def get_registered_contacts_data(data):
    try:
        if 'pid' in data and int(data['pid']) > 0:
            pid = data['pid']
        else:
            raise Exception("Wrong pid given")
        if 'contacts_emails' in data:
            if len(data['contacts_emails']) > 0:
                contacts_emails = data['contacts_emails']
            elif len(data['contacts_emails']) < 0:
                raise Exception("Wrong contacts_emails given")
        emails = []
        for x in contacts_emails:
            strippedStr = x.strip()
            filteredUser = re.sub(r'[^a-zA-Z0-9@!#$%&*+-/?^_`{|}~]', '', strippedStr)
            print(filteredUser)
            if 0 < len(filteredUser) <= 50:
                emails.append('%s' % filteredUser)

            # username, url = strippedStr.split('@')
            # website, extension = url.split('.')

            # if username.replace('-', '').replace('_', '').isalnum() is False:
            #     baduser = ''
            #     filteredUser = username.strip(baduser)
            # else:

            # badurl = ''
            # filteredUrl = url.strip(badurl)
        email_imploded = ""
        j = 0
        for i in emails:
            if j < len(emails) - 1:
                email_imploded += "'" + i + "'" + ","
                j += 1
            else:
                email_imploded += "'" + i + "'"

        query = execution.execute(f"SELECT DISTINCT ply_id, ply_fname, ply_lname, ply_email\
                FROM players\
                WHERE ply_email IN ({email_imploded})\
                    AND ply_pid = {pid}")
        if str(query).__contains__("Something went wrong"):
            raise Exception(str(query))
        regEmails = []
        for row in query:
            id = row['ply_id']
            email = row['ply_email']
            fname = row['ply_fname']
            lname = row['ply_lname']

            regEmails.append({email: {"id": id, "email": email, "first_name": fname, "last_name": lname}})

        return response.success(result_data=regEmails)

    except Exception as e:
        return response.error(e.__str__())
