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


if __name__ == '__main__':
    unittest.main()
