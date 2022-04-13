from database import execution


def get_instructor_date(game_id, game_recur_id, for_recur_only):
    return True


def get_IssetOrgTerms_key_for_game(admin_id):
    terms_info = execution.execute(f"SELECT * FROM admin_terms WHERE admin_id={admin_id}")
    if not terms_info:
        return "false"
    elif terms_info[0] and terms_info[0]["terms"]:
        return "true"
    else:
        return "false"
