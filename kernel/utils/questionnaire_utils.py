from database import execution


def get_game_questionnaire_data(game_id):
    """"
    desc: get game questionnaire data
    input: game_id
    output:{GmQues: [{QuesID,QuesReq,QuesAns,QuesTitle,QuesType,QuesSortOrder}]}
    """
    try:
        if game_id and game_id > 0:
            checkQues = execution.execute(
                f"SELECT COUNT(gm_ques_id) AS count_data FROM gm_questionnaire WHERE gm_ques_gm_id = {game_id};")
            if "count_data" not in checkQues[0] or checkQues[0]["count_data"] <= 0:
                cloned_game = execution.execute(f"SELECT gm_copy_ques_from FROM game WHERE gm_id = {game_id};")
                if "gm_copy_ques_from" in cloned_game[0] and cloned_game[0]['gm_copy_ques_from'] > 0:
                    game_id = cloned_game[0]['gm_copy_ques_from']
            GmQues = execution.execute(
                "SELECT Distinct gm_ques_ques_id AS QuesID,adm_ques_ques_req AS QuesReq, adm_ques_ques_ans As QuesAns,ques_title AS QuesTitle, ques_type AS QuesType,ques_sort_order AS QuesSortOrder "
                "FROM gm_questionnaire join game on gm_id=gm_questionnaire.gm_ques_gm_id JOIN admin_ques ON (adm_ques_adm_id = game.gm_org_id and adm_ques_stype_id =gm_ques_stype_id "
                f"and adm_ques_ques_id = gm_ques_ques_id) JOIN questionnaire ON gm_ques_ques_id = ques_id WHERE  gm_ques_gm_id = {game_id} ORDER BY FIELD(ques_type, 'text') ASC, questionnaire.ques_sort_order Asc ,questionnaire.ques_id Asc ;")
            if GmQues:
                return {"GmQues": GmQues}
            else:
                return {"GmQues": []}
        else:
            raise Exception("game id is required")
    except Exception as e:
        return e.__str__()


def get_player_questionnaire_answers(game_id, player_id):
    """"
    desc: get game questionnaire data
    input: game_id,player_id
    output:{“PlyAnswers”: [{QuesID,PlyAns}]}
    """
    try:
        if game_id and game_id > 0 and player_id and int(player_id) > 0:
            answers_ques = execution.execute(
                "SELECT DISTINCT ply_ques_ques_id AS QuesID,(CASE WHEN (ques_type != 'radio') THEN ply_ques_ques_answer WHEN (ques_type = 'radio' && ply_ques_ques_answer = 0) THEN 'no' "
                "WHEN (ques_type = 'radio' && ply_ques_ques_answer = 1) THEN 'yes' END ) AS PlyAns "
                "FROM ply_questionnaire JOIN questionnaire ON questionnaire.ques_id = ply_questionnaire.ply_ques_ques_id "
                f"JOIN gm_questionnaire ON gm_questionnaire.gm_ques_ques_id = ply_questionnaire.ply_ques_ques_id WHERE ply_ques_ply_id = {player_id} AND gm_ques_gm_id = {game_id} ORDER BY FIELD(ques_type, 'text') ASC, questionnaire.ques_sort_order Asc ,questionnaire.ques_id Asc ;")
            if answers_ques:
                return {'PlyAnswers': answers_ques}
            else:
                return {'PlyAnswers': []}
        else:
            raise Exception("game id and player id are required")
    except Exception as e:
        return e.__str__()
