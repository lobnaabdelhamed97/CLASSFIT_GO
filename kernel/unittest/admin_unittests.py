import unittest

from controllers.admin_controller import *


class MyTestCase(unittest.TestCase):
    def test_remove_by_admin(self):
        response = remove_by_admin(
            data={"class_id": 283908, "PlyID": "5952", "ply_id": 6232, "source": "Web", "ProjectKey": "1234",
                  "ProjectSecret": "1234", "DevID": "mac_Chrome_172.31.41.60",
                  "Tkn": "3ca33c685027afeaf86749a039e4b3b6d2e085a8"})
        print("\n", response)
        self.assertTrue(response, "Error in data")

    def test_guest_actions(self):
        response = guest_actions(
            data={'ply_id': 6198, 'class_id': 264486, 'ProjectSecret': "1234", 'ProjectKey': "1234", 'source': 'web'})
        print("\n", response)
        self.assertTrue(response, "Error in data")

    def test_add_guest(self):
        response = add_guest(
            data={"GmID": 283908, "PlyID": "5952", "source": "Web", "GuestMail": "Aydieyasser@mailinator.com",
                  "GuestFname": "Ay%20die", "GuestLname": "",
                  "GuestCheckinStatus": "false", "ProjectKey": "1234", "ProjectSecret": "1234",
                  "dev_id": "mac_Chrome_172.31.41.60", "tkn": "3ca33c685027afeaf86749a039e4b3b6d2e085a8"})
        print("\n", response)
        self.assertTrue(response, "Error in data")

    def test_get_player_offline_payments_data(self):
        projectKey = ["1234", "1234"]
        projectSecret = ["1234", "1234"]
        playerId = ["5952", -2]
        # ************** Test With All *****************
        print("Test With All")
        for i in range(len(projectKey)):
            data = {
                "ProjectKey": projectKey[i], "ProjectSecret": projectSecret[i],
                "PlyID": playerId[i]
            }
            response = get_player_offline_payments_data(data)
            print("\n", data, "\n")
            print("\n", response)
        # ************** Test Without playerId *****************
        print("Test Without playerId")
        data = {
            "ProjectKey": "1234", "ProjectSecret": "1234",
        }
        response = get_player_offline_payments_data(data)
        print("\n", data, "\n")
        print("\n", response)
        # ************** Test Without ProjectKey *****************
        print("Test Without ProjectKey")
        data = {
            "ProjectSecret": "1234",
            "PlyID": "5952"
        }
        response = get_player_offline_payments_data(data)
        print("\n", data, "\n")
        print("\n", response)

        # ************** Test Without ProjectSecret **************
        print("Test Without ProjectSecret")
        data = {
            "ProjectKey": "1234",
            "PlyID": "5952"
        }
        response = get_player_offline_payments_data(data)
        print("\n", data, "\n")
        print("\n", response)

    def test_get_registered_contacts_data(self):
        contacts_emails = [
            ['am@mailinator.com', 'salma19922019@outlook.sa', 'dainijis@ob5d31gf3whzcoo.ga', 'Seifmohamed@yahoo.com'],
            ['am@mailin==ator.com', 'salma19922019@outlo==ok.sa', 'dainijis@ob5d31gf3whzc==oo.ga',
             'Seifmohamed@yah==oo.com']]
        for x in contacts_emails:
            data = {
                "pid": 1, "contacts_emails": x
            }
            print("\n", data, "\n")
            response = get_registered_contacts_data(data)
            print("\n", response)


if __name__ == '__main__':
    unittest.main()
