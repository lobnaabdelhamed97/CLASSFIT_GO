import json
import unittest

from utils.notification_utils import checking_notification_for_player


class TestNotification(unittest.TestCase):
    # def test_notifications(self):
    #     response = notifications(ply_id= 5952, gm_id= 269641, remindstate= 1, period_type= "h", period=12)
    #     print("\n", response)
    #     self.assertTrue(response, "Error in data")

    def test_checking_notification_for_player(self):
        try:
            gm_data = {'Gm': {'GmID': 992, 'GmT': 'yoga%20test', 'OrgID': 894, 'OrgEmail': 'dainijis@hactzayvgqfhpd.tk',
                              'OrgName': 'newgen%2F%2Fsalma 3', 'OrgGdr': 'm', 'OrgBusiness': None, 'STypeID': 475,
                              'STypeName': 'Zumba', 'CourtID': 18, 'CourtT': 'Concrete', 'LevelID': 8,
                              'LevelT': 'All levels', 'ImgName': '3773c3450e6616d62dbd218ff3a120ad.jpg', 'Gdr': 'mf',
                              'Age': 'All ages', 'MinPly': 1, 'MaxPly': 2, 'STime': '22:45:00', 'ETime': 222,
                              'timeZone': None, 'CountryID': 66, 'CountryIso': 'EG', 'CountryName': 'Egypt',
                              'CityID': 0, 'CityName': None, 'Lat': '26.820553', 'DisOrg': 'n', 'Long': '30.802498',
                              'LocDesc': 'Egypt', 'Scope': 'Open to public', 'HasGlly': 'n', 'Desc': '',
                              'Req': 'ReqReqReqReqReq', 'Notes': 'NoteNoteNoteNote', 'Rules': 'RulesRulesRules',
                              'Kits': 'KitsKitsKitsKits', 'IsFree': 'y', 'attendType': None, 'zoomUrl': None,
                              'zoomMeetingId': None, 'PlyBirthDate': '1987-04-29', 'GmRecurrDaysTimes': None,
                              'PayType': 'Null', 'showMem': 'False', 'CurrencyID': 212, 'CurrencyName': 'gbp',
                              'currency_symbol': '£', 'PolicyID': 0, 'PolicyT': None, 'RecurrID': 8977,
                              'IsStopRecurred': 'n', 'gm_recurr_times': 0, 'gm_recurr_type': None, 'RenewID': 0,
                              'ply_img': '8616e8ab13dc8f83059036d123a7f724.gif', 's3_profile': 0, 'gm_s3_status': '0',
                              'GmOrgDate': '2018-06-04', 'gm_img': '3773c3450e6616d62dbd218ff3a120ad.jpg', 'Fees': 0,
                              'UTCDateTime': '2018-06-04 20:45:00', 'STypeImg': 'gm_s_types/Zumba-class.png',
                              'IsHis': 'y', 'ply_country_id': 66, 'FeedStatus': '', 'FeedPlyID': '', 'GmDist': '',
                              'zoomPwd': '',
                              'OrgImg': 'https://classfit-assets.s3.amazonaws.com/backup/upload/ply/8616e8ab13dc8f83059036d123a7f724.gif',
                              'OrgImgThumb': 'https://classfit-assets.s3.amazonaws.com/backup/upload/ply/8616e8ab13dc8f83059036d123a7f724.gif',
                              'GmImg': 'https://classfit-assets.s3.amazonaws.com/images/upload/gm/3773c3450e6616d62dbd218ff3a120ad.jpg',
                              'GmImgThumb': 'https://classfit-assets.s3.amazonaws.com/images/upload/gm/thumb/3773c3450e6616d62dbd218ff3a120ad.jpg',
                              'GmDate': '2018-06-04', 'SSTime': '08:45 PM', 'Day': 'Monday', 'EETime': '12:27 AM',
                              'Subscriptions': '',
                              'plySubscriptions': '', 'validJoinSubscriptions': '', 'invalidPlySubscriptions': '',
                              'orgOfflineStatus': '',
                              'Days': '', 'EndRecurr': ''}}

            test_data_object = {
                'case_1': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_2': {'project_id': "ss", 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_3': {'project_id': 0, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_4': {'project_id': 1, 'player_id': '842', 'game_id': 84843, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_5': {'project_id': 1, 'player_id': 0, 'game_id': 84843, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_6': {'project_id': 1, 'player_id': 842, 'game_id': 0, 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_7': {'project_id': 1, 'player_id': 842, 'game_id': "pp", 'typeo': "InvFriToGm",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_8': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "",
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_9': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': 9,
                           'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                           'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_10': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm", 'message': '',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_11': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm", 'message': 9,
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # 'case_12': {'project_id': 1,'player_id': 842 ,'game_id' : 84843 , 'typeo' : "InvFriToGm" , 'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00' ,'Gm':"", 'ProjectKey' :'1234' , 'ProjectSecret' : '1234' ,'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b' ,'dev_id': '100f11dc8b54fb87'},
                # 'case_13': {'project_id': 1,'player_id': 842 ,'game_id' : 84843 , 'typeo' : "InvFriToGm" , 'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00' ,'Gm':[], 'ProjectKey' :'1234' , 'ProjectSecret' : '1234' ,'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b' ,'dev_id': '100f11dc8b54fb87'},
                'case_12': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '', 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_13': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': 9, 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_14': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_15': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': 0,
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_16': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234', 'tkn': "",
                            'dev_id': '100f11dc8b54fb87'},
                'case_17': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234', 'tkn': 8,
                            'dev_id': '100f11dc8b54fb87'},
                'case_18': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': ''},
                'case_19': {'project_id': 1, 'player_id': 842, 'game_id': 84843, 'typeo': "InvFriToGm",
                            'message': 'newgen%2F%2Fsalma 3 has invited you to join yoga%20test on 2018-06-04 00:00:00',
                            'Gm': gm_data['Gm'], 'ProjectKey': '1234', 'ProjectSecret': '1234',
                            'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': 8},
            }
            i = 1
            result_response = []
            expected_output = {
                "{'Result': 'true'}", 'invalid project_id', 'invalid player_id', 'invalid game_id', 'invalid type',
                'invalid message', 'invalid data', 'invalid project key', 'invalid project key',
                'invalid project secret', 'invalid token', 'invalid device_id',
            }
            print(type(gm_data))
            # print(gm_data['Gm'])
            for key, value in test_data_object.items():
                print()
                response = checking_notification_for_player(value)
                # value['project_id'],value['game_id'],value['player_id'],value['type'],value['message'],value['data'],value['ProjectKey'],value['ProjectSecret'],value['tkn'],value['dev_id'])
                print("---------------------------------------------------- case " + str(
                    i) + " result ----------------------------------------------------")

                print(json.dumps(response))
                str_response = str(response)
                i = i + 1
                result_response.append(str_response)
                # print(result_response)
                result_response.append(str_response)
                if str_response not in expected_output:
                    # print(key)
                    testValue = False

                    test = self.assertTrue(str(str_response), testValue)

                    if test is None:
                        print("error occurs in case " + key + " and says " + str_response)

        except Exception as err:
            return err


if __name__ == '__main__':
    unittest.main()
