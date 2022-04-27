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
	PlyID          string `json:"PlyID"`
	PlyFname       string `json:"PlyFname"`
	PlyLname       string `json:"PlyLname"`
	Country_name   string `json:"PlyCountry"`
	City_name      string `json:"PlyCty"`
	ContactID      int    `json:"ContactID"`
	Gm_ply_ply_id  int    `json:"-"`
	Guest_ply_id   int    `json:"-"`
	Privecy        string `json:"Privecy"`
	PlyType        string `json:"PlyType"`
	Ply_typed_city string `json:"-"`
}
type Input struct {
	Gm_id string `json:"Gm_id"`
}

type Final struct {
	Member   []Mem_info       `json:"member"`
	Waitlist []Wait_list_info `json:"waitlist"`
}

type Log_input struct {
	PostData []PostData
}

type PostData struct {
	PlyID      string
	Type       string
	ActionFrom int
	Limit      int
	SearchTxt  string
}

type Enter struct {
	Org_id    string
	Type      string
	SearchArr PostData
}
type Wait_list_info struct {
	Ply_id         string `json:"PlyID"`
	Ply_fname      string `json:"PlyFname"`
	Ply_lname      string `json:"PlyLname"`
	Country_name   string `json:"PlyCountry"`
	City_name      string `json:"PlyCty"`
	Ply_img        string `json:"PlyImg"`
	Privecy        string `json:"Privecy"`
	PlyType        string `json:"PlyType"`
	Ply_typed_city string `json:"-"`
}

type User_infoandflags struct {
	Custom_notification_reminder_status int    `json:"RemindStat"`
	Custom_notification_period          string `json:"RemindPeriod"`
	PlyID                               int    `json:"PlyID"`
	GmMem                               string `json:"GmMem"`
	Terms                               string `json:"IssetOrgTerms"`
	IsOrg                               string `json:"IsOrg"`
	IsMem                               string `json:"IsMem"`
	Offline_payments_status             string `json:"offline_payments_status"`
	Offline_payments_currency_amount    string `json:"offline_payments_currency_amount"`
}

type StripeData struct {
	CardName  string `json:"CardName"`
	CardLast4 string `json:"CardLast4"`
}

type Organizer_info struct {
	OrgID         int        `json:"OrgID"`
	PlyImg        string     `json:"PlyImg"`
	Ply_bio       string     `json:"Bio"`
	Ply_business  string     `json:"Business"`
	OrgName       string     `json:"OrgName"`
	StripeData    StripeData `json:"StripeData"`
	Ply_brithdate string     `json:"PlyBirthDate"`
	Ply_email     string     `json:"OrgEmail"`
	Terms         string     `json:"IssetOrgTerms"`
}

type Game_org_info struct {
	Gm_id                int    `json:"GmID"`                ///checkout	//org
	Gm_title             string `json:"GmT"`                 ///checkout  //org
	Gm_desc              string `json:"Desc"`                ///checkout  //org
	Gm_age               int    `json:"Age"`                 ///checkout   //org
	Gm_img               string `json:"GmImg"`               //check on gm_s3_status			///checkout   //org
	Gm_reqQues           int    `json:"GmReqQues"`           ////checkout  //org
	Gm_payment_type      string `json:"PayType"`             ///checkout   //org
	Gm_is_free           string `json:"IsFree"`              //org
	Gm_status            string `json:"GmStatus"`            ///checkout  ///org
	Gm_start_time        string `json:"STime"`               ////checkout   //org
	Gm_end_time          string `json:"ETime"`               ////checkout		//org
	Attend_type          string `json:"attendType"`          ////checkout   //org
	Zoom_url             string `json:"zoomUrl "`            //org
	Gm_utc_datetime      string `json:"UTCDateTime"`         ///checkout  //org
	Gm_available_to_join int    `json:"GmIsAvailableToJoin"` ///checkout  //org
	Gm_date              string `json:"GmDate"`              ////checkout  //org
	Gm_fees              string `json:"Fees"`                //org ///checkout
	Gm_loc_desc          string `json:"LocDesc"`             ///checkout  //org
	Gm_is_stop_recurred  string `json:"IsStopRecurred"`      ////checkout  //org
	Gm_scope             string `json:"Scope"`               //org
	Gm_policy_id         int    `json:"Gm_policy_id"`        //org

	Gm_s_type_name         string `json:"STypeName"` ////checkout  //org //get stype id from game then get stype name from gm s types
	Level_title            string `json:"LevelT"`    //org //get level id from game then get levelt from level
	Court_title            string `json:"CourtT"`    //org //get court id from game then get courtt name from court
	Policy_title           string `json:"PolicyT"`   //org //get policy id from game then get policyt name from policy
	
	Subscriptions          []string ///checkout		//org
	PlySubscriptions       []string ///checkout		//org
	ValidJoinSubscriptions []string ///checkout		//org
	InvalidPlySubscriptions []string
	IsHis                  string							//org
	ISRecurr               string 					///checkout			//org
	ParentState            string 					///checkout  //org
	GmIsPaused             string
	MemGm                  string ///checkout    //org
	GmPlys                 int    ////checkout    //org
	Days                   string ////checkout   //org
	SSTime                 string ////checkout  //org
	EETime                 string ////checkout  //org
	OrgCheckInData         string        //org
	WithdrawMess string ////checkout   ??????		//org
	PlyMethods   string ///checkout as currPlyMethods?????  //org
	InstructorData         string							//org
	GmImgThumb           string `json:"GmImgThumb"` ///checkout

}

type Game_details struct {
	Gm_id                  int    `json:"GmID"`  ///checkout	//org
	Gm_title               string `json:"GmT"`   ///checkout  //org
	Gm_org_id              int    `json:"OrgID"` ///checkout
	Gm_desc                string `json:"Desc"`  ///checkout  //org
	PlyID                  int    `json:"PlyID"`
	Gm_age                 int    `json:"Age"`        ///checkout   //org
	Gm_img                 string `json:"GmImg"`      //check on gm_s3_status			///checkout   //org
	Gm_reqQues             int    `json:"GmReqQues"`  ////checkout  //org
	Gm_payment_type        string `json:"PayType"`    ///checkout   //org
	Gm_is_free             string `json:"IsFree"`					//org
	Gm_status              string `json:"GmStatus"` ///checkout  ///org
	Gm_start_time          string `json:"STime"` ////checkout   //org
	Gm_end_time            string `json:"ETime"` ////checkout		//org
	Attend_type            string `json:"attendType"` ////checkout   //org
	Zoom_url               string `json:"zoomUrl "`  //org
	Gm_utc_datetime        string `json:"UTCDateTime"` ///checkout  //org
	Gm_max_players         int    `json:"MaxPly"`              ///checkout
	Gm_available_to_join   int    `json:"GmIsAvailableToJoin"` ///checkout  //org
	Gm_date                string `json:"GmDate"`     ////checkout  //org
	Gm_fees                string `json:"Fees"`     //org ///checkout
	Gm_loc_desc            string `json:"LocDesc"` ///checkout  //org
	OrgName                string `json:"OrgName"`        /////checkout
	Gm_is_stop_recurred    string `json:"IsStopRecurred"` ////checkout  //org
	Gm_loc_lat             string `json:"Lat"`
	Gm_loc_long            string `json:"Long"`
	Gm_gender              string `json:"Gdr"`              ////checkout
	Gm_currency_symbol     string `json:"Gm_currency_symbol"`           ///checkout
	Symbol					string `json:"Symbol"`
	Gm_scope			   string `json:"Scope"`    //org
	Gm_sub_type_id int    `json:"gm_sub_type_id"`
	Gm_display_org string `json:"gm_display_org"`
	ShowMem     		   string    `json:"ShowMem"` ///checkout //check if 1 from db then then true else false /////
	Level_title            string `json:"LevelT"`    //org //get level id from game then get levelt from level
	Court_title            string `json:"CourtT"`    //org //get court id from game then get courtt name from court
	Policy_title           string `json:"PolicyT"`   //org //get policy id from game then get policyt name from policy
	Gm_s_type_name         string `json:"STypeName"` ////checkout  //org //get stype id from game then get stype name from gm s types
	IsHis                  string `json:"IsHis"`							//org //done
	Gm_s3_status   int    `json:"gm_s3_status"` //done
	Gm_showMem     int    `json:"Gm_showMem"` ///checkout //check if 1 from db then then true else false ///// //done
	Gm_court_id    int    `json:"gm_court_id"` //done
	Gm_level_id    int    `json:"gm_level_id"`	//done
	Gm_policy_id    int    `json:"Gm_policy_id"` //org  //done
	Gm_recurr_times	int
	Gm_recurr_id	int    `json:"RecurrID"`
	Gm_recurr_type  string
	Currency_name           string `json:"CurrencyName"`     ///checkout
	MemGm                  string ///checkout    //org
	ISRecurr               string 					///checkout			//org
	ParentState            string 					///checkout  //org
	PlyMethods   string ///checkout as currPlyMethods?????  //org //get_ply_verified_methods in kernel
	GmImgThumb           string `json:"GmImgThumb"` ///checkout
	Subscriptions          []string  `json:"Subscriptions"` ///checkout		//org //curl on bundles
	PlySubscriptions       []string `json:"PlySubscriptions"`///checkout		//org //curl on bundles
	ValidJoinSubscriptions []string ///checkout		//org //curl on bundles
	InvalidPlySubscriptions []string
	OrgOfflineStatus       string `json:"OrgOfflineStatus"` ///checkout //curl on payment status
	SSTime                 string ////checkout  //org
	EETime                 string ////checkout  //org
	Day                    string ///checkout
	Days                   string ////checkout   //org
	GmPlys                 int    ////checkout    //org //get_players_count_in_game in kernel
	InstructorData         string							//org

//not in kernel
	AllowRejoin            string `json:"AllowRejoin"`      ///checkout
	PlyStatus              string `json:"PlyStatus"`        ///checkout
	GmIsPaused             string
	OrgCheckInData         string        //org
	HasStopDays            string ////checkout

	//try to delete after finishing

}

type Ply_Methods struct {
	Stripe_users_account_id string `json:"-"`
}

type Count_game struct {
	Gm_ply_ply_id int `json:"-"`
}
type PP struct {
	GmID      int
	GmRecurID int
}

type Instructor struct {
	Instructor_id int    `json:"id"`
	Name          string `json:"name"`
	Bio           string `json:"bio"`
	Image         string `json:"image"`
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
type CountryCurrData struct {
	Currency_code                        string `json:"currency_code"`
	Currrency_symbol                     string `json:"currrency_symbol"`
	Currrency_symbol_formatted           string `json:"currrency_symbol_formatted"`
	Country_monthly_commission_cap       int    `json:"country_monthly_commission_cap"`
	Country_monthly_offline_payment_fees int    `json:"country_monthly_offline_payment_fees"`
}

type OfflinePayment struct {
	Result                      string          `json:"Result"`
	Status                      string          `json:"status"`
	Next_billing_date           string          `json:"next_billing_date"`
	Admin_country_currency_data CountryCurrData `json:"admin_country_currency_data"`
}

type BundleLoad struct{
	New_client	int `json:"new_client"`
	ProjectSecret string 
	ProjectKey string
	Dev_id string `json:"dev_id"`
	Ply_id  int `json:"ply_id"`
	Class_id int `json:"class_id"`
	Tkn string `json:"tkn"`
	Org_id int `json:"org_id"`
	Class_datetime string  `json:"class_datetime"`
}
type BundleOutput struct{
	Result string
	Message string
	OrgBundles          []string  `json:"Subscriptions"` ///checkout		//org //curl on bundles
	PlySubscriptions       []string `json:"PlySubscriptions"`///checkout		//org //curl on bundles
	ValidJoinSubscriptions []string ///checkout		//org //curl on bundles
	InvalidPlySubscriptions []string
}
