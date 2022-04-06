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
//  	var result Result
// 	res :=fmt.Sprintf(`SELECT distinct ply_fname AS PlyFname,ply_lname AS PlyLname , country_name AS PlyCountry, city_name AS PlyCty , ply_id AS PlyID
//                     where ply_id= %s `,v.Gm_id)

// Select `id`, `name` automatically when querying
rows :=DB.Model(&Game{}).Find(&Mem_info{})
// 	rows := DB.Exec(res)
// 	rows.Close()
	fmt.Println(rows)
	return nil
}



