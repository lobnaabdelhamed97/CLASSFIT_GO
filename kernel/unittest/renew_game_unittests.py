import unittest

from controllers.game_controller import renew_game


class TestRenewGame(unittest.TestCase):
    def setUp(self):
        # set some fixed variables
        # example: self.random_start = [0, 0, 0] 893
        self.game_date = "2023-02-20"
        self.game_date_utc = "Sun, 20 Feb 2023 13:00:00 GMT"
        pass

    def test_renew_game(self):
        response = renew_game(
            data={'game_id': 992, 'game_date_utc': self.game_date_utc, 'game_date': self.game_date,
                  'player_id': 7867, 'ProjectKey': '1234', 'ProjectSecret': '1234',
                  'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'})
        print("\n", response)
        self.assertTrue(response)

    # def test_renew_game(self):
    #     response = renew_game(
    #         data={'game_id': 992, 'game_date_utc': self.game_date_utc, 'game_date': self.game_date,
    #               'player_id': 893, 'ProjectKey':1234, 'ProjectSecret': 1234,
    #               'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'})
    #     print("\n", response)
    #     self.assertTrue(response)

    # def test_renew_game_missing_data(self):
    #     # response = renew_game(game_id = 992,game_date = "" , game_date_utc = self.game_date_utc ,project_id=1234,player_id=893, ProjectKey='1234', ProjectSecret='1234', tkn='d4f438b4912fb05ac804d3eead97b4b8ed809a8b', dev_id='100f11dc8b54fb87', modify_type = "onefuture")
    #     response = renew_game(
    #         data={'game_id': 992, 'game_date': "", 'game_date_utc': self.game_date_utc,
    #               'player_id': 893, 'ProjectKey': '1234', 'ProjectSecret': '1234',
    #               'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87',
    #               })
    #     print("\n", response)
    #     output = "something happened:"

    #     assert json.dumps(output) not in json.dumps(response)
    #     self.assertTrue(response)

    # def test_renew_game_wrong_date(self):
    #     response = renew_game(
    #         data={'game_id': 992, 'game_date': "2022-1-1", 'game_date_utc': "2022-1-1",
    #               'player_id': 893, 'ProjectKey': '1234', 'ProjectSecret': '1234',
    #               'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'})
    #     # response = renew_game(game_id = 992,game_date = "2022-1-1", game_date_utc = "2022-1-1" ,project_id=1234,player_id=893, ProjectKey='1234', ProjectSecret='1234', tkn='d4f438b4912fb05ac804d3eead97b4b8ed809a8b', dev_id='100f11dc8b54fb87', modify_type = "onefuture")
    #     print("\n", response)
    #     output = "something happened:"
    #     output2 = "Select upcoming time please"
    #     assert json.dumps(output) not in json.dumps(response)
    #     assert json.dumps(output2) not in json.dumps(response)
    #     self.assertTrue(response)

    # def test_renew_game_wrong_data_type(self):
    #     response = renew_game(
    #         data={'game_id': "992", 'game_date': "2022-1-1", 'game_date_utc': "2022-1-1",
    #               'player_id': 893, 'ProjectKey': '1234', 'ProjectSecret': '1234',
    #               'tkn': 'd4f438b4912fb05ac804d3eead97b4b8ed809a8b', 'dev_id': '100f11dc8b54fb87'})
    #     # response = renew_game(game_id = "992",game_date = "2022-1-1", game_date_utc = "2022-1-1" ,project_id=1234,player_id=893, ProjectKey='1234', ProjectSecret='1234', tkn='d4f438b4912fb05ac804d3eead97b4b8ed809a8b', dev_id='100f11dc8b54fb87', modify_type = "onefuture")
    #     print("\n", response)
    #     output = "something happened:"
    #     assert json.dumps(output) not in json.dumps(response)

    #     self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
