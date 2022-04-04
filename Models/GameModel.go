package Models

type Game struct {
	Gm_id               int    `json:"gm_id"`
	Gm_title            string `json:"gm_title"`
	Gm_org_id           int    `json:"gm_org_id"`
	Gm_sub_type_id      int    `json:"gm_sub_type_id"`
	Gm_display_org      string `json:"gm_display_org"`
	Gm_court_id         int    `json:"gm_court_id"`
	Gm_level_id         int    `json:"gm_level_id"`
	Gm_img              string `json:"gm_img"`
	Gm_s3_status        int    `json:"gm_s3_status"`
	Gm_gender           string `json:"gm_gender"`
	Gm_age              int    `json:"gm_age"`
	Gm_age_min          int    `json:"gm_age_min"`
	Gm_age_max          int    `json:"gm_age_max"`
	Gm_min_players      int    `json:"gm_min_players"`
	Gm_max_players      int    `json:"gm_max_players"`
	Gm_max_players_orig int    `json:"gm_max_players_orig"`
	Gm_date             string `json:"gm_date"`
	Gm_start_time       string `json:"gm_start_time"`
	Gm_end_time         string `json:"gm_end_time"`
}

type Players struct {
	Gm_id               int    `json:"gm_id"`
	Ply_fname           string `json:"ply_fname"`
	Ply_lname           string `json:"ply_lname"`
	Country_name        string `json:"country_name"`
}


func (b *Game) TableName() string {
	return "game"
}

func (b *Players) TableName() string {
	return "players"
}