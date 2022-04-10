from cgi import print_directory
import hashlib
import re
import urllib
from datetime import datetime
from urllib import parse

import pytz

from database import response, execution
from database.config import s3_bucket_url
from utils import game_utils


def get_player_flags(game_id, player_id):
    """"
    desc: get game flags and checks(boolean values) that used in game_view
    input: game_id
    output: result[OrgMem,DisOrg,ReqGm,InvGm,MemGm,PlyStatus,IsPly,RequestedBefore]
    """
    try:
        if not game_id or not player_id or int(game_id) < 0 or int(player_id) < 0:
            raise Exception("game and player id required")
        else:
            PlyStatus = 'No'
            IsPly = 'n'
            RequestedBefore = 'n'
            check = execution.execute(
                f"SELECT gm_ply_id FROM gm_players WHERE gm_ply_gm_id ={game_id} and gm_ply_ply_id={player_id}")
            if str(check).__contains__('Something went wrong'):
                raise Exception(check)
            OrgMem = True if check != [] and check[0]['gm_ply_id'] != '' else False
            invitedToGm = execution.execute(
                f"SELECT inv_id FROM invitations WHERE inv_gm_id = {game_id} AND inv_ply_to_id ={player_id} AND inv_approve = 'y' LIMIT 1, 0;")
            if str(invitedToGm).__contains__('Something went wrong'):
                raise Exception(invitedToGm)
            InvGm = True if invitedToGm != [] and invitedToGm[0]['inv_id'] > 0 else False
            wait = execution.execute(
                f"SELECT gm_wait_list_id FROM gm_waitlist WHERE gm_wait_list_gm_id={game_id} and gm_wait_list_ply_id={player_id}")
            if str(wait).__contains__('Something went wrong'):
                raise Exception(wait)
            if wait != [] and wait[0]['gm_wait_list_id'] != '':
                PlyStatus = 'Wait'
            inv = execution.execute(
                f"SELECT inv_id FROM invitations WHERE inv_gm_id={game_id} and inv_ply_to_id={player_id}")
            if str(inv).__contains__('Something went wrong'):
                raise Exception(inv)
            if inv != [] and inv[0]['inv_id'] != '':
                PlyStatus = 'Inv'
            member = execution.execute(
                f"SELECT gm_ply_id FROM gm_players WHERE gm_ply_gm_id ={game_id} AND gm_ply_ply_id = {player_id} AND gm_ply_status = 'y';")
            if str(member).__contains__('Something went wrong'):
                raise Exception(member)
            if member != [] and member[0]['gm_ply_id'] != '':
                PlyStatus = 'Mem'
                IsPly = 'y'
            gm_recurr = execution.execute(f"SELECT gm_recurr_times , gm_recurr_id FROM game WHERE gm_id={game_id}")
            if str(gm_recurr).__contains__('Something went wrong'):
                raise Exception(gm_recurr)
            if gm_recurr != [] and gm_recurr[0]['gm_recurr_times'] == 1 and gm_recurr[0]['gm_recurr_id'] == 0:
                gm_parent = execution.execute(
                    f"SELECT gm_id FROM gm_players AS gm INNER JOIN game AS g ON gm.gm_ply_gm_id=g.gm_id WHERE gm_ply_ply_id={player_id} AND g.gm_recurr_id={game_id}")
                if str(gm_parent).__contains__('Something went wrong'):
                    raise Exception(gm_parent)
                if gm_parent and gm_parent[0]['gm_id'] != '':
                    RequestedBefore = 'y'
            elif gm_recurr != [] and gm_recurr[0]['gm_recurr_times'] == 0 and gm_recurr[0]['gm_recurr_id'] > 0:
                gm_child = execution.execute(
                    f"SELECT gm_id FROM gm_players AS gm INNER JOIN game AS g ON gm.gm_ply_gm_id=g.gm_id WHERE gm_ply_ply_id={player_id} AND g.gm_recurr_id={gm_recurr[0]['gm_recurr_id']}")
                if str(gm_child).__contains__('Something went wrong'):
                    raise Exception(gm_child)
                if gm_child and gm_child[0]['gm_id'] != '':
                    RequestedBefore = 'y'

            return {'OrgMem': OrgMem, 'InvGm': InvGm, 'PlyStatus': PlyStatus, 'IsPly': IsPly,
                    'RequestedBefore': RequestedBefore}

    except Exception as e:
        return e.__str__()


def get_players_count_in_game(game_id):
    try:
        GmPlys = 0
        GmPlysWhere = ""
        # get all guests then count all the players who are not in guest table.

        AllGuests = execution.execute(
            f"SELECT guest_ply_id FROM guests WHERE guest_ply_id !=0 AND guest_gm_id = {game_id}")
        if AllGuests.__contains__("Something went wrong: "):
            raise Exception(AllGuests)
        if AllGuests:
            GmPlysWhere = " AND gm_ply_ply_id NOT IN ("
            for dicts in AllGuests:
                if dicts['guest_ply_id'] == AllGuests[len(AllGuests) - 1]['guest_ply_id']:
                    GmPlysWhere = GmPlysWhere + str(dicts['guest_ply_id']) + ')'
                else:
                    GmPlysWhere = GmPlysWhere + str(dicts['guest_ply_id']) + ','
        GmPlysRow = execution.execute(
            f" SELECT COUNT(gm_ply_ply_id) AS GmPlys FROM gm_players WHERE gm_ply_status = 'y' AND gm_ply_gm_id ={game_id} {GmPlysWhere}")
        if GmPlysRow.__contains__("Something went wrong: "):
            raise Exception(GmPlysRow)
        if GmPlysRow:
            GmPlys = GmPlysRow[0]['GmPlys']
        GmGsts = 0
        GmGstsRow = execution.execute(f"SELECT COUNT(guest_gm_id) AS guestsNum FROM guests WHERE guest_gm_id={game_id}")
        if GmGstsRow.__contains__("Something went wrong: "):
            raise Exception(GmGstsRow)
        if GmGstsRow:
            GmGsts = GmGstsRow[0]['guestsNum']
        return GmPlys + GmGsts
    except Exception as e:
        return e.__str__()


def can_player_withdraw_from_game(game_id, player_id):
    try:
        game_data = execution.execute(
            f"SELECT gm_min_players,gm_date,gm_start_time,gm_org_id FROM game WHERE gm_id={game_id}")
        if str(game_data).__contains__('Something went wrong'):
            raise Exception(game_data)
        if not game_data:
            raise Exception('not found')
        if game_data[0]["gm_org_id"] == player_id:
            return True

        game_datetime = datetime.strptime(f"{game_data[0]['gm_date']} {game_data[0]['gm_start_time']}",
                                          '%Y-%m-%d %H:%M:%S')
        players_count = get_players_count_in_game(game_id)
        time_diff = datetime.now() - game_datetime
        days, seconds = time_diff.days, time_diff.seconds
        hours = days * 24 + seconds
        if hours <= 24 and days < 1:
            return True if players_count == game_data[0]["gm_min_players"] else False
        else:
            return False
    except Exception as e:
        return e.__str__()


# function to return array of gcm tokens of the Android users

def android_players_regs(project_id, player_id):
    register_array = []
    player_data = execution.execute(
        f"SELECT ply_tkn_gcm_reg FROM ply_tkn_gcm WHERE ply_tkn_gcm_pid = {project_id} AND  ply_tkn_gcm_ply_id = {player_id} AND ply_tkn_gcm_source = 'I' AND ply_tkn_gcm_token != '' order by updated desc"
    )
    if player_data and player_data.count() > 0:
        for player_data_row in player_data:
            register_array.append(player_data_row['ply_tkn_gcm_reg'])

    return register_array


# function to return array of gcm tokens of the Web users

def web_players_regs(project_id, player_id):
    register_array = []
    player_data = execution.execute(
        f"SELECT ply_tkn_gcm_reg FROM ply_tkn_gcm WHERE ply_tkn_gcm_pid = {project_id} AND  ply_tkn_gcm_ply_id = {player_id} AND ply_tkn_gcm_source = 'w' AND ply_tkn_gcm_token != '' AND ply_tkn_gcm_reg != '' order by updated desc"
    )
    if player_data and len(player_data) > 0:
        for player_data_row in player_data:
            register_array.append(player_data_row['ply_tkn_gcm_reg'])

    return register_array


# function to return array of gcm tokens of the IOS users

def ios_players_regs(project_id, player_id):
    register_array = []
    player_data = execution.execute(
        f"SELECT ply_tkn_gcm_reg FROM ply_tkn_gcm WHERE ply_tkn_gcm_pid = {project_id} AND  ply_tkn_gcm_ply_id = {player_id} AND ply_tkn_gcm_source = 'I' AND ply_tkn_gcm_token != '' order by updated desc"
    )
    if player_data and player_data.count() > 0:
        for player_data_row in player_data:
            register_array.append(player_data_row['ply_tkn_gcm_reg'])

    return register_array


def getPlyLastClassesAttendedWithOrganizer(organizerId, playerId, patch_classes, offset):
    player_data = execution.execute(f'''SELECT gm_id, gm_title, gm_date, gm_start_time, gm_utc_datetime,
                (
                    CASE 
                        WHEN (gm_utc_datetime  + INTERVAL gm_end_time MINUTE > CURRENT_TIMESTAMP && gm_ply_status = 'y') THEN 'Registered'
                        WHEN (gm_ply_status = 'y' && gm_ply_is_checkedIn = 1 /*&& gm_status != 'cancel'*/) THEN 'attended'
                        WHEN (gm_ply_status = 'y' && gm_ply_is_checkedIn = 0 /*&& gm_status != 'cancel'*/) THEN 'no show'
                        WHEN (gm_ply_status = 'r' && gm_ply_removed_by_admin = 1) THEN 'removed'
                        WHEN (gm_ply_status = 'r' && gm_ply_removed_by_admin = 0) THEN 'dropped out'
                    END
                ) AS gm_attend_status
                FROM gm_players
                JOIN game ON game.gm_id = gm_players.gm_ply_gm_id
                WHERE gm_ply_ply_id = {playerId}
                AND gm_org_id = {organizerId}

                UNION

                SELECT gm_id, gm_title, gm_date, gm_start_time, gm_utc_datetime,
                (
                    CASE 
                        WHEN (gm_wait_list_withdrew = 0 && gm_wait_list_removed_by_admin = 0) THEN 'Waitlist'
                        WHEN (gm_wait_list_removed_by_admin = 1) THEN 'removed'
                        WHEN (gm_wait_list_withdrew = 1 && gm_wait_list_removed_by_admin = 0) THEN 'dropped out'
                    END
                ) AS gm_attend_status
                FROM gm_waitlist
                JOIN game ON game.gm_id = gm_waitlist.gm_wait_list_gm_id
                WHERE gm_wait_list_ply_id = {playerId}
                AND gm_org_id = {organizerId}

                ORDER BY gm_date DESC, gm_start_time DESC
                LIMIT {patch_classes}
                OFFSET {offset};''')
    contact_data = execution.execute(
        f"SELECT contact_id,contact_ply_id FROM contacts WHERE contact_ply_id ={playerId} AND contact_org_id = {organizerId}")
    contact_classes = []
    if contact_data and contact_data[0]['contact_id'] and contact_data['contact_id'] > 0:
        contact_classes = getContactLastClassesAttendedWithOrganizer(organizerId, contact_data[0]['contact_id'],
                                                                     patch_classes, offset)

    return removeDuplicatedClasses(player_data + contact_classes)


def getContactLastClassesAttendedWithOrganizer(organizerId, contactId, patch_classes, offset):
    data = execution.execute(f'''SELECT gm_id, gm_title, gm_date, gm_start_time, gm_utc_datetime,
                (
                    CASE 
                        WHEN gm_utc_datetime  + INTERVAL gm_end_time MINUTE > CURRENT_TIMESTAMP THEN 'Registered'
                        WHEN (guest_checkedIn = 1) THEN 'attended'
                        WHEN (guest_checkedIn = 0) THEN 'no show'  
                    END
                ) AS gm_attend_status
                FROM guests
                JOIN game ON game.gm_id = guests.guest_gm_id
                JOIN contacts ON guests.guest_mail = contacts.contact_email 
                WHERE gm_org_id = {organizerId}
                AND contacts.contact_id = {contactId}
                AND contacts.contact_org_id = {organizerId}
                ORDER BY gm_date DESC, gm_start_time DESC
                LIMIT {patch_classes}
                OFFSET {offset}''')
    return removeDuplicatedClasses(data)


def removeDuplicatedClasses(classes):
    if (not classes) or classes == []:
        return classes
    results = {}

    for row in classes:
        class_id = int(row['gm_id'])
        results[class_id] = row

    return results


def player_view(player_id=0, token='', dev_id='', project_id=1):
    check_player = execution.execute(
        f'SELECT ply_fname FROM players WHERE  ply_id = {player_id}')
    if not check_player:
        return {}
    player_row = execution.execute(
        f'''SELECT ply_id, ply_fname, ply_lname, ply_email, ply_email_alternative,
        CASE ply_gender WHEN 'm' THEN 'Male' WHEN 'f' THEN 'Female' ELSE '' END AS ply_gender,
        ply_height , ply_h_unit , ply_weight , ply_w_unit ,ply_status,ply_city_id, city_name, typed_city, ply_img,
        ply_header_img,s3_profile,s3_cover,ply_created, country_id , iso, country_name, ply_bio, ply_gc_token,ply_paypal_email,
        ply_email_sett,ply_brithdate_sett,ply_gender_sett,ply_city_sett,ply_view_as,ply_business,ply_website, currencies.currency_id AS plyCurrencyId,
        currencies.currency_name AS plyCurrencyName, currencies.currency_symbol AS plyCurrencySymbol, ply_timezone.timezone AS timezone 
        FROM players  
        LEFT JOIN country ON ply_country_id = country_id
        LEFT JOIN city ON ply_city_id = city_id
        LEFT JOIN currencies ON  currencies.currency_country = CASE WHEN country_id = 235 THEN 'GB' ELSE UPPER(iso) END AND currency_pid = {project_id}  
        LEFT JOIN ply_typed_city ON player_id = ply_id 
        LEFT JOIN ply_timezone ON ply_timezone.player_id = players.ply_id
        WHERE ply_id = {player_id}  AND ply_pid ={project_id}''')
    
    if  player_row==[]:
        return {}
    
    notification_state = 'on'
    
    notif_row = execution.execute(
        f'SELECT notifications_state FROM notifications WHERE notifications_ply_id = {player_id}')[0]
    if (notif_row['notifications_state'] and notif_row['notifications_state'] == 0):
        notification_state = 'off'

    
    # get player image 
    if player_row[0]['s3_profile'] == 1:
        player_row[0]['OrgImg'] = s3_bucket_url + "/upload/ply/" + str(player_row[0]['ply_img'])
        player_row[0]['ply_img'] = str(player_row[0]['ply_img']).replace("profile", "profile/thumb")
        player_row[0]['OrgImgThumb'] = s3_bucket_url + "/upload/ply/" + str(player_row[0]['ply_img'])
    else:
        player_row[0]['OrgImg'] = s3_bucket_url + "/backup/upload/ply/" + str(player_row[0]['ply_img'])
        player_row[0]['OrgImgThumb'] = s3_bucket_url + "/backup/upload/ply/" + str(player_row[0]['ply_img'])
    

    if player_row[0]['s3_cover'] and int(player_row[0]['s3_cover']) == 1:
        header_img = s3_bucket_url + str(player_row[0]['ply_header_img'])
    else:
        header_img = s3_bucket_url + "backup/images/upload/ply/" + str(player_row[0]['ply_header_img'])

    player_payment_data = game_utils.get_ply_verified_methods(player_row[0]["ply_id"])

    #stripe_acc_type = player_payment_data['StripeAccountType']
    #player_dashcode = player_payment_data['PlyHasExpressDashCode']

    if player_payment_data['stripe'] == 'y':
        stripe_admin_conn = 'True'
    else:
        stripe_admin_conn = 'False'

   
    date = str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+'01'
    
    limit = execution.execute(
        f'''SELECT SUM(stripe_payments_system_amount) AS sysTotal FROM stripe_payments
        WHERE stripe_payment_admin_id={player_id}
        AND DATE(stripe_payments_created) <= DATE(CURRENT_DATE)
        AND DATE(stripe_payments_created) >= {date}
        AND stripe_payment_refund_id IS NULL''')
    
    sysToCommission =0
    
    if limit and limit[0] and limit[0]['sysTotal']:
        sysToCommission = limit[0]['sysTotal']
    
    lastGms = LastGm(player_row[0]['ply_id'])
    
    #subscriptions = common_utils.bundle_curl('GetOrgSubscriptions', params)
    #invalidPlayerSubs = common_utils.bundle_curl('GetInvalidPlySubscriptions', params)
    
    #stripeData = RetriveCreditCardData(player_row[0]['ply_id'])
    
    result = {'PlyID' : player_row[0]['ply_id'],
              'PlyFname' : urllib.parse.quote(player_row[0]['ply_fname'])if player_row[0]['ply_fname'] else "",
              'PlyLname': urllib.parse.quote(player_row[0]['ply_lname'])if player_row[0]['ply_lname'] else "",
              'PlyEmail' :player_row[0]['ply_email'],
              'PlyEmailAlter' : player_row[0]['ply_email_alternative'] if  player_row[0]['ply_email_alternative'] else player_row[0]['ply_email'],
              'PlyGdr' : player_row[0]['ply_gender'],
              'PlyHeight' : player_row[0]['ply_height'],
              'H_Unt' : player_row[0]['ply_h_unit'],
              'PlyWeight' : player_row[0]['ply_weight'],
              'W_Unt' : player_row[0]['ply_w_unit'],
              'PlyStatus' : player_row[0]['ply_status'],
              'PlyctyID' : player_row[0]['ply_city_id'],
              'PlyCty': player_row[0]['city_name'] if player_row[0]['city_name'] else urllib.parse.quote(player_row[0]['typed_city'])if player_row[0]['typed_city'] else "",
              'CountryID' : player_row[0]['country_id'],
              'CountryIso' : player_row[0]['iso'],
              'CountryName' : player_row[0]['country_name'],
              'Bio': urllib.parse.quote(player_row[0]['ply_bio'])if player_row[0]['ply_bio'] else "",
              'PlyImg' : player_row[0]['OrgImg'],
              'PlyImgThumb' : player_row[0]['OrgImgThumb'],
              'PImg' : 'ply/' + player_row[0]['ply_img'],
              'PHImg' : header_img,
              'NState' : notification_state,
              'LastGms' : lastGms,
              'Token' : token,
              'FrReqNum' : FrReqNum(player_row[0]['ply_id']),
              'UnreadMessNum' : UnreadMessNum(player_row[0]['ply_id']),
              'GCToken' : player_row[0]['ply_gc_token'] or '',
              #'StripeAccountType': stripe_acc_type,
              #'PlyHasExpressDashCode': player_dashcode,
              'StripeAdminConnected': stripe_admin_conn,
              'DevID' : dev_id,
              
              'Privacy' : {"mail": 'True' if player_row[0]['ply_email_sett'] == "y" else "False",
                           "birthdate": 'True' if player_row[0]['ply_brithdate_sett'] == "y" else "False",
                          "gender": 'True' if player_row[0]['ply_gender_sett'] == "y" else "False",
                           "city": 'True' if player_row[0]['ply_city_sett'] == "y" else "False"},

              'sysTotCommission': sysToCommission,
              'viewAs': player_row[0]['ply_view_as'] or "",
              #'PlySubscriptions' : subscriptions,
              #'invalidPlySubscriptions': invalidPlayerSubs,
              'Business': urllib.parse.quote(player_row[0]['ply_business']) if player_row[0]['ply_business'] else "",
              'Website' : player_row[0]['ply_website'] or "",
              #'stripeData' : stripeData,
              "plyCurrencyId": player_row[0]['plyCurrencyId'],
              "plyCurrencyName": player_row[0]['plyCurrencyName'],
              "plyCurrencySymbol": player_row[0]['plyCurrencySymbol'],
              "PlyTimeZone" :  urllib.parse.quote(player_row[0]['timezone']) if player_row[0]['timezone'] else  "",
              "PlyCreatedAt" : player_row[0]['ply_created'] or '' }
    return result


def LastGm(player_id=0, last_gm=0, show_private=0, project_id=1):
    if player_id:
        limit = ' LIMIT 0,5 '
        Private = ''
        if show_private == 0:
            Private = "AND gm_scope='Open to public'"
        if not last_gm or last_gm == 0:
            limit = " LIMIT 0,1 "

        gm_data = execution.execute(f'''SELECT *
                                    FROM gm_players 
                                    LEFT JOIN game ON gm_pid ={project_id} AND gm_id = gm_ply_gm_id
                                    LEFT JOIN city ON gm_city_id = city_id
                                    LEFT JOIN country on gm_country_id = country_id
                                    LEFT JOIN gm_s_types on gm_sub_type_id = gm_s_type_id
                                    LEFT JOIN notifications on gm_ply_ply_id = notifications_ply_id WHERE (gm_utc_datetime + INTERVAL gm_end_time MINUTE) < CURRENT_TIMESTAMP
                                    AND gm_ply_ply_id = {player_id}
                                    AND gm_ply_status = 'y'
                                    AND gm_status IS NULL {Private} ORDER BY gm_date DESC, gm_start_time DESC 
                        {limit};''')
        result = []

        for GmRow in gm_data:
            # get game image
            if GmRow['gm_s3_status'] == 1:
                GmRow['OrgImg'] = s3_bucket_url + "/upload/gm/" + str(GmRow['gm_img'])
                GmRow['gm_img'] = str(GmRow['gm_img']).replace(
                    "classes", "classes/thumb")
                GmRow['OrgImgThumb'] = s3_bucket_url + "/upload/gm/" + str(GmRow['gm_img'])
            else:
                GmRow['OrgImg'] = s3_bucket_url + "/backup/upload/gm/" + str(GmRow['gm_img'])
                GmRow['OrgImgThumb'] = s3_bucket_url + "/backup/upload/gm/" + str(GmRow['gm_img'])

            state = GmRow['notifications_state']
            if GmRow['notifications_game_stop'] and int(GmRow['gm_id']) > 0:
                notify_data = GmRow['notifications_game_stop'].split(',')
                if GmRow['gm_id'] in notify_data:
                    state = 0

            if not GmRow['gm_end_time'] or GmRow['gm_end_time'] == 'NULL':
                gm_end_time = ''
            else:
                gm_end_time = GmRow['gm_end_time']

            if not GmRow['gm_loc_desc'] or GmRow['gm_loc_desc'] == 'NULL':
                gm_loc_desc = ''
            else:
                gm_loc_desc = GmRow['gm_loc_desc']

            if not GmRow['city_name'] or GmRow['city_name'] == 'NULL':
                city_name = ''
            else:
                city_name = GmRow['city_name']

            game = {'GmID': GmRow['gm_id'],
                    'GmT': GmRow['gm_title'],
                    'GmImg': GmRow['OrgImg'],
                    'GmImgThumb': GmRow['OrgImgThumb'],
                    'GImg': 'gm/' + str(GmRow['gm_img']),
                    'GmDate': GmRow['gm_date'],
                    'GDate': GmRow['gm_date'],
                    'SType': GmRow['gm_s_type_name'],
                    'CountryName': GmRow['country_name'],
                    'NState': state,
                    'STime': GmRow['gm_start_time'],
                    'ETime': gm_end_time,
                    'CityID': GmRow['gm_city_id'],
                    'CityName': city_name,
                    'LocDesc': gm_loc_desc}
            result.append(game)
        return result
    return Exception(response.error(code='100', message="Invalid data"))


# def RetriveCreditCardData(player_id):
#     CardName = ''
#     CardLast4 = ''
#     CardBrand = ''
#     CardExpM = ''
#     CardExpY = ''
#     CardConnected = "n"
#     BankVerified = "n"

#     stripe_data = execution.execute(f'''SELECT stripe_users_cust_id AS customer_id,
#                     stripe_users_account_code AS customer_code,
#                     stripe_users_account_id AS stripe_account_id,
#                     stripe_users_card_id AS credit_card_id
#                     FROM stripe_users
#                     WHERE stripe_users_ply_id = {player_id};''')

#     if stripe_data and stripe_data[0]['customer_id'] and stripe_data[0]['credit_card_id']:
#         CardConnected = 'y'
#         stripe_data['Verified'] = stripe.Customer.retrieve(stripe_data['customer_id'])
#         if stripe_data['Verified'] and stripe_data['Verified']['Result'] and stripe_data['Verified']['Result']['data'] and stripe_data['Verified']['Result']['data'][0]:
#             card_data = stripe_data['Verified']['Result']['data'][0]
#             CardName = card_data['billing_details']['name'] or ''
#             CardExpM = card_data['card']['exp_month'] or ''
#             CardExpY = card_data['card']['exp_year'] or ''
#             CardLast4= card_data['card']['last4'] or ''
#             CardBrand = card_data['card']['brand'] or ''

#             if stripe_data['Status'] and stripe_data['Status'] == 'verified':
#                 BankVerified ='y'
#     result = {'CardName' : CardName,
#             'CardExpM' : CardExpM,
#             'CardExpY' : CardExpY,
#             'CardLast4' : CardLast4,
#             'CardBrand' : CardBrand,
#             'CardConnected' : CardConnected,
#             'BankVerified' : BankVerified}  
#     return result     

def FrReqNum(player_id=0):
    rq_num = 0
    rq_data = execution.execute(f'''SELECT COUNT(inv_id) AS FrReqNum
                        FROM invitations 
                        WHERE inv_gm_id = 0 AND inv_accept = 'p' AND inv_ply_to_id = {player_id}
                        AND inv_ply_frm_id IN (SELECT ply_id FROM players WHERE ply_id = inv_ply_frm_id)''')
    if rq_data and rq_data[0]:
        rq_num = rq_data[0]['FrReqNum']
    return rq_num


def UnreadMessNum(player_id=0):
    unread_mess = 0
    unread_mess_data = execution.execute(
        f"SELECT COUNT(not_log_id)AS UnreadMessNum FROM notification_log WHERE not_log_IsRead = 'n' AND not_log_ply_frm > 0 AND not_log_ply_id = {player_id}")

    if unread_mess_data and unread_mess_data[0]:
        unread_mess = unread_mess_data[0]['UnreadMessNum']

    return unread_mess


def check_account_active(email, project_id):
    if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
        return False

    data = execution.execute(
        f"SELECT ply_status FROM players WHERE ply_email = '{email}' AND ply_pid= {project_id}")
    if data and data[0]['ply_status'] != '' and data[0]['ply_status'].lower() == 'deactive':
        return False

    return True




def player_rem_Qcode(player_id=0):
    if player_id > 0:
        execution.execute(
            f"UPDATE players SET ply_qcode = '', ply_status='' WHERE ply_id = {player_id}")

    
def add_player_token(player_id=0, dev_id='', gcm_reg='', source='', project_id=1):
    try:
        token_data = execution.execute(
            f'SELECT * FROM ply_tkn_gcm WHERE ply_tkn_gcm_pid ={project_id} AND  ply_tkn_gcm_ply_id ={player_id} AND ply_tkn_gcm_dev ="{dev_id}" AND ply_tkn_gcm_source="{source}" ')
        datetime.now(tz=pytz.utc)

        token = hashlib.sha1(str(datetime.now()).encode()).hexdigest()
        if str(token_data).__contains__('Something went wrong:'):
            raise Exception(token_data)
        if token_data:
            if gcm_reg != '':
                execution.execute(
                    f'UPDATE ply_tkn_gcm SET ply_tkn_gcm_token = "{token}", ply_tkn_gcm_reg = "{gcm_reg}"  WHERE ply_tkn_gcm_id = {token_data[0]["ply_tkn_gcm_id"]}')
            else:
                execution.execute(
                    f'UPDATE ply_tkn_gcm SET ply_tkn_gcm_token = "{token}" WHERE ply_tkn_gcm_id = {token_data[0]["ply_tkn_gcm_id"]}')
        else:
            execution.execute(
                f'INSERT INTO ply_tkn_gcm (ply_tkn_gcm_ply_id,ply_tkn_gcm_token,ply_tkn_gcm_dev,ply_tkn_gcm_source,ply_tkn_gcm_pid) VALUES ({player_id} , "{token}", "{dev_id}" , "{source}",{project_id})')

        return token

    except Exception as e:
        return e.__str__()


def saveTimeZone(player_id=0, timezone=''):
    if player_id < 1:
        return False
    data = execution.execute(
        f"SELECT id FROM ply_timezone WHERE player_id={player_id}")

    if data and data[0]['id'] and data[0]['id'] > 0:
        execution.execute(
            f"UPDATE ply_timezone set timezone = '{urllib.parse.quote(timezone)}' WHERE player_id={player_id} AND id={data[0]['id']}")

    else:
        execution.execute(
            f"INSERT INTO ply_timezone (player_id, timezone) VALUES ({player_id}, '{urllib.parse.quote(timezone)}'")

    execution.execute(
        f"INSERT INTO ply_timezone_log (player_id, timezone) VALUES ({player_id}, '{urllib.parse.quote(timezone)}'")

    return True


def check_mail(email, project_id):
    try:
        player_id = execution.execute(f"SELECT ply_id FROM players WHERE ply_email = '{email}' AND ply_pid = '{project_id}'")
        if str(player_id).__contains__('Something went wrong: '):
            raise Exception(player_id)
        if not player_id:
            return 0
        else:
            return int(player_id[0]['ply_id'])


    except Exception as e:

        return e.__str__()


def check_suspended_mail(email, project_id):
    try:
        player_id = execution.execute(f"SELECT sus_id FROM suspended_players WHERE sus_ply_pid ='{project_id}' AND sus_ply_email = '{email}'")
        if str(player_id).__contains__('Something went wrong: '):
            raise Exception(player_id)
        if not player_id:
            return 0
        else:
            return int(player_id[0]['sus_id'])

    except Exception as e:
        return e.__str__()


def org_contacts(org_id=0, joined_ply_ids=[], pid=1):
    result = []
    if joined_ply_ids and len(joined_ply_ids) > 0:
        all_org_contacts = execution.execute(f'''SELECT *
                    FROM contacts
                    WHERE contact_org_id= {org_id} AND contact_ply_id NOT IN {tuple(joined_ply_ids) if len(joined_ply_ids) > 1 else '(' + str(joined_ply_ids[0]) + ')'}
                    AND contact_deleted = 0;''')
    else:
        all_org_contacts = execution.execute(f'''SELECT *
                    FROM contacts
                    WHERE contact_org_id= {org_id}
                    AND contact_deleted = 0;''')
    if str(all_org_contacts).__contains__('Something went wrong: '):
        raise Exception(all_org_contacts)

    if all_org_contacts and len(all_org_contacts) > 0:
        emails = []
        contact_ids = []
        for contact in all_org_contacts:
            emails.append(contact['contact_email'])
            if contact['contact_id']:
                contact_ids.append(contact['contact_id'])

        players = execution.execute(f'''SELECT * FROM players
                                    WHERE ply_email IN ({','.join('"' + email + '"' for email in emails)}) AND ply_pid ={pid};''')

        if str(players).__contains__('Something went wrong: '):
            raise Exception(players)

        last_gms = execution.execute(f'''SELECT gm_id, gm_title, gm_date, gm_start_time, gm_utc_datetime,attend_type, contact_id,
                (
                    CASE
                        WHEN gm_utc_datetime  + INTERVAL gm_end_time MINUTE > CURRENT_TIMESTAMP THEN 'Registered'
                        WHEN (guest_checkedIn = 1) THEN 'attended'
                        WHEN (guest_checkedIn = 0) THEN 'no show'
                    END
                ) AS gm_attend_status
                FROM guests
                JOIN game ON game.gm_id = guests.guest_gm_id
                JOIN contacts ON contacts.contact_id IN {tuple(contact_ids) if len(joined_ply_ids) > 1 else '(' + str(joined_ply_ids[0]) + ')'}
                WHERE gm_org_id = {org_id}
                AND guests.guest_mail = contacts.contact_email
                AND guests.guest_fname = contacts.contact_f_name
                AND guests.guest_lname = contacts.contact_l_name
                AND contacts.contact_org_id = {org_id}
                ORDER BY gm_date DESC, gm_start_time DESC
                LIMIT 1
                OFFSET 0 ''')

        if str(last_gms).__contains__('Something went wrong: '):
            raise Exception(last_gms)

        for contact in all_org_contacts:
            lastGms = []
            cont_ply = 'missing'
            for gm in last_gms:
                if contact['contact_id'] == gm['contact_id']:
                    lastGms.append(gm)
            for player in players:
                if contact['contact_email'] == player['ply_email']:
                    cont_ply = player['ply_id']

            if player['ply_id'] not in joined_ply_ids:
                contact_data = {'ContactID': contact['contact_id'],
                                'ContactFname': contact['contact_f_name'],
                                'ContactLname': contact['contact_l_name'],
                                'ContactEmail': contact['contact_email'],
                                'ContactPlyID': cont_ply if cont_ply != 'missing' else contact['contact_ply_id'],
                                'LastGm': lastGms}
                result.append(contact_data)
    return result


def org_players(org_id=0, pid=1):
    all_org_plys = execution.execute(f'''SELECT DISTINCT gmp.gm_ply_ply_id AS ply_id , gm.gm_id
                                        FROM gm_players gmp LEFT JOIN game gm
                                        ON gmp.gm_ply_gm_id = gm.gm_id
                                        WHERE gm.gm_org_id ={org_id} AND gmp.gm_ply_ply_id !={org_id}
                                        UNION 
                                        SELECT DISTINCT canceled.gm_plys_log_ply_id AS ply_id , gm.gm_id
                                        FROM cancel_gm_plys_log canceled LEFT JOIN game gm
                                        ON canceled.gm_plys_log_gm_id = gm.gm_id
                                        WHERE gm.gm_org_id ={org_id} AND canceled.gm_plys_log_ply_id !={org_id}
                                        UNION
                                        SELECT DISTINCT sub.ply_id AS ply_id,''
                                        FROM bundles.bundles_subscriptions sub
                                        LEFT JOIN bundles.bundles as bundles ON bundles.id=sub.bundle_id 
                                        WHERE bundles.org_id = {org_id} AND sub.is_removed=0
                                        AND sub.ply_id != 0''')

    if str(all_org_plys).__contains__('Something went wrong: '):
        raise Exception(all_org_plys)

    ply_ids = []
    for ply in all_org_plys:
        ply_ids.append(ply['ply_id'])

    ply_ids = list(set(ply_ids))

    players = execution.execute(
        f"SELECT * FROM players WHERE ply_id IN {tuple(ply_ids) if len(ply_ids) > 1 else '(' + str(ply_ids[0]) + ')'}")

    last_games = execution.execute(f'''SELECT * FROM gm_players 
                                        LEFT JOIN game ON gm_pid ={pid} AND gm_id=gm_ply_gm_id
                                        LEFT JOIN city ON gm_city_id = city_id
                                        WHERE (gm_utc_datetime + INTERVAL gm_end_time MINUTE) < CURRENT_TIMESTAMP
                                        AND gm_ply_ply_id IN {tuple(ply_ids) if len(ply_ids) > 1 else '(' + str(ply_ids[0]) + ')'} 
                                        AND gm_org_id = {org_id}
                                        ORDER BY gm_date DESC,gm_start_time DESC  LIMIT 0,1;''')

    if str(players).__contains__('Something went wrong: '):
        raise Exception(players)

    if str(last_games).__contains__('Something went wrong: '):
        raise Exception(last_games)

    all_player_data = []
    for player in players:
        last_gm = []
        for game in last_games:
            if game['gm_ply_ply_id'] == player['ply_id']:
                last_gm = {'GmID': game['gm_id'],
                           'GmT': game['gm_title'],
                           'GImg': 'gm/' + game['gm_img'],
                           'GmDate': game['gm_date'],
                           'STime': game['gm_start_time'],
                           'ETime': game['gm_end_time'] if game['gm_end_time'] != 'NULL' else '',
                           'CityID': game['gm_city_id'],
                           'CityName': game['city_name'] or '',
                           'LocDesc': game['gm_loc_desc'] if game['gm_loc_desc'] != 'NULL' else '',
                           }
                break

        ply_data = {'PlyID': player['ply_id'],
                    'PlyFname': player['ply_fname'],
                    'PlyLname': player['ply_lname'],
                    'PlyEmail': player['ply_email'],
                    'LastGm': last_gm,
                    'LastGmDate': last_gm['GmDate'] if last_gm and last_gm['GmDate'] else ''}
        all_player_data.append(ply_data)

    result = {'OrgPlyData': all_player_data, 'OrgPlyIDs': list(ply_ids)}

    return result

def player_profile_data(organizer_id  , player_id , project_id ) :
    player_arr = {}
    player_data = execution.execute(f'''SELECT ply_fname , ply_lname , ply_email , (CASE WHEN ply_gender='m' THEN 'Male'
                    WHEN ply_gender='f' THEN 'Female' END ) AS gender,
                    ply_img , TIMESTAMPDIFF(YEAR, ply_brithdate, CURDATE()) AS plyAge , ply_mobile_phone, s3_profile
                    FROM players WHERE ply_id = {player_id}''')
    if player_data and player_data[0]['ply_email']:
        # migrated_user_data =  
        execution.execute(f'''SELECT migrate_usr_mobile_phone , migrate_usr_home_phone , migrate_usr_work_phone
                               FROM migrated_users
                               WHERE migrate_usr_orgID = {organizer_id} AND migrate_usr_email= {player_data[0]['ply_email']}
                               AND migrate_usr_pid = {project_id}''')
        ply_images=[]
        if player_data[0]['ply_img']:
                # Util::GetPlyImages($plyRow['ply_img'],$plyRow['s3_profile']);
                ply_images = ""  # calling from image module 
        player_arr["fname"] = player_data[0]["ply_fname"]
        player_arr["lname"] = player_data[0]["ply_lname"]
        player_arr["email"] = player_data[0]["ply_email"]
        player_arr["gender"] = player_data[0]["gender"]
        player_arr["plyAge"] = player_data[0]["plyAge"]
        player_arr["plyImg"] = ""
        # ply_images[0]['ply_img']
        player_arr["phone"] = player_data[0]["ply_mobile_phone"]
        player_arr["type"] = 'player'
    return player_arr

def contact_profile_data(organizer_id , contact_id ,project_id):
    player_arr = {}
    contact_data = execution.execute(f'''SELECT contact_f_name , contact_l_name , contact_email , contact_age , contact_phone , 
                    (CASE WHEN contact_gender='m' THEN 'Male'
                    WHEN contact_gender='f' THEN 'Female' END ) AS gender
                    FROM contacts WHERE contact_deleted =0 AND contact_id = {contact_id}''')
  
    if contact_data and contact_data[0]['contact_email']:
        migrate_user_data = execution.execute(f'''SELECT migrate_usr_mobile_phone , migrate_usr_home_phone , migrate_usr_work_phone
                               FROM migrated_users
                               WHERE migrate_usr_orgID = {organizer_id} AND migrate_usr_email= '{contact_data[0]['contact_email']}'
                               AND migrate_usr_pid = {project_id}''')
        contact_phone = ""
  
        # print(migrate_user_data[0]['migrate_usr_mobile_phone'])
        if contact_data[0]['contact_phone']:
            contact_phone = contact_data[0]['contact_phone']
        elif migrate_user_data[0]['migrate_usr_mobile_phone']:
            contact_phone = migrate_user_data[0]['migrate_usr_mobile_phone']
        ply_images = ""
        if contact_data[0]['gender']:
            if contact_data[0]['gender'] == 'Male' :
                # hanle in img module 
                ply_images = ""
            if contact_data[0]['gender']== 'Female':
                # hanle in img module 
                ply_images = ""
        else :
            # hanle in img module 
            ply_images =""
        player_arr["fname"] = contact_data[0]["contact_f_name"]
        player_arr["lname"] = contact_data[0]["contact_l_name"]
        player_arr["email"] = contact_data[0]["contact_email"]
        player_arr["gender"] = contact_data[0]["gender"]
        player_arr["plyAge"] = contact_data[0]["contact_age"]
        player_arr["plyImg"] = ply_images
        player_arr["phone"] = contact_phone
        player_arr["type"] = 'contact'

    return player_arr

def get_player_org_contact_data (data):
    # organizer_id=0, player_id=0, contact_id=0):
    arr = []
    try :
        if not data['organizer_id'] or  type(data['organizer_id']) != int or int(data['organizer_id']) < 0  :
            raise Exception("organizer id required")

        if not data['player_id'] or type(data['player_id']) != int  or int(data['player_id']) < 0 :
            raise Exception("player id required")
        else : 
            arr = player_profile_data(data['organizer_id'] , data['player_id'] ,data ['project_id'])

        if not data['contact_id'] or type(data['contact_id']) != int or int(data['contact_id']) < 0  :
            raise Exception("contact id required")
        else :
            arr = contact_profile_data(data['organizer_id'] , data['contact_id'], data['project_id'])
        return arr

    except Exception as e:
        return e.__str__()
     

def get_all_guest(game_id):
    try:
        AllGuests = execution.execute(
            f"SELECT guest_ply_id FROM guests WHERE guest_ply_id !=0 AND guest_gm_id = {game_id}")
        if AllGuests.__contains__("Something went wrong: "):
            raise Exception(AllGuests)
        else:
            guests_id = [guest.get('guest_ply_id') for guest in AllGuests]
            return guests_id
    except Exception as e:
        return e.__str__()


def gm_plys(gm_id,limit_start,limit_number,ply_id,org_id,project_id):
    try:
        if not gm_id and int(gm_id) <= 0:
            raise Exception("invalid gm_id")
        if not limit_start and int(limit_start) < 0:
            raise Exception("invalid limit_start")
        if not limit_number and int(limit_number) < 0:
            raise Exception("invalid limit_number")
        if not ply_id and int(ply_id) <= 0:
            raise Exception("invalid ply_id")
        if not org_id and int(org_id) <= 0:
            raise Exception("invalid org_id")
        if not project_id and int(project_id) <= 0:
            raise Exception("invalid project_id")

        gm_ply_arr = []
        gm_plyD = execution.execute(f"CALL GamePlayers('{gm_id}','{project_id}','{limit_start}','{limit_number}')")
        # all_guests = get_all_guest(gm_id)



    except Exception as e:
        return "something happened:" + e.__str__()


