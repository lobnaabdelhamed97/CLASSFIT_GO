import unittest

from controllers.game_controller import *


# from main import app , payload

class TestPendPlayer(unittest.TestCase):

    def test_pending_player(self):
        try:

            test_data_object = {
                # 'case_0':{'player_email': 'am@mailinator.com', 'project_id':1 ,"ProjectSecret":"1234","ProjectKey":"1234","tkn": "d9a4013b9cba108f12ae950f8ae38a5c0aec3622", "dev_id": "windows_Chrome_172.31.35.236"},
                'case_1': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_2': {'player_email': 7, 'project_id': 1, 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992 ,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_3': {'player_email': '', 'project_id': 1, 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_4': {'player_email': 'mailinator.com', 'project_id': 0, 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_5': {'player_email': 'am@mailinator.com', 'project_id': "", 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_6': {'player_email': 'am@mailinator.com', 'project_id': "mm", 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # 'case_7': {'player_email': 'am@mailinator.com', 'project_id':1,'game_id': 'kkkkk','player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # 'case_8': {'player_email': 'am@mailinator.com', 'project_id':1,'game_id': 992,'player_id': '7867' , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # 'case_9': {'player_email': 'am@mailinator.com', 'project_id':1,'game_id': 992,'player_id': 0 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_10': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '',
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                            'dev_id': '100f11dc8b54fb87'},
                'case_11': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                            'dev_id': '100f11dc8b54fb87'},
                'case_12': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                            'ProjectSecret': '', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                            'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 ,
                'case_13': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                            'ProjectSecret': 9, 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                            'dev_id': '100f11dc8b54fb87'},
                'case_14': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                            'ProjectSecret': '1234', 'tkn': '', 'dev_id': '100f11dc8b54fb87'},
                'case_15': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 9, 'dev_id': '100f11dc8b54fb87'},
                # 'game_id': 992,'player_id': 7867 ,
                'case_16': {'player_email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': ''},
                # ,'game_id': 992,'player_id': 7867
                'case_17': {'player_email': 'am@mailinator.com', 'player_id': 7867, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': 9}
                # , 'project_id':1,'game_id': 992
            }
            i = 1
            expected_output = {
                '{"result": "True", "data": {"output": "true"}, "emaildata": "", "code": 200}', "invalid email",
                "invalid project id", "invalid project key", "invalid token", "invalid device id", "invalid email",
                "invalid project secret"
                # ,"invalid game id","invalid project key","invalid token","invalid device id","invalid email" ,"invalid player id" ,"invalid project secret"
            }
            result_response = []

            for key, value in test_data_object.items():

                response = pending_player(value)
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
