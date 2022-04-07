package Controllers

import (
	"CLASSFIT_GO/Models"
	"CLASSFIT_GO/Responses"
	"fmt"
	"net/http"
	"github.com/gin-gonic/gin"
	"encoding/json"
)



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

func Mem_info(c* gin.Context){
    var mem_info Models.Mem_info
	c.BindJSON(&mem_info)
	//create validation here
	err := mem_info.Validate()
	if err != nil {
		fmt.Println(err)
		c.AbortWithStatus(http.StatusUnprocessableEntity)
		return
	}
}
func ViewGame(c *gin.Context) {
	var viewgame Models.ViewGame
	c.BindJSON(&viewgame)
	//create validation here
	err := viewgame.Validate()
	if err != nil{
Responses.ERROR(c,err.Error())
	} else {
		data,_:=json.Marshal(viewgame)
		Responses.SUCCESS(c,string(data))
	}
}