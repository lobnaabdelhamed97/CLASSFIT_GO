package Models

import (
	"errors"
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
	if b.Gm_id < 0 {
		return errors.New("Gm_id Required")
	}
	if b.PlyID < 0 {
		return errors.New("PlyID Required")
	}
	return nil
}
func Member_info(mem_info *[]Mem_info) (err error) {
	query := "SELECT ply_id,contact_id,ply_fname ,ply_lname FROM players  LEFT JOIN fastplayapp_test.contacts ON contact_ply_id = ply_id and contact_org_id = (SELECT gm_org_id from fastplayapp_test.game WHERE gm_id=283908) where ply_id=5286;"
	if err = Config.DB.Raw(query).Scan(&mem_info).Error; err != nil {
		return err
	}
	return nil
}
