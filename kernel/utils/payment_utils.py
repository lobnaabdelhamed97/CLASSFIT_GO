def get_game_payment_methods():
    """"
    desc: get game payment methods states
    input: game_id
    output: result{PayMethods:{gocardless,stripe}}
    """

    return {}


def get_player_payment_methods():
    """"
    desc: get player payment methods states
    input: player_id
    output: result[currPlyMethods:[gocardless,stripe,StCustomer: {Bank,Card},GcCustomer,StripeAccountType,PlyHasExpressDashCode]
    """
    return {}
