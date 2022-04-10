import datetime
import unittest
from controllers.game_controller import handleRefundPolicyMsg


class MyTestCase(unittest.TestCase):
    def test_RefundHandler(self):

        isFree = [1, 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                  'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
        PayType = ['offline', 1, 'offline', 'offline', 'offline', 'offline', 'offline', 'offline', 'offline', 'onsight',
                   'offline', 'offline', 'offline', 'offline', 'offline', 'offline', 'offline', 'offline', 'offline',
                   'offline', 'offline', 'offline', 'offline', 'offline']
        PolicyT = ['Refund', 'Refund', 1, 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund',
                   'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund',
                   'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund', 'Refund']
        PolicyID = [1, 2, 3, 'h', 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        GmPlys = [4, 4, 4, 4, 'h', 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 44, 4, 4, 4]
        MaxPly = [5, 5, 5, 55, 5, 'h', 5, 5, 5, 5, 5, 5, 5, 5, 55, 5, 5, 5, 5, 5]
        Symbol = ['61', '61', '61', '61', '61', '61', 7, '61', '61', '61', '61', '61', '61', '61', '61', '61', '61',
                  '61', '61''61']
        Fees = [500, 500, 500, 500, 500, 500, 500, 'skjdvn', 50, 505, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                5, 5, 5, 5, 5, 5, 5]
        UTC = ['03/01/2022, 14:58:06', '03/01/2022, 17:58:06', '03/01/2022, 20:58:06', '03/01/2022, 14:58:06',
               '03/01/2022, 14:58:06', '03/01/2022, 14:58:06', '03/01/2022, 14:58:06', '03/01/2022, 10:58:06',
               '02/28/2022, 14:58:06']

        c = 0
        for x in isFree:
            try:
                data = {"IsFree": x, "PayType": PayType[c], "PolicyT": PolicyT[c],
                        "PolicyID": PolicyID[c], "GmPlys": GmPlys[c],
                        "MaxPly": MaxPly[c], "Symbol": Symbol[c], "Fees": Fees[c],
                        "UTCDateTime": '03/01/2022, 14:58:06',
                        }
                c = c + 1
                response = handleRefundPolicyMsg(data=data)
                print("response", "\n", response)
            except:
                pass


if __name__ == '__main__':
    unittest.main()
