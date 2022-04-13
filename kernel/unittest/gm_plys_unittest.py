import unittest
from utils.player_utils import *
from controllers.game_controller import *


class MyTestCase(unittest.TestCase):
    def test_set_ply_data(self):
        output = "something happened:"
        gm_id = 3521
        project_id = 1
        game_player_data = [
            {'ply_id': 848, 'ply_fname': 'classfit', 'ply_lname': '1', 'ply_email': 'dainijis@ob5d31gf3whzcoo.ga',
             'ply_brithdate': '1999-12-16', 'ply_gender': 'Male', 'ply_height': 0, 'ply_h_unit': 'cm', 'ply_weight': 0,
             'ply_w_unit': 'kg', 'ply_email_sett': 'y', 'ply_brithdate_sett': 'n', 'ply_gender_sett': 'n',
             'ply_city_sett': 'n', 'ply_city_id': 0, 'city_name': None, 'ply_country_id': 66, 'country_name': 'Egypt',
             'ply_img': 'bab3eb743ae6268004111323fece0562.jpg', 'Age': 22, 'IsCheckedIn': 0}]

        response = set_ply_data(game_player_data, gm_id, project_id)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_gm_plys(self):
        try:
            # 'ply_id': 1503, 'org_id': 1503
            test_data_object = {
                'case_1': {'gm_id': 3521, 'limit_start': 0, 'limit_number': 50, 'project_id': 1},
                'case_2': {'gm_id': "wee", 'limit_start': 0, 'limit_number': 50, 'project_id': 1},
                'case_3': {'gm_id': '', 'limit_start': 0, 'limit_number': 50, 'project_id': 1},
                'case_4': {'gm_id': [], 'limit_start': 0, 'limit_number': 50, 'project_id': 1},
                'case_5': {'gm_id': 3521, 'limit_start': 'sffd', 'limit_number': 50, 'project_id': 1},
                'case_6': {'gm_id': 3521, 'limit_start': '', 'limit_number': 50, 'project_id': 1},
                'case_7': {'gm_id': 3521, 'limit_start': [], 'limit_number': 50, 'project_id': 1},
                'case_8': {'gm_id': 3521, 'limit_start': 0, 'limit_number': 'ewew', 'project_id': 1},
                'case_9': {'gm_id': 3521, 'limit_start': 0, 'limit_number': '', 'project_id': 1},
                'case_10': {'gm_id': 3521, 'limit_start': 0, 'limit_number': [], 'project_id': 1},
                'case_11': {'gm_id': 3521, 'limit_start': 0, 'limit_number': 50, 'project_id': 'dsds'},
                'case_12': {'gm_id': 3521, 'limit_start': 0, 'limit_number': 50, 'project_id': ''},
                'case_13': {'gm_id': 3521, 'limit_start': 0, 'limit_number': 50, 'project_id': []},
            }
            i = 1
            expected_output = {"invalid project id", "invalid project key", "invalid token", "invalid device id",
                               "invalid project secret"}
            result_response = []

            for key, value in test_data_object.items():
                print(value)
                response = gm_plys(value)
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
