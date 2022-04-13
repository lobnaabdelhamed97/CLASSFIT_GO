package Models

import (
	"errors"
"strconv"

	_ "github.com/go-sql-driver/mysql"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
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
	// if v.ProjectKey == "" {
	// 	return errors.New("required project key")
	// }
	// if v.ProjectSecret == "" {
	// 	return errors.New("required project Secret")
	// }
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
if err = Config.DB.Table("admin_terms").Where("admin_id = ?",in.PlyID).Select("terms as IssetOrgTerms").Scan(&user_infoandflags).Error; err != nil {
	if string(err.Error()) == "record not found"{
		user_infoandflags.IssetOrgTerms="false"
		}else {
			return err
		}	
}
if user_infoandflags.IssetOrgTerms != "false"{
	user_infoandflags.IssetOrgTerms="true"
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
 return nil
}
func (in *Input) Validate() error {
    Gm_id, _:= strconv.Atoi(in.Gm_id)
    PlyID, _:= strconv.Atoi(in.PlyID)
    if Gm_id  <= 0 {
		return errors.New("Data Required")
	}
	if PlyID <= 0 {
		return errors.New("required Player ID")
	}
	return nil
}

func Member_info(in *Input, mem_info *Mem_info) (err error) {

	query := "SELECT distinct ply_id,ply_fname,ply_lname,country_name,city_name,contact_id,gm_ply_ply_id,guest_ply_id,CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS privecy,gm_ply_ply_id ,guest_ply_id  " +
		"FROM players " +
		"LEFT JOIN country ON ply_country_id= country_id " +
		"LEFT JOIN city ON ply_city_id = city_id " +
		"LEFT JOIN gm_players ON gm_ply_ply_id=ply_id and gm_ply_gm_id= " + in.Gm_id + " " +
		"LEFT JOIN guests ON guest_ply_id=gm_ply_ply_id and guest_gm_id= " + in.Gm_id + " " +
		"LEFT JOIN contacts ON contact_ply_id = ply_id and contact_org_id IN (SELECT gm_org_id from game WHERE gm_id=" + in.Gm_id + ") where ply_id=" + in.PlyID + ";"

          if err = Config.DB.Raw(query).Scan(&mem_info).Error; err != nil {
                return errors.New("No Available Data")
        }
          if mem_info.Gm_ply_ply_id > 0 && mem_info.Guest_ply_id == 0 {
                mem_info.PlyType = "member"
        } else if (mem_info.Gm_ply_ply_id == 0 && mem_info.Guest_ply_id > 0) || (mem_info.Gm_ply_ply_id > 0 && mem_info.Guest_ply_id > 0){
                mem_info.PlyType = "guest"
 	}
	return nil
}
