import unittest
from controllers.game_controller import ViewGmsCal


class MyTestCase(unittest.TestCase):
    def test_View_Gms_Cal(self):
        pid = 1
        Lat = 50
        Long = 50
        GmDate = '%%'
        aid = [7977, 7977, 5957, 7977, 2215, 7977, 5957, 7977]
        source = ["android", "ios", "ios", "ios", "linux", 0, "android", "ios"]
        x = 0
        for z in aid:
            data = {"pid": pid, "Number": 50,
                    "PlyId": 5952, "GmDate": GmDate,
                    "aid": z, "daygroup": 1, #"Lat":Lat,"Long":Long,
                    "source": source[x], "limit": 0,"Month":"06","Year":2021,
                    "ProjectKey": "1234", "ProjectSecret": "1234", "Tkn": "033404b2ec151bf575b2a9733ad668a2a38c1e3d",
                    "dev_id": "windows_Chrome_156.194.162.122"
                    }
            x += 1
            print("data:", "\n", data)
            response = ViewGmsCal(data=data)
            print("response", "\n", response, "\n\n")
        # except:
        #     print(range(aid))
        #     pass


if __name__ == '__main__':
    unittest.main()
