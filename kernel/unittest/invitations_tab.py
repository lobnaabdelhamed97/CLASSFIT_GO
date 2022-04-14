import unittest

from controllers.game_controller import invitations_tab


class MyTestCase(unittest.TestCase):
    def test_invitations_tab(self):
        ply_ids = [5952, 7255, 6311, 6003, 6002]
        types = 'Rec'
        limit = [1, 0, 2, 1, 0.5]
        number = [50, 0, 1, 1, 0.5]
        Lat = 50
        Long = 50
        for i, j, k in zip(ply_ids, limit, number):
            data = {'PlyID': i, 'Type': types, 'Limit': j, 'Lat': Lat, 'Long': Long, 'Number': k, 'DayGroup': 1}
            response = invitations_tab(data=data)
            print("response", "\n", response, "\n\n")

    def test_invitations__tab(self):
        response = invitations_tab({'PlyID': "7255", 'Type': 'Rec', 'Limit': 1, 'Lat': 50, 'Long': 50, 'adminId': 5952})
        print("response", "\n", response, "\n\n")


if __name__ == '__main__':
    unittest.main()
