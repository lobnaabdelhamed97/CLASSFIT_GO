import unittest
from utils.player_utils import *
from controllers.game_controller import *


class MyTestCase(unittest.TestCase):
    def test_gm_plys(self):
        output = "something happened:"
        gm_id = 3521
        limit_start = 0
        limit_number = 50
        ply_id = 1503
        org_id = 1503
        project_id = 1
        response = gm_plys(gm_id, limit_start, limit_number, ply_id, org_id, project_id)
        print("response", "\n", response)
        assert json.dumps(output) not in json.dumps(response)


if __name__ == '__main__':
    unittest.main()
