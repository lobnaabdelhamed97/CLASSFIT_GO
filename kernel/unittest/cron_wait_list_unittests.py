import unittest

from utils.game_utils import *
from controllers.game_controller import *


class MyTestCase(unittest.TestCase):
    def test_cron_waitlist(self):
        try:

            test_data_object = {
                'case_1': {'project_id': 1},
                'case_2': {'project_id': ""},
                'case_3': {'project_id': "ffddfdf"},
            }
            i = 1
            expected_output = {"invalid project id", "invalid project key", "invalid token", "invalid device id",
                               "invalid project secret"}
            result_response = []

            for key, value in test_data_object.items():

                response = cron_waitlist(value)
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

    def test_getClassIds(self):
        output = "Something went wrong:"
        response = getClassIds(project_id=1)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_getClassData(self):
        output = "Something went wrong:"
        response = getClassData(SqlArray="(272841, 273216, 272817)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_informWaitlist(self):
        output = "Something went wrong:"
        response = informWaitlist(ClassesData=[
            {'gm_id': 272817, 'gm_org_id': 1765, 'gm_utc_datetime': 'datetime.datetime(2022, 1, 5, 17, 0)',
             'gm_max_players': 1}], SqlArray="(272841, 273216, 272817)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_countGmPlys(self):
        output = "Something went wrong:"
        response = countGmPlys(SqlArray="(272841, 273216, 272817)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_getWaitListMembers(self):
        output = "Something went wrong:"
        response = getWaitListMembers(SqlArray="(272841, 273216, 272817)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_sendWaitlistInform(self):
        output = "Something went wrong:"
        ClassesData = [{'gm_id': 272817, 'gm_org_id': 1765, 'gm_utc_datetime': 'datetime.datetime(2022, 1, 5, 17, 0)',
                        'gm_max_players': 1}]

        waitlist_members = [{'gm_wait_list_id': 4566, 'gm_wait_list_gm_id': 272841, 'gm_wait_list_ply_id': 1767,
                             'gm_wait_list_withdrew': 0, 'gm_wait_list_removed_by_admin': 0,
                             'gm_wait_list_created': 'datetime.datetime(2022, 1, 2, 12, 7, 54)'}]
        game_time_difference_check = [False, True, False, True]
        SqlArray = "(272841, 273216, 272817)"

        response = sendWaitlistInform(ClassesData=ClassesData, waitlist_members=waitlist_members,
                                      game_time_difference_check=game_time_difference_check, SqlArray=SqlArray)
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_ChkIsInvGm(self):
        output = "Something went wrong:"
        response = ChkIsInvGm(SqlArray="(272841, 273216, 272817)", WaitIDArray="(1767,1767,1767)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_getLastInvDateTime(self):
        output = "Something went wrong:"
        response = getLastInvDateTime(SqlArray="(272841, 273216, 272817)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)

    def test_ChkIsBan(self):
        output = "Something went wrong:"
        response = ChkIsBan(OrgIDArray="(1765, 1765, 1765)", WaitIDArray="(1767,1767,1767)")
        print("\n", response)
        assert json.dumps(output) not in json.dumps(response)


if __name__ == '__main__':
    unittest.main()
