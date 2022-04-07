package Models

import (
	"CLASSFIT_GO/Config"
	"github.com/jinzhu/gorm"
	"errors"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
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
		return errors.New("Required Game ID")
	}
	if v.PlyID < 0 {
		return errors.New("Required Player ID")
	}
	if v.DevID == "" {
		return errors.New("Required Device ID")
	}
	if v.Source == "" {
		return errors.New("Required Source")
	}
	if v.Tkn == "" {
		return errors.New("Required token")
	}
	if v.ProjectKey == "" {
		return errors.New("Required project key")
	}
	if v.ProjectSecret == "" {
		return errors.New("Required project Secret")
	}
	return nil
}
func (v *Mem_info) Validate() error {
	if (v.Gm_id < 0 ) {
		return errors.New("Data Required")
    }
	type Result struct {
        PlyFname    string
        PlyLname    string
        PlyCountry  string
        PlyCty      string
        PlyID       int
        Privecy     string
        contact_id  int
	}
	var DB *gorm.DB
  	var result Result
 	res := DB.Raw(`SELECT distinct ply_fname AS PlyFname,ply_lname AS PlyLname , country_name AS PlyCountry, city_name AS PlyCty ,ply_id AS PlyID, ply_img AS PlyImg,
                CASE WHEN ply_city_sett = 'y' THEN 'true' ELSE  'false' END AS Privecy, gm_ply_ply_id AS member , guest_ply_id AS guest,
                (YEAR(CURDATE()) - ply_brithdate) AS PlyAge, contact_id AS ContactID
                FROM players
                LEFT JOIN gm_players ON gm_ply_ply_id=ply_id
                LEFT JOIN guests ON guest_ply_id=gm_ply_ply_id
                LEFT JOIN gm_waitlist ON gm_wait_list_ply_id= ply_id
                LEFT JOIN country ON ply_country_id= country_id
                LEFT JOIN city ON ply_city_id = city_id
                LEFT JOIN contacts ON contact_ply_id = ply_id and contact_org_id = (SELECT gm_org_id from game WHERE gm_id=?)
                where ply_id=?;`,v.Gm_id,v.PlyID).Scan(&result)

// Select `id`, `name` automatically when querying
// rows :=DB.Model(&Game{}).Find(&Mem_info{})
// 	rows := DB.Exec(res)
// 	rows.Close()
	fmt.Println(res)
	return nil
}



