import unittest

from controllers.game_controller import *
from utils.game_utils import *
from utils.notification_utils import *
from utils.player_utils import *
from utils.questionnaire_utils import *


class TestCase(unittest.TestCase):
    def test_get_game_player_data(self):
        response = get_game_player_data(game_id=1317, player_id=893, ProjectKey='1234', ProjectSecret='1234',
                                        tkn='d4f438b4912fb05ac804d3eead97b4b8ed809a8b', dev_id='100f11dc8b54fb87')
        print(response)
        self.assertTrue(response)

    def test_get_game_flags(self):
        output = "Something went wrong:"
        response = get_game_flags(game_id=0, player_id=6003)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_player_flags(self):
        output = "Something went wrong:"
        response = get_player_flags(game_id=264474, player_id=5286)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_notification_flags(self):
        output = "Something went wrong:"
        response = get_notification_flags(game_id=264474, player_id=5286)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_game_questionnaire_data(self):
        output = "Something went wrong:"
        response = get_game_questionnaire_data(game_id=264474)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_get_player_questionnaire_answers(self):
        output = "Something went wrong:"
        response = get_player_questionnaire_answers(game_id=264474, player_id=5286)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_withdrew(self):
        response = withdrew(
            data={'class_id': 269307, 'ply_id': 5286, 'source': 'web', 'ProjectSecret': "1234", 'ProjectKey': "1234"})
        print(response)


if __name__ == '__main__':
    unittest.main()
