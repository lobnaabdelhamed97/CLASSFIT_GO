import unittest
from controllers.game_controller import getLastClassesAttendedWithOrganizer


class MyTestCase(unittest.TestCase):
    def test_last_attended_with_org(self):

        playerId = [848, 842, 847, 852]
        organizerId = [852, 848, 842, 893]
        contactId = [65, 15, 17, 18]

        for player in playerId:
            for organizer in organizerId:
                data = {'playerId': player, 'organizerId': organizer}
                response = getLastClassesAttendedWithOrganizer(data=data)
                print("response", "\n", response)

        print(" testing contacts")

        for contact in contactId:
            for organizer in organizerId:
                data = {'contactId': contact, 'organizerId': organizer}
                response = getLastClassesAttendedWithOrganizer(data=data)
                print("response", "\n", response)


if __name__ == '__main__':
    unittest.main()
