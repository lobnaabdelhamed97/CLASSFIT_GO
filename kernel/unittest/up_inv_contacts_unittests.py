import unittest

from controllers.admin_controller import *


class MyTestCase(unittest.TestCase):
    def test_up_inv_contacts(self):
        try:
            test_data_object = {
                'case_1': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': 4605,
                           'project_id': 1},
                'case_2': {'first_name': "", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': 4605,
                           'project_id': 1},
                'case_3': {'first_name': 324, 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': 4605,
                           'project_id': 1},
                'case_4': {'first_name': "amr", 'last_name': "", 'email': "002@mailinator.com", 'ply_id': 4605,
                           'project_id': 1},
                'case_5': {'first_name': "amr", 'last_name': 3223, 'email': "002@mailinator.com", 'ply_id': 4605,
                           'project_id': 1},
                'case_6': {'first_name': "amr", 'last_name': "sobhy", 'email': "", 'ply_id': 4605, 'project_id': 1},
                'case_7': {'first_name': "amr", 'last_name': "sobhy", 'email': 232323, 'ply_id': 4605, 'project_id': 1},
                'case_8': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': "ffd",
                           'project_id': 1},
                'case_9': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': "4605",
                           'project_id': 1},
                'case_10': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': "",
                            'project_id': 1},
                'case_11': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': 4605,
                            'project_id': "dffd"},
                'case_12': {'first_name': "amr", 'last_name': "sobhy", 'email': "002@mailinator.com", 'ply_id': 4605,
                            'project_id': ""}
            }
            i = 1
            expected_output = {
                "invalid email", "invalid project id", "invalid project key", "invalid token",
                "invalid device id", "invalid email", "invalid player id", "invalid project secret"
            }
            result_response = []

            for key, value in test_data_object.items():

                response = up_inv_contacts(value)
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
