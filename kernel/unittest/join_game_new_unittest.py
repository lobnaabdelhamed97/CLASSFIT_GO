import unittest

from controllers.game_controller import join_class, withdrew


class MyTestCase(unittest.TestCase):
    def test_join_game(self):
        cases = {
            'case1': {'class_id': 284080, 'org_id': 5952, 'ply_id': 5286, 'pay_type': 'stripe', 'sub_id': 0,
                      'coupon_code': "", 'tkn': '2f8355f1d625f8eb84fb0c37428b1356e8383471',
                      'dev_id': 'windows_Chrome_172.31.28.243', 'pay_choice': 0, 'ProjectKey': 1234,
                      'ProjectSecret': 1234, 'join_type': "", 'fees': 100.00, 'currency_id': 1, 'source': 'web',
                      'gm_date': '2022-03-20'},
            'case2': {'class_id': 284080, 'org_id': 5952, 'ply_id': 6003, 'pay_type': 'stripe', 'sub_id': 0,
                      'coupon_code': "789999", 'tkn': 'aa3a7d634476f15116549ab295a63eac43fe3b2e',
                      'dev_id': 'windows_Chrome_172.31.23.87', 'pay_choice': 0, 'ProjectKey': 1234,
                      'ProjectSecret': 1234, 'join_type': "", 'fees': 100.00, 'currency_id': 1, 'source': 'web',
                      'gm_date': '2022-03-20'},
            'case3': {'class_id': 284133, 'org_id': 3500, 'ply_id': 6311, 'pay_type': '', 'sub_id': 6095,
                      'coupon_code': "", 'tkn': 'bfd38a283c4d501dd19b8b62ebae616965a5ac09',
                      'dev_id': 'windows_Chrome_172.31.41.60', 'pay_choice': 1, 'ProjectKey': 1234,
                      'ProjectSecret': 1234, 'join_type': "credit", 'fees': 100.00, 'currency_id': 1, 'source': 'web',
                      'gm_date': '2022-03-20'},
            'case4': {'class_id': 284136, 'org_id': 7255, 'ply_id': 6003, 'pay_type': '', 'sub_id': 0,
                      'coupon_code': "", 'tkn': 'aa3a7d634476f15116549ab295a63eac43fe3b2e',
                      'dev_id': 'windows_Chrome_172.31.23.87', 'pay_choice': 0, 'ProjectKey': 1234,
                      'ProjectSecret': 1234, 'join_type': "", 'fees': 0, 'currency_id': 1, 'source': 'web',
                      'gm_date': '2022-03-20'},
        }
        for key, value in cases.items():
            response = join_class(value)
            print(response)

    def test_withdrew(self):
        cases = {
            'case1': {'class_id': 284136, 'ply_id': 6003, 'source': 'web', 'ProjectSecret': "1234",
                      'ProjectKey': "1234"},
            'case2': {'class_id': 284080, 'ply_id': 6003, 'source': 'web', 'ProjectSecret': "1234",
                      'ProjectKey': "1234"},
            'case3': {'class_id': 284133, 'ply_id': 6311, 'source': 'web', 'ProjectSecret': "1234",
                      'ProjectKey': "1234"},
        }
        for key, value in cases.items():
            response = withdrew(value)
            print(response)


if __name__ == '__main__':
    unittest.main()
