import unittest

from utils.game_utils import *


class MyTestCase(unittest.TestCase):

    def test_create_charge(self):
        response = create_charge(ply_id=6311, class_id=284080, fees=100.00, currency_id=1, ProjectKey="1234",
                                 ProjectSecret="1234", dev_id='windows_Chrome_172.31.41.60',
                                 tkn='8740b5de60191ea54cda278105643aef6ab29b6a',
                                 pay_type='stripe')
        print("\n", response)
        self.assertTrue(response, "this player is not an attendee")

    def test_class_capacity(self):
        response = class_capacity(org_id=5952, ply_id=6311, class_id=247364)
        print("\n", response)
        self.assertTrue(response, "this player is not an attendee")

    def test_add_waitlisted_attendee(self):
        output = "Something went wrong:"
        response = add_waitlisted_attendee(class_id='$%^&', ply_id=0)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    #
    # def test_class_valid(self):
    #     response = class_valid(org_id=-7255, ply_id=0, class_id='')
    #     print(response)
    #     self.assertTrue(response, "this player is not an attendee")

    def test_class_type(self):
        output = "Something went wrong:"
        response = class_type(class_id=254502, org_id=5952)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_add_attendee_to_class(self):
        response = add_attendee_to_class(ply_id=6311, class_id=247364)
        print("\n", response)
        self.assertTrue(response, "this player is not an attendee")

    def test_check_pending_refund(self):
        output = "Something went wrong:"
        response = check_pending_refund(class_id=247364, ply_id=7797, org_id=5952,
                                        tkn='0df6f03dc38703bff5ef4f48135000398d67c8d9', dev_id='test',
                                        pay_type='stripe', pay_choice=1, fees=1, currency_id=1, ProjectKey=1234,
                                        ProjectSecret=1234, coupon_code='', join_type='credit')
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_paid_type(self):
        output = "Something went wrong:"
        response = paid_type(ply_id=7554, class_id=253881, fees=0.2, currency_id=1, ProjectKey="1234",
                             ProjectSecret="1234", dev_id='test', tkn='97b54a475e4c260a0e05d12d6835c4b6d43549b6',
                             pay_type=0, pay_choice=0, org_id=5952, coupon_code='657hdhs')
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_apply_coupon_to_fees(self):
        response = apply_coupon_to_fees(class_id=284080, coupon_code='789999', org_id=5952, fees=100.00)
        print("\n", response)
        self.assertTrue(response, "this player is not an attendee")

    def test_check_recurr_class(self):
        output = "Something went wrong:"
        response = check_recurr_class(class_id=264446, ply_id=3500)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_check_zoom_details(self):
        output = "Something went wrong:"
        response = check_zoom_details(class_id=264446)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    #                                               *** refund *** part ***

    def test_check_abs_type(self):
        output = "Something went wrong:"
        response = check_abs_type(class_id=81473, ply_id=1581, ProjectKey='1234', ProjectSecret='1234')
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_update_player_asrefunded(self):
        response = update_player_asrefunded(ply_id=7748, class_id=264446)
        print("\n" + response)
        self.assertTrue(response, "this player is not an attendee")

    def test_check_refund_policy(self):
        output = "Something went wrong:"
        response = check_refund_policy(class_id=264446, ply_id=3500)
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_refund_if_replaced(self):
        response = refund_if_replaced(ply_id=7748, class_id=264446)
        print("\n" + response)
        self.assertTrue(response, "this player is not an attendee")

    def test_check_type_payment(self):
        output = "Something went wrong:"
        response = check_type_payment(class_id=252339, ply_id=6600, ProjectSecret='1234',
                                      ProjectKey='1234')
        print(response)
        assert json.dumps(output) not in json.dumps(response)

    def test_fully_refunded_per_time(self):
        output = "Something went wrong:"
        response = fully_refunded_per_time(class_id=264446, policy_id=1)
        print(response)
        assert json.dumps(output) not in json.dumps(response)


if __name__ == '__main__':
    unittest.main()
