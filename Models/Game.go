package Models

import (
	"CLASSFIT_GO/Config"

	_ "github.com/go-sql-driver/mysql"
)

func GetAllGames(game *[]Game) (err error) {
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

func Mem_info(players *Players, id int) (err error) {
	Config.DB.Find(players)
	return nil
}



