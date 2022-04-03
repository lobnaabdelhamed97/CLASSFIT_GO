package Routes

import (
	"CLASSFIT_GO/Controllers"

	"github.com/gin-gonic/gin"
)

//SetupRouter ... Configure routes
func SetupRouter() *gin.Engine {
	r := gin.Default()
	grp1 := r.Group("/view-game")
	{
		grp1.POST("game", Controllers.GetGames)
		grp1.GET("game/:gm_id", Controllers.GetGameByID)

	}
	grp2 := r.Group("/view-absence")
	{
		grp2.POST("absence", Controllers.GetAbsences)
		grp2.GET("absence/:absence_id", Controllers.GetAbsenceByID)
		//grp2.POST("absence", Controllers.CreateAbsence)

	}
	return r
}
