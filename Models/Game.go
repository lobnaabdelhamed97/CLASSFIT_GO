package Models

import (
	"errors"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
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
func (b *Mem_info) Validate() error {
	// 	if (v.Gm_id < 0) {
	// 		return errors.New("Gm_id Required")
	//     }
	//     if (v.PlyID < 0) {
	// 		return errors.New("PlyID Required")
	//     }
	return nil
}

func (b *Mem_info) Member_info() (*gorm.DB , error) {
	type Result struct {
		PlyFname   string `json:"ply_fname"`
		PlyLname   string `json:"ply_lname"`
		PlyCountry string `json:"country_name"`
		PlyCty     string `json:"city_name"`
		PlyID      int    `json:"ply_id"`
		Privecy    string `json:"ply_city_sett"`
		ContactID  int    `json:"contact_id"`
		PlyImg     string `json:"ply_img"`
		Member     int    `json:"gm_ply_ply_id"`
		Guest      int    `json:"guest_ply_id"`
	}
	var DB *gorm.DB
	var result Result
	res := DB.Raw(`SELECT distinct ply_fname AS PlyFname,ply_lname AS PlyLname , country_name AS PlyCountry, city_name AS PlyCty ,ply_id AS PlyID, ply_img AS PlyImg,
                CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE 'false' END AS Privecy,gm_ply_ply_id AS member,guest_ply_id AS guest,contact_id AS ContactID
                FROM players
                LEFT JOIN gm_players ON gm_ply_ply_id=ply_id
                LEFT JOIN guests ON guest_ply_id=gm_ply_ply_id
                LEFT JOIN gm_waitlist ON gm_wait_list_ply_id= ply_id
                LEFT JOIN country ON ply_country_id= country_id
                LEFT JOIN city ON ply_city_id = city_id
                LEFT JOIN contacts ON contact_ply_id = ply_id and contact_org_id = (SELECT gm_org_id from game WHERE gm_id=?)
                where ply_id=?;`, b.Gm_id, b.PlyID).Scan(result)
    if res == nil {
        return nil,errors.New("There's no available data to this user")
    }
	return res,nil
}
