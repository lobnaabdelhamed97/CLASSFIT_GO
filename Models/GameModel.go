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

 func (b *Game) TableName() string {
  	return "game"
 }

type Mem_info struct {
	PlyID         string     `json:"PlyID"`
	PlyFname      string     `json:"PlyFname"`
	PlyLname      string     `json:"PlyLname"`
	Country_name  string     `json:"PlyCountry"`
	City_name     string     `json:"PlyCty"`
	ContactID     int        `json:"ContactID"`
	Gm_ply_ply_id int        `json:"-"`
	Guest_ply_id  int        `json:"-"`
	Privecy       string     `json:"Privecy"`
	PlyType       string     `json:"PlyType"`
}
type Input struct {
	PlyID string `json:"PlyID"`
	Gm_id string `json:"Gm_id"`
}

type Wait_list_info struct {
	PlyID         string     `json:"PlyID"`
	PlyFname      string     `json:"PlyFname"`
	PlyLname      string     `json:"PlyLname"`
	Country_name  string     `json:"PlyCountry"`
	City_name     string     `json:"PlyCty"`
    Ply_img       string     `json:"PlyImg"`
    Privecy       string     `json:"Privecy"`
}

type Wait_list_input struct {
	Gm_id string `json:"Gm_id"`
}


type User_infoandflags struct {
	Custom_notification_reminder_status int `json:"RemindStat"`
	Custom_notification_period string	`json:"RemindPeriod"`
	PlyID         int    `json:"PlyID"`
	GmMem	string    `json:"GmMem"`  

}

type ViewGame struct {
	GmID          int    `json:"GmID"`
	PlyID         int    `json:"PlyID"`
	ProjectSecret string `json:"ProjectSecret"`
	ProjectKey    string `json:"ProjectKey"`
	Tkn           string `json:"Tkn"`
	DevID         string `json:"DevID"`
	Source        string `json:"source"`
}
