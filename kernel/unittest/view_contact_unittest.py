import unittest

from controllers.admin_controller import view_contact


class MyTestCase(unittest.TestCase):

    def test_view_contact(self):

        cases = [5952, 852, 848, 842, 848, 893, 1717]

        data = {'PlyID': 0}

        for i in range(len(cases)):

            print('test Case ', i + 1)

            data['PlyID'] = cases[i]
            response = view_contact(data)

            testValue = True
            if '"code": 200' not in str(response):
                testValue = False

            if testValue is False:
                raise Exception("error occurs in case " +
                                str(i + 1) + " and says " + str(response))


if __name__ == '__main__':
    unittest.main()
