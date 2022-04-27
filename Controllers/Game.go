package Controllers

import (
	"encoding/json"
	"net/http"
	//     "github.com/lobnaabdelhamed97/CLASSFIT_GO/History_log"
	"github.com/gin-gonic/gin"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Models"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Responses"
"fmt"
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
	eror := c.BindJSON(&game)
	if eror != nil {
		return
	}
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

func User_infoandflags(c *gin.Context) {
	var viewgame Models.ViewGame
	eror := c.BindJSON(&viewgame)
	if eror != nil {
		return
	}
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

func Organizer_info(c *gin.Context) {
	var viewgame Models.ViewGame
	eror := c.BindJSON(&viewgame)
	if eror != nil {
		return
	}
	err := viewgame.Validate()
	if err != nil {
		Responses.ERROR(c, err.Error())
	} else {
		var Organizer_info Models.Organizer_info
		err := Models.Organizerinfo(&viewgame, &Organizer_info)
		if err != nil {
			Responses.ERROR(c, err.Error())
		} else {
			data, _ := json.Marshal(Organizer_info)
			Responses.SUCCESS(c, string(data))
		}
	}
}

func Game_Details(c *gin.Context) {
	var viewgame Models.ViewGame
	eror := c.BindJSON(&viewgame)
	if eror != nil {
		return
	}
	err := viewgame.Validate()
	if err != nil {
		Responses.ERROR(c, err.Error())
	} else {
		var Game_details Models.Game_details
		err := Models.GameDetails(&viewgame, &Game_details)
		if err != nil {
			Responses.ERROR(c, err.Error())
		} else {
			data, _ := json.Marshal(Game_details)
			Responses.SUCCESS(c, string(data))
		}
	}
}

func ViewGame(c *gin.Context) {
	var viewgame Models.ViewGame
	eror := c.BindJSON(&viewgame)
	if eror != nil {
		return
	}
	//create validation here
	err := viewgame.Validate()
	if err != nil {
		Responses.ERROR(c, err.Error())
	} else {
		data, _ := json.Marshal(viewgame)
		Responses.SUCCESS(c, string(data))
	}
}

func Participants(c *gin.Context) {
	var wait_list_info []Models.Wait_list_info
	var mem_info []Models.Mem_info
	var validate Models.Input
	eror := c.BindJSON(&validate)
	if eror != nil {
		return
	}
	err_validate_mem := validate.Validate()
	if err_validate_mem != nil {
		Responses.ERROR(c, err_validate_mem.Error())
	} else {
		members, err_mem := Models.Member_info(&validate, &mem_info, &wait_list_info)
		if err_mem != nil {
			Responses.ERROR(c, err_mem.Error())
		} else {
			c.JSON(http.StatusOK, members)
		}
	}
}

// func Player_data(c *gin.Context) {
// 	var validate       Models.Player_input
// 	c.BindJSON(&validate)
//         members  := Models.Get_ply_verified_methods(&validate)
//         if members != ""{
//             c.JSON(http.StatusOK, members)
//         }else {
//             Responses.ERROR(c, "No data")
//         }
//
//
// }

// func Game_data(c *gin.Context) {
//     var result         []Models.Count_game
//  	var validate       Models.PP
//  	c.BindJSON(&validate)
//          members  := Models.Get_players_count_in_game(&validate,&result)
//          c.JSON(http.StatusOK, members)
//
//  }

// func Inst_data(c *gin.Context){
//         var validate       Models.PP
//         c.BindJSON(&validate)
//         members  := Models.GetGmInstructorData(&validate)
//
//         c.JSON(http.StatusOK, members)
//
// }
