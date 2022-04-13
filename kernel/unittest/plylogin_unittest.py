import unittest
from controllers.admin_controller import player_login


class MyTestCase(unittest.TestCase):

    def test_ply_login(self):

        # No Email
        case_1 = {'Email': '', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '121'}
        # No Pass
        case_2 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': '', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '122'}

        # long
        case_3 = {'Email': 'dainijis@ob5d31gf3whzcoo.gadfjlksajflsloejgkfyhsfhf', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '119'}
        # long  Pass
        case_4 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': 'VACF101123123123123123123123129', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '120'}

        # invalid Email
        case_5 = {'Email': 'dainijisob5d31gf3whzcoo.ga', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '118'}
        # deactive  Email
        case_6 = {'Email': 'sa@wq.lo', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '130'}
        # unavailable Email
        case_7 = {'Email': 'john@doe.com', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '101'}
        # wrong Pass
        case_8 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': 'ABCD123', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '129'}
        # correct data web
        case_9 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': 'VACF101', 'source': 'web',
                  'DevID': 'fcc78fd5d99ead13', 'PlyTkn': 'cbf81f86b11a291ecb024d4757fb7e3a',
                  'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '200'}
        # correct ios data
        case_10 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': 'VACF101', 'source': 'ios',
                   'DevID': '23232323', 'PlyTkn': '',
                   'usrAppleID': '23', 'TimeZone': 'Africa%2FCairo', 'code': '200'}

        # correct android data
        case_11 = {'Email': 'dainijis@ob5d31gf3whzcoo.ga', 'Pass': 'VACF101', 'source': 'android',
                   'DevID': '23232323', 'PlyTkn': '',
                   'usrAppleID': '', 'TimeZone': 'Africa%2FCairo', 'code': '200'}

        cases = [case_1, case_2, case_3, case_4, case_5,
                 case_6, case_7, case_8, case_9, case_10, case_11]

        for i in range(len(cases)):
            print('test Case ', i + 1)

            response = player_login(data=cases[i])

            testValue = True
            if cases[i]['code'] not in str(response):
                testValue = False

            if testValue is False:
                raise Exception("error occurs in case " +
                                str(i + 1) + " and says " + str(response))


if __name__ == '__main__':
    unittest.main()
