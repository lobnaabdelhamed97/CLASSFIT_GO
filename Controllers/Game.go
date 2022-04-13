package Controllers

import (
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Models"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Responses"
	"net/http"
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

func Mem_info(c *gin.Context) {
	var mem_info Models.Mem_info
	//create validation here
	var in Models.Input
	c.BindJSON(&in)
	err_validate := in.Validate()
	if err_validate != nil {
		Responses.ERROR(c, err_validate.Error())
	} else {
		err := Models.Member_info(&in, &mem_info)
		if err != nil {
			Responses.ERROR(c, err.Error())
			//       c.AbortWithStatus(http.StatusNotFound)
		} else {
			c.JSON(http.StatusOK, mem_info)
		}
	}
}

func User_infoandflags(c *gin.Context) {
	var viewgame Models.ViewGame
	c.BindJSON(&viewgame)
	err := viewgame.Validate()

	if err != nil {
		Responses.ERROR(c, err.Error())
	} else {
		var User_infoandflags Models.User_infoandflags
		err := Models.Userinfoandflags(&viewgame, &User_infoandflags)
		if err != nil {
			Responses.ERROR(c, err.Error())
		} else {
			data, _ := json.Marshal(User_infoandflags)
			Responses.SUCCESS(c, string(data))
		}
	}
}

func ViewGame(c *gin.Context) {
	var viewgame Models.ViewGame
	c.BindJSON(&viewgame)
	//create validation here
	err := viewgame.Validate()
	if err != nil {
		Responses.ERROR(c, err.Error())
	} else {
		data, _ := json.Marshal(viewgame)
		Responses.SUCCESS(c, string(data))
	}
}

func Wait_list_info(c *gin.Context) {
	var wait_list_info []Models.Wait_list_info
	//create validation here
	var in Models.Wait_list_input
	c.BindJSON(&in)
	err_validate := in.Validate()
	if err_validate != nil {
		Responses.ERROR(c, err_validate.Error())
	} else {
		err := Models.Wait_list_info_func(&in, &wait_list_info)
		if err != nil {
			Responses.ERROR(c, err.Error())
		} else {
			c.JSON(http.StatusOK, wait_list_info)
		}
	}
}
