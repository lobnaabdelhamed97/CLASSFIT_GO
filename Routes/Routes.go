package Routes

import (
	"github.com/gin-gonic/gin"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Controllers"
)

//SetupRouter ... Configure routes
func SetupRouter() *gin.Engine {
	r := gin.Default()
	grp1 := r.Group("/get-game")
	{
		grp1.POST("game", Controllers.GetGames)
		grp1.GET("game/:gm_id", Controllers.GetGameByID)

	}

	r.POST("/view-game", Controllers.ViewGame)
	r.POST("/participants", Controllers.Participants)
	r.POST("/user-info", Controllers.User_infoandflags)
	r.POST("/organizer-info", Controllers.Organizer_info)
	r.POST("/game-details", Controllers.Game_Details)
// 	r.POST("/player-data", Controllers.Player_data)
//  	r.POST("/game-data", Controllers.Game_data)




	return r
}
