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
	PlyID           string     `json:"PlyID"`
	PlyFname        string     `json:"PlyFname"`
	PlyLname        string     `json:"PlyLname"`
	Country_name    string     `json:"PlyCountry"`
	City_name       string     `json:"PlyCty"`
	ContactID       int        `json:"ContactID"`
	Gm_ply_ply_id   int        `json:"-"`
	Guest_ply_id    int        `json:"-"`
	Privecy         string     `json:"Privecy"`
	PlyType         string     `json:"PlyType"`
	Ply_typed_city  string      `json:"-"`
}
type Input struct {
	Gm_id string `json:"Gm_id"`
}

type Final struct {
     Member      []Mem_info         `json:"member"`
     Waitlist    []Wait_list_info   `json:"waitlist"`

}

type Log_input struct{
     PostData   []PostData
}

type PostData struct{
     PlyID           string
     Type            string
     ActionFrom      int
     Limit           int
     SearchTxt       string
  }

type Enter struct{
    Org_id           string
    Type             string
    SearchArr        PostData

}
type Wait_list_info struct {
	Ply_id          string     `json:"PlyID"`
	Ply_fname       string     `json:"PlyFname"`
	Ply_lname       string     `json:"PlyLname"`
	Country_name    string     `json:"PlyCountry"`
	City_name       string     `json:"PlyCty"`
    Ply_img         string     `json:"PlyImg"`
    Privecy         string     `json:"Privecy"`
    PlyType         string     `json:"PlyType"`
	Ply_typed_city  string     `json:"-"`
}

type User_infoandflags struct {
	Custom_notification_reminder_status int `json:"RemindStat"`
	Custom_notification_period string	`json:"RemindPeriod"`
	PlyID         int    `json:"PlyID"`
	GmMem	string    `json:"GmMem"`  
	Terms string `json:"IssetOrgTerms"`
	IsOrg string `json:"IsOrg"`
	IsMem string `json:"IsMem"`
	Offline_payments_status string `json:"offline_payments_status"`
	Offline_payments_currency_amount string `json:"offline_payments_currency_amount"`
}

type StripeData struct {
	CardName string `json:"CardName"`
	CardLast4 string `json:"CardLast4"`
}

type Organizer_info struct {
	PlyImg string `json:"PlyImg"`
	Ply_bio string `json:"Bio"`
	Ply_business string `json:"Business"`
	OrgName string `json:"OrgName"` 
	StripeData StripeData `json:"StripeData"`
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
type CountryCurrData struct{
	Currency_code string `json:"currency_code"`
	Currrency_symbol string  `json:"currrency_symbol"`
	Currrency_symbol_formatted string `json:"currrency_symbol_formatted"`
	Country_monthly_commission_cap int `json:"country_monthly_commission_cap"`
	Country_monthly_offline_payment_fees int `json:"country_monthly_offline_payment_fees"`
}

type OfflinePayment struct {
	Result string `json:"Result"`
	Status string `json:"status"`
	Next_billing_date string `json:"next_billing_date"`
	Admin_country_currency_data CountryCurrData  `json:"admin_country_currency_data"`
}

