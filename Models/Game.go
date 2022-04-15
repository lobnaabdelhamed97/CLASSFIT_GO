package Models

import (
	"errors"
	_ "github.com/go-sql-driver/mysql"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Helper"
	"strconv"
	"encoding/json"
	"net/url"
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

func UpdateGame(game *Game, id string) (err error) {
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
	// if v.DevID == "" {
	// 	return errors.New("required Device ID")
	// }
	// if v.Source == "" {
	// 	return errors.New("required Source")
	// }
	// if v.Tkn == "" {
	// 	return errors.New("required token")
	// }
	 if v.ProjectKey == "" {
	 	return errors.New("required project key")
	 }
	 if v.ProjectSecret == "" {
	 	return errors.New("required project Secret")
	 }
	return nil
}
// func (v *User_infoandflags) Validate() error {
// 	if v.GmID < 0 {
// 		return errors.New("required Game ID")
// 	}
// 	if v.PlyID < 0 {
// 		return errors.New("required Player ID")
// 	}
// 	return nil
// }
func Userinfoandflags(in *ViewGame, user_infoandflags *User_infoandflags) (err error) {
 if err = Config.DB.Table("custom_notifications").Where("custom_notification_gm_id = ? AND custom_notification_ply_id = ?",in.GmID,in.PlyID).Select("custom_notification_reminder_status, custom_notification_period").Scan(&user_infoandflags).Error; err != nil {
	if string(err.Error()) == "record not found"{
		user_infoandflags.Custom_notification_reminder_status=0
		user_infoandflags.Custom_notification_period="" } else {
	return err 
}}
user_infoandflags.PlyID=in.PlyID
if err = Config.DB.Table("admin_terms").Where("admin_id = ?",in.PlyID).Select("terms as Terms").Scan(&user_infoandflags).Error; err != nil {
	if string(err.Error()) == "record not found"{
		user_infoandflags.Terms="false"
		}else {
			return err
		}	
}
if user_infoandflags.Terms != "false"{
	user_infoandflags.Terms="true"
}
type IdDummy struct {
	Gm_org_id int
	Gm_ply_id int
}
var iddata IdDummy
if err = Config.DB.Table("gm_players").Where("gm_ply_gm_id = ? AND gm_ply_ply_id = ? AND gm_ply_status = 'y'",in.GmID,in.PlyID).Select("gm_ply_id").Scan(&iddata).Error; err != nil {
if string(err.Error()) == "record not found"{
user_infoandflags.GmMem="no"
} else {
	return err}}
	if user_infoandflags.GmMem != "no"{
		user_infoandflags.GmMem="mem"
	}
	if err = Config.DB.Table("game").Where("gm_id = ?",in.GmID).Select("gm_org_id").Scan(&iddata).Error; err != nil {
				return err
			}	
	if iddata.Gm_org_id == in.PlyID {
		user_infoandflags.IsOrg="true"
	} else {
		user_infoandflags.IsOrg="false"
	}
	if err = Config.DB.Table("gm_players").Where("gm_ply_gm_id = ? AND gm_ply_ply_id = ? AND gm_ply_status = 'y' AND (gm_ply_leave IS NULL OR gm_ply_leave = '')",in.GmID,in.PlyID).Select("gm_ply_id").Scan(&iddata).Error; err != nil {
		if string(err.Error()) == "record not found"{
		user_infoandflags.IsMem="false"
		} else {
			return err}}
			if user_infoandflags.IsMem != "false"{
				user_infoandflags.IsMem="true"
			}	
			keysec:=Helper.KeySecured(in.ProjectKey,in.ProjectSecret)

values,err := json.Marshal(in)
body:=Helper.PaymentCurl(keysec,"https://v2.classfit.com/payment/offline/admin/data",values)
var payment OfflinePayment
json.Unmarshal(body, &payment)
user_infoandflags.Offline_payments_status=payment.Status
OffPayment:=payment.Admin_country_currency_data.Country_monthly_offline_payment_fees
if OffPayment < 0{
	OffPayment = 15
}
Symbol:=payment.Admin_country_currency_data.Currrency_symbol_formatted
if Symbol == "" {
	Symbol=payment.Admin_country_currency_data.Currrency_symbol
	if Symbol == "" {
		Symbol = "US$"
	}
}
	user_infoandflags.Offline_payments_currency_amount=Symbol+strconv.Itoa(OffPayment)
			return nil
}

func Organizerinfo(in *ViewGame, organizer_info *Organizer_info) (err error) {
	type IdDummy struct {
		Gm_org_id int
	}
	var iddata IdDummy
	if err = Config.DB.Table("game").Where("gm_id = ?",in.GmID).Select("gm_org_id").Scan(&iddata).Error; err != nil {
		return err 
	}
	if err = Config.DB.Table("players").Where("ply_id = ?",iddata.Gm_org_id).Select("ply_bio,ply_business").Scan(&organizer_info).Error; err != nil {
		return err 
	}
	organizer_info.Ply_bio,_=url.PathUnescape(organizer_info.Ply_bio)
	organizer_info.Ply_bio=url.PathEscape(organizer_info.Ply_bio)
	organizer_info.Ply_business,_=url.PathUnescape(organizer_info.Ply_business)
	organizer_info.Ply_business=url.PathEscape(organizer_info.Ply_business)
	type Name struct {
		Ply_fname string
		Ply_lname string
	}
	var name Name
	if err = Config.DB.Table("players").Where("ply_id = ?",iddata.Gm_org_id).Select("ply_fname,ply_lname").Scan(&name).Error; err != nil {
		return err 
	}
	name.Ply_fname,_=url.PathUnescape(name.Ply_fname)
	name.Ply_lname,_=url.PathUnescape(name.Ply_lname)
	organizer_info.OrgName=name.Ply_fname+" "+name.Ply_lname
	
	type Image struct {
		Aws_server string
		Ply_img string
		S3_profile int
	}
	var image Image
	if err = Config.DB.Table("players").Where("ply_id = ?",iddata.Gm_org_id).Select("ply_img,s3_profile").Scan(&image).Error; err != nil {
		return err 
	}	
	image.Aws_server="https://classfit-assets.s3.amazonaws.com/"
	if image.S3_profile == 1{
		organizer_info.PlyImg = image.Aws_server + image.Ply_img
	} else {
		organizer_info.PlyImg = image.Aws_server +"backup/images/upload/ply/"+ image.Ply_img

	}

return nil}

func (validate *Input) Validate() error {
    Gm_id, _:= strconv.Atoi(validate.Gm_id)
    if Gm_id  <= 0 {
		return errors.New("GmID Required")
	}

	return nil
}

func (log * Log_input) Validate() error{

//     if (log.PostData == nil){
//         return errors.New("No Data Sent")
//     }
//     Org_id, _ := strconv.Atoi(log.PostData["PlyID"])
//     if Org_id  <= 0 {
// 		return errors.New("GmID Required")
// 	}
//     if log.PostData.Type  == "" {
// 		return errors.New("Type Required")
// 	}
    return nil
}

func Member_info(validate *Input, mem_info *[]Mem_info,wait_list_info *[]Wait_list_info) (final Final,err error) {

      if err = Config.DB.Table("players").Select("distinct ply_id, ply_fname ,ply_lname ,country_name, city_name,typed_city,contact_id,gm_ply_ply_id,guest_ply_id,CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS privecy").
          Joins("LEFT JOIN country ON ply_country_id= country_id").Joins("LEFT JOIN ply_typed_city ON player_id = ply_id").Joins("LEFT JOIN city ON ply_city_id = city_id").Joins("LEFT JOIN gm_players ON gm_ply_ply_id=ply_id and gm_ply_gm_id= " + validate.Gm_id + " ").
          Joins("LEFT JOIN guests ON guest_ply_id=gm_ply_ply_id and guest_gm_id= " + validate.Gm_id + " ").Joins("LEFT JOIN contacts ON contact_ply_id = ply_id and contact_org_id IN (SELECT gm_org_id from game WHERE gm_id= " + validate.Gm_id + ") ").Where("gm_ply_gm_id= "+validate.Gm_id+" AND gm_ply_status = 'y' AND gm_ply_removed_by_admin = 0 ").
          Scan(&mem_info).Error; err != nil {
                return final,errors.New("No Available Data")
                }
                for i := 0; i < len(*mem_info) ;i++{
                  if (*mem_info)[i].Gm_ply_ply_id > 0 && (*mem_info)[i].Guest_ply_id == 0 {
                        (*mem_info)[i].PlyType = "member"
                } else if ((*mem_info)[i].Gm_ply_ply_id == 0 && (*mem_info)[i].Guest_ply_id > 0) || ((*mem_info)[i].Gm_ply_ply_id > 0 && (*mem_info)[i].Guest_ply_id > 0){
                        (*mem_info)[i].PlyType = "guest" }

                  if ((*mem_info)[i].City_name == "" && (*mem_info)[i].Ply_typed_city != "" ){
                        (*mem_info)[i].City_name = (*mem_info)[i].Ply_typed_city }
            }

 	if err = Config.DB.Table("players").Select("ply_fname,ply_lname,country_name,city_name,ply_id,typed_city,CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS privecy,ply_img").
        Joins("LEFT JOIN country ON ply_country_id= country_id").Joins("LEFT JOIN city ON ply_city_id = city_id").
        Joins("LEFT JOIN gm_waitlist ON gm_wait_list_ply_id= ply_id").Joins("LEFT JOIN ply_typed_city ON player_id = gm_wait_list_ply_id").
        Where("gm_wait_list_gm_id= "+validate.Gm_id+" AND gm_wait_list_withdrew = 0 AND gm_wait_list_removed_by_admin = 0").Scan(&wait_list_info).Error; err != nil {
        return final,errors.New("No Available Data")
        }
          for i := 0; i < len(*wait_list_info) ;i++{
               (*wait_list_info)[i].PlyType = "member"
               (*wait_list_info)[i].Ply_img = "https://classfit-assets.s3.amazonaws.com/backup" + (*wait_list_info)[i].Ply_img

               if ((*wait_list_info)[i].City_name == "" && (*wait_list_info)[i].Ply_typed_city != "" ){
                        (*wait_list_info)[i].City_name = (*wait_list_info)[i].Ply_typed_city }
               }

 	    final = Final{Member : *mem_info,Waitlist : *wait_list_info}

	return final,nil
}

