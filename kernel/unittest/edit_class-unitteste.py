import unittest

from utils.game_utils import *
from controllers.game_controller import *


class MyTestCase(unittest.TestCase):

    def test_get_policy_title(self):
        output = "something happened:"
        response = get_policy_title(PolicyID=6)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_currency_data(self):
        output = "something happened:"
        response = get_currency_data(symbol=6)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_level_name(self):
        output = "something happened:"
        response = get_level_name(LevelID=6)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_stype_name(self):
        output = "something happened:"
        response = get_stype_name(STypeID=6)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_specify_game_edits_to_historyLog(self):
        output = "something happened:"
        EditField = {"GmT": "amr", "GmDate": "2021-5-17", "STime": "14:40", "AttendType": "inPerson",
                     "STypeID": 464, "CourtID": 1, "LevelID": 8, "Age": "3", "Minply": 1,
                     "Maxply": 4, "ETime": "30", "LocDesc": "Alexandria%20Governorate%2C%20Egypt",
                     "Desc": "eewew", "Scope": "Open to public", "PayType": "stripe", 'PolicyID': 1,
                     "GmReqQues": "no", "Symbol": "61", "Fees": 80, 'imgChanged': True
                     }
        oldData = {"GmT": "amre", "GmDate": "2021-5-18", "STime": "15:40", "attendType": "zoom",
                   "STypeID": 465, "CourtID": 2, "LevelID": 9, "Age": "All ages", "MinPly": 2,
                   "MaxPly": 3, "ETime": 31, "LocDesc": "Alexandria%20Governorate%2C%20Egypt",
                   "Desc": "2133", "Scope": "Open to public", "PayType": "stripe", 'PolicyID': 1,
                   "GmReqQues": "no", "Fees": 80.0
                   }

        response = specify_game_edits_to_historyLog(EditField=EditField, OldData=oldData)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_add_class_to_bundles(self):
        output = "something happened:"
        EditField = {"ProjectKey": "1234", "ProjectSecret": "1234", "DevID": "windows_Firefox_156.197.248.161 ",
                     "Tkn": "b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e", "GmID": 6, "PlyID": 3500,
                     "source": "Web", "BundlesIds": "[676]",
                     }
        class_id = 6
        bundlesIds = {"BundlesIds": '676'}
        isRecurr = 0

        response = add_class_to_bundles(EditField=EditField, classId=class_id, bundlesIds=bundlesIds, isRecurr=isRecurr)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_ply_verified_methods(self):
        output = "something happened:"
        response = get_ply_verified_methods(PlyID=6)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_Wait_List_Members(self):
        output = "something happened:"
        response = get_Wait_List_Members(GmID=13521)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_zoom_user(self):
        output = "something happened:"
        response = get_zoom_user(PlyID=2305)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_Utc_Datetime(self):
        output = "something happened:"
        response = get_Utc_Datetime(tZone="Europe/London", dTime="2022-10-21 12:30")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_log_edit_action(self):
        output = "something happened:"

        EditField = {'ProjectKey': '1234', 'ProjectSecret': '1234', 'DevID': 'windows_Firefox_156.197.248.161 ',
                     'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', 'GmID': 6, 'GmT': '%20nola1%20test',
                     'PlyID': 3500, 'DisOrg': 'n', 'STypeID': 464, 'CourtID': 1, 'LevelID': 8, 'Age': '3', 'Minply': 1,
                     'Maxply': 3, 'GmDate': '2021-5-17', 'STime': '14:40', 'ETime': '30',
                     'UTCDateTime': 'Mon, 17 May 2021 11:40:00 GMT', 'CityName': '', 'CtyID': 0, 'CountryID': 66,
                     'Lat': 30.8760568, 'Long': 29.742604, 'LocDesc': 'Alexandria%20Governorate%2C%20Egypt',
                     'Scope': 'Open to public', 'Desc': '', 'Req': 'ReqReqReqReqReq', 'Note': 'NoteNoteNoteNote',
                     'Rules': 'RulesRulesRules', 'Kits': 'KitsKitsKitsKits', 'PayType': 'stripe', 'Fees': 80,
                     'Symbol': '61', 'PolicyID': 1, 'showMem': 'no', 'HasGlly': 'n', 'instructorId': 361,
                     'AttendType': 'inPerson', 'timeZoneZoom': '0',
                     'gameImg': '05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg',
                     'gmS3Status': '1', 'timeZone': 'Europe/London', 'source': 'Web', 'BundlesIds': '[676]',
                     'GmReqQues': '0'}
        newGmData = {"GmID": 6, "GmT": "%2520nola1%2520test", "OrgID": 852, "OrgEmail": "ma9300179@gmail.com",
                     "OrgName": "meroo moo", "OrgGdr": "f", "OrgBusiness": "", "STypeID": 464,
                     "STypeName": "Fitness",
                     "CourtID": 1, "CourtT": "Indoors", "LevelID": 8, "LevelT": "All levels",
                     "ImgName": "05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg",
                     "Gdr": "mf", "Age": "All ages", "MinPly": 1, "MaxPly": 3, "STime": "14:40:00", "ETime": 30,
                     "timeZone": "Europe/London", "CountryID": 66, "CountryIso": "EG", "CountryName": "Egypt",
                     "CityID": 0,
                     "CityName": "", "Lat": "30.8760568", "Long": "29.742604",
                     "LocDesc": "Alexandria%2520Governorate%252C%2520Egypt", "Scope": "Open to public",
                     "HasGlly": "n",
                     "Desc": "", "Req": "ReqReqReqReqReq", "Notes": "NoteNoteNoteNote", "Rules": "RulesRulesRules",
                     "Kits": "KitsKitsKitsKits", "IsFree": "n", "attendType": "inPerson", "zoomUrl": "",
                     "zoomMeetingId": "", "PlyBirthDate": "1993-4-4", "GmRecurrDaysTimes": "", "PayType": "Stripe",
                     "showMem": "False", "CurrencyID": 61, "CurrencyName": "egp", "currency_symbol": "\u00a3",
                     "PolicyID": 1, "PolicyT": "Refund available (If replaced)", "RecurrID": 0,
                     "IsStopRecurred": "",
                     "gm_recurr_times": 0, "gm_recurr_type": "", "RenewID": 0,
                     "ply_img": "de435fe61549b33e6f5069397c3116c9.jpeg", "s3_profile": 0, "gm_s3_status": "0",
                     "GmOrgDate": "2021-05-17",
                     "gm_img": "05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg",
                     "Fees": 80.0, "UTCDateTime": "2021-05-17 13:40:00", "STypeImg": "gm_s_types/Fitness-class.png",
                     "IsHis": "y", "ply_country_id": 235, "FeedStatus": "", "FeedPlyID": "", "GmDist": "",
                     "zoomPwd": "",
                     "OrgImg": "https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg",
                     "OrgImgThumb": "https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg",
                     "GmImg": "https://classfit-assets.s3.amazonaws.com/images/upload/gm/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg",
                     "GmImgThumb": "https://classfit-assets.s3.amazonaws.com/images/upload/gm/thumb/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg",
                     "GmDate": "2021-05-17", "SSTime": "01:40 PM", "Day": "Monday", "EETime": "02:10 PM",
                     "orgOfflineStatus": "", "Days": "", "EndRecurr": "", "gm_time_zone": "(Utc+00:00)",
                     "GmStatus": "",
                     "ISRecurr": "False", "Parent": "False", "GmReqQues": "no", "GmReported": "",
                     "Withdrawable": False,
                     "OrgMem": False, "InvGm": False, "PlyStatus": "No", "IsPly": "n", "RequestedBefore": "n",
                     "HasStopDays": "y", "NState": "on", "HaveReminder": "y", "RemindStat": "", "RemindPeriod": "",
                     "GmQues": [], "PlyAnswers": [], "Wait": []}

        oldData = {'GmID': 6, 'GmT': '%2520nola1%2520test', 'OrgID': 852, 'OrgEmail': 'ma9300179@gmail.com',
                   'OrgName': 'meroo moo', 'OrgGdr': 'f', 'OrgBusiness': '', 'STypeID': 464, 'STypeName': 'Fitness',
                   'CourtID': 1,
                   'CourtT': 'Indoors', 'LevelID': 8, 'LevelT': 'All levels',
                   'ImgName': '05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg',
                   'Gdr': 'mf',
                   'Age': 'All ages', 'MinPly': 1, 'MaxPly': 3, 'STime': '14:40:00', 'ETime': 30,
                   'timeZone': 'Europe/London',
                   'CountryID': 66, 'CountryIso': 'EG', 'CountryName': 'Egypt', 'CityID': 0, 'CityName': '',
                   'Lat': '30.8760568',
                   'Long': '29.742604', 'LocDesc': 'Alexandria%2520Governorate%252C%2520Egypt',
                   'Scope': 'Open to public',
                   'HasGlly': 'n', 'Desc': '', 'Req': 'ReqReqReqReqReq', 'Notes': 'NoteNoteNoteNote',
                   'Rules': 'RulesRulesRules',
                   'Kits': 'KitsKitsKitsKits', 'IsFree': 'n', 'attendType': 'inPerson', 'zoomUrl': '',
                   'zoomMeetingId': '',
                   'PlyBirthDate': '1993-4-4', 'GmRecurrDaysTimes': '', 'PayType': 'Stripe', 'showMem': 'False',
                   'CurrencyID': 61,
                   'CurrencyName': 'egp', 'currency_symbol': '£', 'PolicyID': 1,
                   'PolicyT': 'Refund available (If replaced)',
                   'RecurrID': 0, 'IsStopRecurred': '', 'gm_recurr_times': 0, 'gm_recurr_type': '', 'RenewID': 0,
                   'ply_img': 'de435fe61549b33e6f5069397c3116c9.jpeg', 's3_profile': 0, 'gm_s3_status': '0',
                   'GmOrgDate': '2021-05-17',
                   'gm_img': '05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg',
                   'Fees': 80.0,
                   'UTCDateTime': '2021-05-17 13:40:00', 'STypeImg': 'gm_s_types/Fitness-class.png', 'IsHis': 'y',
                   'ply_country_id': 235, 'FeedStatus': '', 'FeedPlyID': '', 'GmDist': '', 'zoomPwd': '',
                   'OrgImg': 'https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg',
                   'OrgImgThumb': 'https://classfit-assets.s3.amazonaws.com/backup/upload/ply/de435fe61549b33e6f5069397c3116c9.jpeg',
                   'GmImg': 'https://classfit-assets.s3.amazonaws.com/images/upload/gm/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg',
                   'GmImgThumb': 'https://classfit-assets.s3.amazonaws.com/images/upload/gm/thumb/05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg',
                   'GmDate': '2021-05-17', 'SSTime': '01:40 PM', 'Day': 'Monday', 'EETime': '02:10 PM',
                   'orgOfflineStatus': '',
                   'Days': '', 'EndRecurr': '', 'gm_time_zone': '(Utc+00:00)', 'GmStatus': '', 'ISRecurr': 'False',
                   'Parent': 'False', 'GmReqQues': 'no', 'GmReported': '', 'Withdrawable': False, 'OrgMem': False,
                   'InvGm': False,
                   'PlyStatus': 'No', 'IsPly': 'n', 'RequestedBefore': 'n', 'HasStopDays': 'y', 'NState': 'on',
                   'HaveReminder': 'y', 'RemindStat': '', 'RemindPeriod': '', 'GmQues': [], 'PlyAnswers': [],
                   'Wait': []}

        response = log_edit_action(EditField=EditField, newGmData=newGmData, oldData=oldData)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_game_recur_id(self):
        output = "something happened:"
        response = get_game_recur_id(GmID=6)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_update_access_token(self):
        output = "something happened:"
        response = update_access_token(player_id=2152,
                                       access_token="eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiIxNmZiMTZkOC1lMTUwLTRkNDktODEyMS0zM2U4MTYxY2RiMWMifQ.eyJ2ZXIiOjcsImF1aWQiOiJmNTA1ZjMyMjhkMTljYzRkZGExOGJlZDQ0ZGU1Y2JkZSIsImNvZGUiOiI4T1NaY05BYTF1X0VsZFIyX2IwUkZxdzVMd0NXdElENUEiLCJpc3MiOiJ6bTpjaWQ6YlhON190dGFURmVZekhyRXFuSHp0QSIsImdubyI6MCwidHlwZSI6MSwidGlkIjo3OTksImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IkVsZFIyX2IwUkZxdzVMd0NXdElENUEiLCJuYmYiOjE2MTkzMDUyNDQsImV4cCI6MjA5MjM0NTI0NCwiaWF0IjoxNjE5MzA1MjQ0LCJhaWQiOiI3emNiSkJ2UlI4NmFheDYxTHEwRFRBIiwianRpIjoiNTQ4ZGRmZWUtYWI5ZS00MzkwLWFjMmItMmUxNjNhMDQ2ZDVhIn0.gR3t2pOcgFAkYHqmxkM5Sp_du_KVNacG8_ckR6GGCFTkS1mMfxNngtWg3oSN5yx05Qu-AV5zgL-ehW_1qr5RGA")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_game_instructor_data(self):
        output = "something happened:"
        response = get_game_instructor_data(game_id=141818, game_recurr_id=1, for_recur_only=True)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_parent_id(self):
        output = "something happened:"
        response = get_parent_id(game_id=6, game_recurr_id=1)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_handle_all_recur_instructorQuery(self):
        output = "something happened:"
        response = handle_all_recur_instructorQuery(instructor_id=6, game_id=141818, game_recurr_id=1)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_handle_one_future_recur_instructorQuery(self):
        output = "something happened:"
        response = handle_one_future_recur_instructorQuery(instructor_id=6, game_id=141818)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_handle_game_instructor(self):
        output = "something happened:"
        response = handle_game_instructor(game_id=6, game_recurr_id=1, instructor_id=6, modify_type='')
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_validation_field_to_edit(self):
        output = "something happened:"

        EditField = {
            "ProjectKey": "1234",
            "ProjectSecret": "1234",
            "DevID": "windows_Firefox_156.197.248.161 ",
            "Tkn": "b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e",
            "GmID": 6,
            "GmT": "%20nola1%20test",
            "PlyID": 3500,
            "DisOrg": "n",
            "STypeID": 464,
            "CourtID": 1,
            "LevelID": "4",
            "Age": "3",
            "Minply": 1,
            "Maxply": 3,
            "GmDate": "2021-5-17",
            "STime": "14:40",
            "ETime": "30",
            "UTCDateTime": "Mon, 17 May 2021 11:40:00 GMT",
            "CityName": "", "CtyID": 0,
            "CountryID": 66,
            "Lat": 30.8760568,
            "Long": 29.742604,
            "LocDesc": "Alexandria%20Governorate%2C%20Egypt",
            "Scope": "Open to public",
            "Desc": "",
            "Req": "ReqReqReqReqReq",
            "Note": "NoteNoteNoteNote",
            "Rules": "RulesRulesRules",
            "Kits": "KitsKitsKitsKits",
            "PayType": "stripe",
            "Fees": 80,
            "Symbol": "61",
            "PolicyID": 1,
            "showMem": "no",
            "HasGlly": "n",
            "instructorId": 361,
            "AttendType": "inPerson",
            "timeZoneZoom": "0",
            "gameImg": "05-2021/classes/09052021JSbc0mdRZyL8ApTijnB7MKe5sPV2UYqzHuNCFhlta46wXQEIrg.jpg",
            "gmS3Status": "1",
            "timeZone": "Europe/London",
            "source": "Web",
            "BundlesIds": "[676]",
            "GmReqQues": "no",
        }
        response = validation_field_to_edit(EditField=EditField)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_edit_class(self):
        try:

            test_data_object = {
                'case_1': {'ProjectKey': "1234", 'ProjectSecret': '1234', 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},
                'case_2': {'ProjectKey': '', 'ProjectSecret': '1234', 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},
                'case_3': {'ProjectKey': 1234, 'ProjectSecret': '1234', 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},
                'case_4': {'ProjectKey': "1234", 'ProjectSecret': '', 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},
                'case_5': {'ProjectKey': "1234", 'ProjectSecret': 1234, 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},

                'case_6': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': '',
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},

                'case_7': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 2323,
                           'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},

                'case_8': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': '', 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},

                'case_9': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                           'PlyID': 0, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                           "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                           "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                           "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                           "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1, "ISFreeChk": "n",
                           "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                           "timeZone": "Africa/Cairo", "source": "Web"},

                'case_10': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': '', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_11': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 3232, "DisOrg": "",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_12': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": 32,
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_13': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": "", "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1, "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_14': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": "284076", "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_15': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_16': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": 23, "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_17': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": "tee", "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_18': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": "", "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_19': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_20': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "sssd", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_21': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": 463, "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_22': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": "qwqw",
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_23': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": '',
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_24': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 0,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_25': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 0,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_26': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": "ffsd",
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_27': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": '',
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_28': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_29': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "dssd", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_30': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": 12, "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_31': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_32': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": 2323, "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_33': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 0,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_34': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": "66",
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_35': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": '',
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_36': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": "30.8760568", "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_37': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": "", "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_38': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 0, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_39': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 0, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_40': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": "", "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_41': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": "29.742604", "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_42': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_43': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": 34, "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_44': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_45': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": 'n', "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": 97973,
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_46': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "23", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": 00, "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_47': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "wffd", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_48': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_49': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": 000e32, "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_50': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": "10", "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_51': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": "", "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_52': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 00, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_53': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_54': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "fgfdg", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_55': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": 00, "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_56': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": "fddf",
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_57': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": "",
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_58': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "433",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_59': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": 'n', "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": 4343,
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_60': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_61': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_62': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "44334", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_63': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": 23234, "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_64': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": "2342", "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_65': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": "reer", "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_66': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": "", "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_67': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "",
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_68': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": 3434,
                            "timeZone": "Africa/Cairo", "source": "Web"},

                'case_69': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "", "source": "Web"},

                'case_70': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": 3443, "source": "Web"},

                'case_71': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": ""},

                'case_72': {'ProjectKey': "1234", 'ProjectSecret': "1234", 'DevID': 'windows_Firefox_156.197.248.161 ',
                            'PlyID': 7163, 'Tkn': 'b8f72b4ea3de157f4e23022c0ba82a36a9b15a9e', "DisOrg": "n",
                            "GmID": 284076, "IsPly": "n", "STypeID": 463, "STypeName": "463", "Minply": 1,
                            "Maxply": 3,
                            "ETime": "12", "UTCDateTime": "Thu, 31 Mar 2022 07:00:00 GMT", "CountryID": 66,
                            "Lat": 30.8760568, "Long": 29.742604, "AttendType": "inPerson", "Scope": "Open to public",
                            "Desc": "", "PayType": "stripe", "Fees": 10, "Symbol": "61", "PolicyID": 1,
                            "ISFreeChk": "n",
                            "GmReqQues": "no", "instructorId": 2342, "timeZoneZoom": "Africa/Cairo",
                            "timeZone": "Africa/Cairo", "source": 68687},

            }
            i = 1
            expected_output = {
                "invalid email", "invalid project id", "invalid game id", "invalid project key", "invalid token",
                "invalid device id", "invalid email", "invalid player id", "invalid project secret"
            }
            result_response = []

            for key, value in test_data_object.items():

                response = edit_class(value)
                print("------------------------------ case " + str(i) + " result ------------------------------")
                print(response)

                str_response = str(response)
                i = i + 1
                result_response.append(str_response)
                if str_response not in expected_output:
                    # print(key)
                    testValue = False

                    test = self.assertTrue(str(str_response), testValue)

                    if test is None:
                        print("error occurs in case " + key + " and says " + str_response)
        except Exception as err:
            # print(err)
            return err


if __name__ == '__main__':
    unittest.main()
