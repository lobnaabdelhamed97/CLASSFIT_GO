import base64
import json
import sys

from controllers.admin_controller import *
from controllers.game_controller import *
from database.response import error
if __name__ == "__main__":
    if not sys.argv[1] or not sys.argv[2]:
        # use response error here
        print(error("error in arguments"))
        exit()
    data = sys.argv[2]
    payload = json.loads(base64.b64decode(data))
    route = sys.argv[1]

    if route == "join_class":
        print(join_class(payload))

    elif route == "view_game":
        print(view_game(payload))

    elif route == "checkPlayerAndContactWithOrganizer":
        print(checkPlayerAndContactWithOrganizer(payload))

    elif route == "withdraw_game":
        print(withdrew(payload))

    elif route == "edit_class":
        print(edit_class(payload))

    elif route == "cron_waitlist":
        print(cron_waitlist(payload))

    elif route == "up_inv_contacts":
        print(up_inv_contacts(payload))

    elif route == "renew_game":
        print(renew_game(payload))

    elif route == "checking_notification_for_player":
        print(check_notification(payload))

    elif route == "pending_player":
        print(pending_player(payload))

    elif route == 'remove_by_admin':
        print(remove_by_admin(payload))

    elif route == 'view_game_org_view':
        print(view_game_org_view(payload))

    elif route == 'add_guest':
        print(add_guest(payload))
    elif route == 'refund_handler':
        print(handleRefundPolicyMsg(payload))

    elif route == 'view_games_cal':
        print(ViewGmsCal(payload))

    elif route == 'getLastClassesAttendedWithOrganizer':
        print(getLastClassesAttendedWithOrganizer(payload))

    elif route == 'player_login':
        print(player_login(payload))

    elif route == 'view_contact':
        print(view_contact(payload))

    elif route == 'social':
        print(social(payload))
    elif route == 'invitations_tab':
        print(invitations_tab(payload))
    else:
        # handle 404 no route error
        print(error("route not found"))
        exit()
