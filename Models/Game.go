package Models

import (
	"encoding/json"
	"errors"
	"strconv"
	"strings"
	"net/url"
	_ "github.com/go-sql-driver/mysql"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Helper"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"time"
	//  "fmt"
	//  "github.com/leekchan/timeutil"
)

func GetAllGames(game *Game) (err error) {
	if err = Config.DB.Find(game).Error; err != nil {
		return err
	}
	return nil
}

func CreateGame(game *Game) (err error) {
	if err = Config.DB.Create(game).Error; err != nil {
		return err
	}
	return nil
}

func GetGameByID(game *Game, id string) (err error) {
	if err = Config.DB.Where("gm_id = ?", id).First(game).Error; err != nil {
		return err
	}
	return nil
}

func UpdateGame(game *Game) (err error) {
	Config.DB.Save(game)
	return nil
}

func DeleteGame(game *Game, id string) (err error) {
	Config.DB.Where("gm_id = ?", id).Delete(game)

	return nil
}
func (v *ViewGame) Validate() error {

	if v.GmID < 0 {
		return errors.New("required Game ID")
	}
	if v.PlyID < 0 {
		return errors.New("required Player ID")
	}
	if v.DevID == "" {
		return errors.New("required Device ID")
	}
	if v.Source == "" {
		return errors.New("required Source")
	}
	if v.Tkn == "" {
		return errors.New("required token")
	}
	if v.ProjectKey == "" {
		return errors.New("required project key")
	}
	if v.ProjectSecret == "" {
		return errors.New("required project Secret")
	}
	return nil
}

// Userinfoandflags func (v *User_infoandflags) Validate() error {
// 	if v.GmID < 0 {
// 		return errors.New("required Game ID")
// 	}
// 	if v.PlyID < 0 {
// 		return errors.New("required Player ID")
// 	}
// 	return nil
// }

func Userinfoandflags(in *ViewGame, user_infoandflags *User_infoandflags) (err error) {
	if err = Config.DB.Table("custom_notifications").Where("custom_notification_gm_id = ? AND custom_notification_ply_id = ?", in.GmID, in.PlyID).Select("custom_notification_reminder_status, custom_notification_period").Scan(&user_infoandflags).Error; err != nil {
		if string(err.Error()) == "record not found" {
			user_infoandflags.Custom_notification_reminder_status = 0
			user_infoandflags.Custom_notification_period = ""
		} else {
			return err
		}
	}
	user_infoandflags.PlyID = in.PlyID
	if err = Config.DB.Table("admin_terms").Where("admin_id = ?", in.PlyID).Select("terms").Scan(&user_infoandflags).Error; err != nil {
		if string(err.Error()) == "record not found" {
			user_infoandflags.Terms = "false"
		} else {
			return err
		}
	}
	user_infoandflags.PlyID = in.PlyID
	if err = Config.DB.Table("admin_terms").Where("admin_id = ?", in.PlyID).Select("terms as Terms").Scan(&user_infoandflags).Error; err != nil {
		if string(err.Error()) == "record not found" {
			user_infoandflags.Terms = "false"
		} else {
			return err
		}
	}
	if user_infoandflags.Terms != "false" {
		user_infoandflags.Terms = "true"
	}
	type IdDummy struct {
		Gm_org_id int
		Gm_ply_id int
	}
	var iddata IdDummy
	if err = Config.DB.Table("gm_players").Where("gm_ply_gm_id = ? AND gm_ply_ply_id = ? AND gm_ply_status = 'y'", in.GmID, in.PlyID).Select("gm_ply_id").Scan(&iddata).Error; err != nil {
		if string(err.Error()) == "record not found" {
			user_infoandflags.GmMem = "no"
		} else {
			return err
		}
	}
	if user_infoandflags.GmMem != "no" {
		user_infoandflags.GmMem = "mem"
	}
	if err = Config.DB.Table("game").Where("gm_id = ?", in.GmID).Select("gm_org_id").Scan(&iddata).Error; err != nil {
		return err
	}
	if iddata.Gm_org_id == in.PlyID {
		user_infoandflags.IsOrg = "true"
	} else {
		user_infoandflags.IsOrg = "false"
	}
	if err = Config.DB.Table("gm_players").Where("gm_ply_gm_id = ? AND gm_ply_ply_id = ? AND gm_ply_status = 'y' AND (gm_ply_leave IS NULL OR gm_ply_leave = '')", in.GmID, in.PlyID).Select("gm_ply_id").Scan(&iddata).Error; err != nil {
		if string(err.Error()) == "record not found" {
			user_infoandflags.IsMem = "false"
		} else {
			return err
		}
	}
	if user_infoandflags.IsMem != "false" {
		user_infoandflags.IsMem = "true"
	}
	keysec := Helper.KeySecured(in.ProjectKey, in.ProjectSecret)
	values, err := json.Marshal(in)
	body := Helper.PaymentCurl(keysec, "https://v2.classfit.com/payment/offline/admin/data", values, "application/json")

	var payment OfflinePayment
	err = json.Unmarshal(body, &payment)
	if err != nil {
		return err
	}
	user_infoandflags.Offline_payments_status = payment.Status
	OffPayment := payment.Admin_country_currency_data.Country_monthly_offline_payment_fees
	if OffPayment < 0 {
		OffPayment = 15
	}
	Symbol := payment.Admin_country_currency_data.Currrency_symbol_formatted
	if Symbol == "" {
		Symbol = payment.Admin_country_currency_data.Currrency_symbol
		if Symbol == "" {
			Symbol = "US$"
		}
	}
	user_infoandflags.Offline_payments_currency_amount = Symbol + strconv.Itoa(OffPayment)
	return nil
}

func Organizerinfo(in *ViewGame, organizer_info *Organizer_info) (err error) {
	type IdDummy struct {
		Gm_org_id int
	}
	var iddata IdDummy
	if err = Config.DB.Table("game").Where("gm_id = ?", in.GmID).Select("gm_org_id").Scan(&iddata).Error; err != nil {
		return err
	}
	organizer_info.OrgID = iddata.Gm_org_id
	if err = Config.DB.Table("players").Where("ply_id = ?", iddata.Gm_org_id).Select("ply_bio,ply_business,ply_brithdate,ply_email").Scan(&organizer_info).Error; err != nil {
		return err
	}
	organizer_info.Ply_bio, _ = url.PathUnescape(organizer_info.Ply_bio)
	organizer_info.Ply_bio = url.PathEscape(organizer_info.Ply_bio)
	organizer_info.Ply_business, _ = url.PathUnescape(organizer_info.Ply_business)
	organizer_info.Ply_business = url.PathEscape(organizer_info.Ply_business)
	type Name struct {
		Ply_fname string
		Ply_lname string
	}
	var name Name
	if err = Config.DB.Table("players").Where("ply_id = ?", iddata.Gm_org_id).Select("ply_fname,ply_lname").Scan(&name).Error; err != nil {
		return err
	}
	name.Ply_fname, _ = url.PathUnescape(name.Ply_fname)
	name.Ply_lname, _ = url.PathUnescape(name.Ply_lname)
	organizer_info.OrgName = name.Ply_fname + " " + name.Ply_lname

	type Image struct {
		Aws_server string
		Ply_img    string
		S3_profile int
	}
	var image Image
	if err = Config.DB.Table("players").Where("ply_id = ?", iddata.Gm_org_id).Select("ply_img,s3_profile").Scan(&image).Error; err != nil {
		return err
	}
	image.Aws_server = "https://classfit-assets.s3.amazonaws.com/"
	if image.S3_profile == 1 {
		organizer_info.PlyImg = image.Aws_server + image.Ply_img
	} else {
		organizer_info.PlyImg = image.Aws_server + "backup/images/upload/ply/" + image.Ply_img
	}
	type CustomerID struct {
		Stripe_users_cust_id string
		Stripe_users_card_id string
	}
	var customerID CustomerID
	if err = Config.DB.Table("stripe_users").Where("stripe_users_ply_id = ?", iddata.Gm_org_id).Select("stripe_users_cust_id,stripe_users_card_id").Scan(&customerID).Error; err != nil {
		return err
	}
	organizer_info.StripeData.CardName, organizer_info.StripeData.CardLast4, err = Helper.RetrieveData(customerID.Stripe_users_cust_id, customerID.Stripe_users_card_id)
	if err != nil {
		organizer_info.StripeData.CardName = ""
		organizer_info.StripeData.CardLast4 = ""
	}
	if err = Config.DB.Table("admin_terms").Where("admin_id = ?", in.PlyID).Select("terms").Scan(&organizer_info).Error; err != nil {
		if string(err.Error()) == "record not found" {
			organizer_info.Terms = "false"
		} else {
			return err
		}
	}
	if organizer_info.Terms != "false" {
		organizer_info.Terms = "true"
	}
	return nil
}

func (validate *Input) Validate() error {
	Gm_id, _ := strconv.Atoi(validate.Gm_id)
	if Gm_id <= 0 {
		return errors.New("GmID Required")
	}

	return nil
}

func Member_info(validate *Input, mem_info *[]Mem_info, wait_list_info *[]Wait_list_info) (final Final, err error) {

	if err = Config.DB.Table("players").Select("distinct ply_id, ply_fname ,ply_lname ,country_name, city_name,typed_city,contact_id,gm_ply_ply_id,guest_ply_id,CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS privecy").
		Joins("LEFT JOIN country ON ply_country_id= country_id").Joins("LEFT JOIN ply_typed_city ON player_id = ply_id").Joins("LEFT JOIN city ON ply_city_id = city_id").Joins("LEFT JOIN gm_players ON gm_ply_ply_id=ply_id and gm_ply_gm_id= " + validate.Gm_id + " ").
		Joins("LEFT JOIN guests ON guest_ply_id=gm_ply_ply_id and guest_gm_id= " + validate.Gm_id + " ").Joins("LEFT JOIN contacts ON contact_ply_id = ply_id and contact_org_id IN (SELECT gm_org_id from game WHERE gm_id= " + validate.Gm_id + ") ").Where("gm_ply_gm_id= " + validate.Gm_id + " AND gm_ply_status = 'y' AND gm_ply_removed_by_admin = 0 ").
		Scan(&mem_info).Error; err != nil {
		return final, errors.New("no Available Data")
	}
	for i := 0; i < len(*mem_info); i++ {
		if (*mem_info)[i].Gm_ply_ply_id > 0 && (*mem_info)[i].Guest_ply_id == 0 {
			(*mem_info)[i].PlyType = "member"
		} else if ((*mem_info)[i].Gm_ply_ply_id == 0 && (*mem_info)[i].Guest_ply_id > 0) || ((*mem_info)[i].Gm_ply_ply_id > 0 && (*mem_info)[i].Guest_ply_id > 0) {
			(*mem_info)[i].PlyType = "guest"
		}

		if (*mem_info)[i].City_name == "" && (*mem_info)[i].Ply_typed_city != "" {
			(*mem_info)[i].City_name = (*mem_info)[i].Ply_typed_city
		}
	}

	if err = Config.DB.Table("players").Select("ply_fname,ply_lname,country_name,city_name,ply_id,typed_city,CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS privecy,ply_img").
		Joins("LEFT JOIN country ON ply_country_id= country_id").Joins("LEFT JOIN city ON ply_city_id = city_id").
		Joins("LEFT JOIN gm_waitlist ON gm_wait_list_ply_id= ply_id").Joins("LEFT JOIN ply_typed_city ON player_id = gm_wait_list_ply_id").
		Where("gm_wait_list_gm_id= " + validate.Gm_id + " AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0").Scan(&wait_list_info).Error; err != nil {
		return final, errors.New("no Available Data")
	}
	for i := 0; i < len(*wait_list_info); i++ {
		(*wait_list_info)[i].PlyType = "member"
		(*wait_list_info)[i].Ply_img = "https://classfit-assets.s3.amazonaws.com/backup" + (*wait_list_info)[i].Ply_img

		if (*wait_list_info)[i].City_name == "" && (*wait_list_info)[i].Ply_typed_city != "" {
			(*wait_list_info)[i].City_name = (*wait_list_info)[i].Ply_typed_city
		}
	}

	final = Final{Member: *mem_info, Waitlist: *wait_list_info}

	return final, nil
}
func CommonGameKeys(in *ViewGame, game_details *Game_details) (game *Game_details, err error) {
	res1 := strings.Split(game_details.Gm_utc_datetime, "T")
	res2 := strings.Split(res1[1], "+")
	game_details.Gm_date=res1[0]
	game_details.Gm_utc_datetime=res1[0]+" "+res2[0]

	if game_details.Gm_recurr_times > 0 && game_details.Gm_recurr_type != "" {
		game_details.ParentState = "p"
	} else if game_details.Gm_recurr_id > 0 {
		game_details.ParentState = "c"
	}
	if game_details.Gm_s3_status == 1 {
		Gm_img := game_details.Gm_img
		game_details.Gm_img = "https://classfit-assets.s3.amazonaws.com" + game_details.Gm_img
		Gm_img = strings.ReplaceAll(Gm_img, "classes", "classes/thumb")
		game_details.GmImgThumb = "https://classfit-assets.s3.amazonaws.com" + Gm_img
	} else {
		game_details.Gm_img = "https://classfit-assets.s3.amazonaws.com" + "/images/upload/gm/" + game_details.Gm_img
		game_details.GmImgThumb = "https://classfit-assets.s3.amazonaws.com" + "/images/upload/gm/thumb/" + game_details.Gm_img
	}

//time part donot forget
type TimeResult struct {
	Id int
	Timezone string
}
var timeresult TimeResult

if err := Config.DB.Table("ply_timezone").Select("id,timezone").Where("player_id = ?", in.PlyID).Scan(&timeresult).Error; err != nil {
return nil,err}

if timeresult.Id>0 && timeresult.Timezone != "" {
	timeresult.Timezone, _ = url.PathUnescape(timeresult.Timezone)
	t, err := time.Parse("2006-01-02", game_details.Gm_date)
if err != nil {
   return nil,err
}
game_details.Day=t.Weekday().String()
myDate, err := time.Parse("2006-01-02 15:04:00", game_details.Gm_utc_datetime)
game_details.SSTime=myDate.Format("03:04 PM")
// td:= timeutil.Timedelta{Minutes: game_details.Gm_end_time}

//     result := myDate.Add(td.Duration())
//     fmt.Println(result)
// game_details.EETime= result.String()

}

	type Result struct {
		Contact_id int `json:"Contact_id"`
	}
	var result Result
	var new_client int
	if err := Config.DB.Table("contacts").Select("contact_id").Where("contact_org_id = ? and contact_ply_id = ?", game_details.Gm_org_id, in.PlyID).Scan(&result).Error; err != nil {
		if string(err.Error()) == "record not found" {
			new_client = 1
		} else {
			return nil, err
		}
	}
	data := url.Values{}

	data.Set("new_client", strconv.Itoa(new_client))
	data.Set("ProjectSecret", in.ProjectSecret)
	data.Set("ProjectKey", in.ProjectKey)
	data.Set("dev_id", in.DevID)
	data.Set("ply_id", strconv.Itoa(in.PlyID))
	data.Set("class_id", strconv.Itoa(in.GmID))
	data.Set("tkn", in.Tkn)
	data.Set("org_id", strconv.Itoa(game_details.Gm_org_id))
	data.Set("class_datetime", game_details.Gm_utc_datetime)
	keysec := Helper.KeySecured(in.ProjectKey, in.ProjectSecret)
	body := Helper.BundleCurl(keysec, "https://v2.classfit.com/bundles/playerBundles", data, "application/x-www-form-urlencoded")
	var output BundleOutput
	err = json.Unmarshal(body, &output)
	if err != nil {
		return nil, err
	}
	if output.Result=="error"{
		return nil,errors.New(output.Message)
	}
game_details.Subscriptions=output.OrgBundles
game_details.PlySubscriptions=output.PlySubscriptions
game_details.ValidJoinSubscriptions=output.ValidJoinSubscriptions
game_details.InvalidPlySubscriptions=output.InvalidPlySubscriptions
in.PlyID=game_details.Gm_org_id
values, err := json.Marshal(in)
body = Helper.PaymentCurl(keysec, "https://v2.classfit.com/payment/offline/admin/status", values, "application/json")
var payment OfflinePayment
err = json.Unmarshal(body, &payment)
if err != nil {
	return nil,err
}
game_details.OrgOfflineStatus = payment.Status

	return game_details, nil
}

func Get_ply_verified_methods(PlyID int) (data string) {
	if PlyID < 1 {
		return ""
	}
	var result Ply_Methods
	if err := Config.DB.Table("stripe_users").Select("stripe_users_account_id").Where("stripe_users_ply_id = " + strconv.Itoa(PlyID) + " ").Scan(&result).Error; err != nil {
		return ""
	}
	data = "n"
	if result.Stripe_users_account_id != "" {
		data = "y"
	}
	return data
}

func GetGmInstructorData(GmID int, GmRecurID int) (inst_data Instructor) {
	if GmID < 1 {
		return inst_data
	}
	var check Instructor
	Config.DB.Raw("SELECT instructor_id, name, bio, image FROM gm_instructors_parents_only JOIN instructors ON instructors.id = gm_instructors_parents_only.instructor_id WHERE gm_id = " + strconv.Itoa(GmID) + "  ").Scan(&inst_data)
	if inst_data == check {
		Config.DB.Raw("SELECT instructor_id, name, bio, image FROM gm_instructors JOIN instructors ON instructors.id = gm_instructors.instructor_id WHERE gm_id = " + strconv.Itoa(GmID) + " ").Scan(&inst_data)
	}
	if inst_data == check && GmRecurID > 0 {
		type Game struct {
			Gm_copy_id int
		}
		var game_copy_id Game
		Config.DB.Table("game").Select("gm_copy_id").Where("gm_id= " + strconv.Itoa(GmID) + " ").Scan(&game_copy_id)
		if game_copy_id.Gm_copy_id > 0 {
			GmRecurID = game_copy_id.Gm_copy_id
		}
		Config.DB.Raw("SELECT instructor_id, name, bio, image FROM gm_instructors JOIN instructors ON instructors.id = gm_instructors.instructor_id WHERE gm_id = " + strconv.Itoa(GmRecurID) + " ").Scan(&inst_data)
	}
	return inst_data
}

func Get_players_count_in_game(Gm_id int, result *[]Count_game) (players int) {
	if Gm_id < 1 {
		return 0
	}
	if err := Config.DB.Raw("SELECT gm_ply_ply_id FROM gm_players where gm_ply_gm_id= " + strconv.Itoa(Gm_id) + " Union ALL SELECT guest_ply_id FROM guests WHERE guest_gm_id= " + strconv.Itoa(Gm_id) + " ").Scan(&result).Error; err != nil {
		return 0
	}
	unique := make([]int, 0)
	for i := 0; i < len(*result); i++ {
		unique = append(unique, (*result)[i].Gm_ply_ply_id)
	}
	keys := make(map[int]bool)
	var list []int
	for _, entry := range unique {
		if _, value := keys[entry]; !value || entry == 0 {
			keys[entry] = true
			list = append(list, entry)
		}
	}
	return len(list)
}

func GameDetails(in *ViewGame, game_details *Game_details) (err error) {
	if err = Config.DB.Table("game").Where("gm_id = ? AND (gm_status IS NULL OR gm_status NOT LIKE '%deleted%')", in.GmID).Select("gm_org_id,gm_id,gm_title,gm_desc,gm_age,gm_reqQues,gm_payment_type,gm_is_free,gm_status,gm_start_time,gm_end_time,attend_type,zoom_url,gm_utc_datetime,gm_max_players,gm_available_to_join,gm_date,gm_fees,gm_loc_desc,gm_is_stop_recurred,gm_loc_lat,gm_loc_long,gm_img,gm_scope,gm_gender,gm_currency_symbol,gm_display_org,gm_showMem,gm_sub_type_id,gm_s_type_name,gm_court_id,gm_level_id,gm_policy_id,level_title,court_title,policy_title,gm_s3_status,gm_recurr_times,gm_recurr_type,gm_recurr_id,currency_name,(CASE WHEN ((gm_org_id = " + strconv.Itoa(in.PlyID) + " && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP) OR (gm_org_id != " + strconv.Itoa(in.PlyID) + " && (gm_utc_datetime + INTERVAL gm_end_time MINUTE) >= CURRENT_TIMESTAMP)) THEN 'n' ELSE 'y' END) AS IsHis").Joins("FULL JOIN players org ON gm_org_id =org.ply_id" + " left JOIN gm_s_types ON gm_sub_type_id = gm_s_type_id" + " LEFT JOIN court ON gm_court_id = court_id" + " LEFT JOIN level ON gm_level_id = level_id" + " LEFT JOIN `policy` ON gm_policy_id = policy_id" + " LEFT JOIN currencies ON currency_id=gm_currency_symbol").Scan(&game_details).Error; err != nil {
		return err
	}

	if game_details.Gm_showMem == 1 {
		game_details.ShowMem = "True"
	} else {
		game_details.ShowMem = "False"
	}
	if game_details.Gm_is_stop_recurred == "n" {
		game_details.ISRecurr = "True"
	} else {
		game_details.ISRecurr = "False"

	}
	game_details.PlyID = in.PlyID
	type Name struct {
		Ply_fname string
		Ply_lname string
	}
	var name Name
	if err = Config.DB.Table("players").Where("ply_id = ?", game_details.Gm_org_id).Select("ply_fname,ply_lname").Scan(&name).Error; err != nil {
		return err
	}
	name.Ply_fname, _ = url.PathUnescape(name.Ply_fname)
	name.Ply_lname, _ = url.PathUnescape(name.Ply_lname)
	game_details.OrgName = name.Ply_fname + " " + name.Ply_lname
	type IdDummy struct {
		Gm_ply_id int
	}
	var iddata IdDummy
	if err = Config.DB.Table("gm_players").Where("gm_ply_gm_id = ? AND gm_ply_ply_id = ? AND gm_ply_status = 'y'", in.GmID, in.PlyID).Select("gm_ply_id").Scan(&iddata).Error; err != nil {
		if string(err.Error()) == "record not found" {
			game_details.MemGm = "False"
		} else {
			return err
		}
	}
	if game_details.MemGm != "False" {
		game_details.MemGm = "True"
	}
	if game_details.Gm_org_id == in.PlyID {
		game_details.Symbol = game_details.Gm_currency_symbol
	} else if game_details.Attend_type == "zoom" {
		game_details.Symbol = game_details.Currency_name
	}

	game_details, err = CommonGameKeys(in, game_details)
	if err != nil {
		return err
	}
	return nil
}
