import unittest
from utils.player_utils import *

# from main import app , payload

class TestPendPlayer(unittest.TestCase):

    def test_ply_org(self):
        try:
            
            test_data_object ={
            'case_1': {'organizer_id':1579 , 'player_id': 842, 'contact_id' : 384 ,'project_id':1},
            'case_2': {'organizer_id':-1 , 'player_id': 842, 'contact_id' : 384 ,'project_id':1},
            'case_3': {'organizer_id':"0" , 'player_id': 842, 'contact_id' : 384 ,'project_id':1},
            'case_4': {'organizer_id':1579 , 'player_id': "842", 'contact_id' : 384 ,'project_id':1},
            'case_5': {'organizer_id':1579 , 'player_id': -1, 'contact_id' : 384 ,'project_id':1},
            'case_6': {'organizer_id':1579 , 'player_id': 842, 'contact_id' : "384" ,'project_id':1},
            'case_7': {'organizer_id':1579 , 'player_id': 842, 'contact_id' : -1 ,'project_id':1},
            }
            i = 1
            expected_output = {
             "organizer id required" , "player id required","contact id required","{'fname': 'c', 'lname': 'm%20', 'email': 'amtesting94', 'gender': None, 'plyAge': None, 'plyImg': '', 'phone': '0999', 'type': 'contact'}"
            }
            result_response = []

            for key, value in test_data_object.items():

                response = get_player_org_contact_data(value)
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

    if __name__ == '__main__':
        unittest.main()
