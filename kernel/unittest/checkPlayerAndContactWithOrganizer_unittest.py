import unittest

from controllers.admin_controller import checkPlayerAndContactWithOrganizer


class MyTestCase(unittest.TestCase):
    def test_something(self):

        organizerId = [848,-2,500,1518,1518]
        playerId = [848,-2,500,2215,500]
        contactId = [848,-2,500,500,5541]
        print("Testing without Contact ID************************************")
        for i in range(len(playerId)):
            data = {"organizerId" : organizerId[i],
                    "playerId":playerId[i],
                    }

            print("data:", "\n", data)
            response = checkPlayerAndContactWithOrganizer(data=data)
            print("response", "\n", response, "\n\n")

        print("Testing without PLayerID ID*************************************")
        for i in range(len(playerId)):
            data = {"organizerId" : organizerId[i],
                    "contactId":contactId[i],
                    }
            print("data:", "\n", data)
            response = checkPlayerAndContactWithOrganizer(data=data)
            print("response", "\n", response, "\n\n")


if __name__ == '__main__':
    unittest.main()
