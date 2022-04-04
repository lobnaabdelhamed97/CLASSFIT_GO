package Controllers

import (
	"CLASSFIT_GO/Models"
	"fmt"
	"errors"
	"net/http"
	"github.com/gin-gonic/gin"
	"database/sql"
	"log"
)
    var db *sql.DB


func GetGames(c *gin.Context) {
	var game Models.Game
	err := Models.GetAllGames(&game)
	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, game)
	}
}

func CreateGame(c *gin.Context) {
	var game Models.Game
	c.BindJSON(&game)
	err := Models.CreateGame(&game)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, game)
	}
}

func GetGameByID(c *gin.Context) {
	id := c.Params.ByName("gm_id")
	var game Models.Game
	err := Models.GetGameByID(&game, id)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, game)
	}
}
func Mem_info(gm_id int , ply_id int) ( Models.Players,  error) {
    data := Models.Players{}
    if gm_id == 0 || ply_id ==0 {
    return data , errors.New("Invalid Data")
}
    row := db.QueryRow("SELECT distinct ply_fname AS PlyFname,ply_lname AS PlyLname FROM players where ply_id=5952;")
	if err := row.Scan(&data.Ply_fname, &data.Ply_lname); err != nil {
	log.Fatalf("could not scan row: %v", err)
}
    fmt.Println(data)
    return data,nil
}

func ViewGame(c *gin.Context) {
	var viewgame Models.ViewGame
	c.BindJSON(&viewgame)
	//create validation here
	err := viewgame.Validate()
	if err != nil {
		fmt.Println(err)
		c.AbortWithStatus(http.StatusUnprocessableEntity)

		return
	}

}