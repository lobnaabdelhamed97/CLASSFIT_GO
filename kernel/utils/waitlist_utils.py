def get_game_waitlist_players(waitlist):
    """"
    desc: get players in waiting list of game
    input: game_id
    output:[??]
    """
    # try:
    #     data = execute(f"SELECT ply_id , ply_fname , ply_lname , ply_email , ply_brithdate , (CASE ply_gender WHEN 'm' THEN 'Male' WHEN 'f' THEN 'Female' ELSE '' END) AS ply_gender,\
    #     ply_height , ply_h_unit , ply_weight , ply_w_unit , ply_email_sett , ply_brithdate_sett , ply_gender_sett , ply_city_sett,\
    #                     ply_city_id , city_name,ply_country_id,country_name , ply_img , TIMESTAMPDIFF(YEAR, ply_brithdate, CURDATE()) AS Age,\
    #                     IFNULL((SELECT inv_id FROM invitations WHERE inv_approve = 'p' AND inv_gm_id = {game_id} AND ( inv_ply_frm_id = ply_id OR inv_ply_to_id = ply_id)),0) AS IsReq\
    #                         FROM gm_waitlist\
    #                         LEFT JOIN players ON gm_wait_list_ply_id = ply_id\
    #                 LEFT JOIN city ON ply_city_id = city_id\
    #                 LEFT JOIN country ON ply_country_id = country_id\
    #                 WHERE gm_wait_list_gm_id = {game_id}\
    #                     AND gm_wait_list_withdrew = 0\
    #                     AND gm_wait_list_removed_by_admin = 0\
    #                 ORDER BY gm_wait_list_created LIMIT '0','1000'")
    #     if str(data).__contains__('Something went wrong'):
    #         raise Exception(data)
    #     return data
    # except Exception as e:
    #     return e.__str__()
    return {'Wait': []}
