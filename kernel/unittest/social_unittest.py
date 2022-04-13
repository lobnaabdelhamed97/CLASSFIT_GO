import unittest
from controllers.game_controller import social


class TestSocial(unittest.TestCase):

    def test_social(self):
        try:

            test_data_object = {
                'case_1': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87', 'source': 'web'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_2': {'Email': 7, 'project_id': 1, 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87',
                           'source': 'web'},
                # ,'game_id': 992 ,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_3': {'Email': '', 'project_id': 1, 'ProjectKey': '1234', 'ProjectSecret': '1234',
                           'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_4': {'Email': 'mailinator.com', 'project_id': 0, 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_5': {'Email': 'am@mailinator.com', 'project_id': "", 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                # ,'game_id': 992,'player_id': 7867 , 'ProjectKey': '1234', 'ProjectSecret': '1234','tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'},
                'case_6': {'Email': 'am@mailinator.com', 'project_id': "mm", 'ProjectKey': '1234',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                'case_7': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '',
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                'case_8': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                           'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                'case_9': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                           'ProjectSecret': '', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                           'dev_id': '100f11dc8b54fb87'},
                'case_10': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                            'ProjectSecret': 9, 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b',
                            'dev_id': '100f11dc8b54fb87'},
                'case_11': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': '1234',
                            'ProjectSecret': '1234', 'tkn': '', 'dev_id': '100f11dc8b54fb87'},
                'case_12': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 9, 'dev_id': '100f11dc8b54fb87'},
                'case_13': {'Email': 'am@mailinator.com', 'project_id': 1, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': ''},
                # ,'game_id': 992,'player_id': 7867
                'case_14': {'Email': 'am@mailinator.com', 'player_id': 7867, 'ProjectKey': 9,
                            'ProjectSecret': '1234', 'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': 9},
                'case_15': {"source": "Web", 'project_id': 1, "ProjectSecret": "1234", "ProjectKey": "1234",
                            "tkn": "d9a4013b9cba108f12ae950f8ae38a5c0aec3622", "dev_id": "windows_Chrome_172.31.35.236",
                            "FName": "iii", "LName": "iii", "Email": "iii@mailinator.com"},
                'case_16': {"source": "Web", 'project_id': 1, "ProjectSecret": "1234", "ProjectKey": "1234",
                            "tkn": "d9a4013b9cba108f12ae950f8ae38a5c0aec3622", "dev_id": "windows_Chrome_172.31.35.236",
                            "FName": "lobna", "LName": "abdelhamed", "Email": "lobna@mailinator.com"},
                'case_17': {"source": "Web", 'project_id': 1, "ProjectSecret": "1234", "ProjectKey": "1234",
                            "tkn": "d9a4013b9cba108f12ae950f8ae38a5c0aec3622", "dev_id": "windows_Chrome_172.31.35.236",
                            "FName": "lllll", "LName": "mmmm", "Email": "lobna@xyzxyz.com"},
                'case_18': {"source": "Web", 'project_id': 1, "ProjectSecret": "1234", "ProjectKey": "1234",
                            "tkn": "d9a4013b9cba108f12ae950f8ae38a5c0aec3622", "dev_id": "windows_Chrome_172.31.35.236",
                            "FName": "lobna", "LName": "abdelhamed", "Email": "lobna@yahhooohhh.com",
                            "PlyImg": "https://classfit-assets.s3.amazonaws.com/2021/profile/010920219DFHC5stBJVY1bwpzuPmaEZROAMgeoWdhn6xNXy4kfIl20USK7.jpeg",
                            "addimg": "y"}
            }
            i = 1
            expected_output = {
                "invalid Email",
                "invalid project id", "invalid project key", "invalid token", "invalid device id",
                "invalid project secret"
                # ,"invalid game id","invalid project key","invalid token","invalid device id","invalid email" ,"invalid player id" ,"invalid project secret"
            }
            result_response = []

            for key, value in test_data_object.items():

                response = social(value)
                print("------------------------------ case " + str(i) + " result ------------------------------")
                print(response)

                str_response = str(response)
                i = i + 1
                result_response.append(str_response)
                if str_response not in expected_output or not str_response.__contains__("Result"):
                    # print(key)
                    testValue = False

                    test = self.assertTrue(str(str_response), testValue)

                    if test is None:
                        print("error occurs in case " + key + " and says " + str_response)
        except Exception as err:
            return err

    if __name__ == '__main__':
        unittest.main()
