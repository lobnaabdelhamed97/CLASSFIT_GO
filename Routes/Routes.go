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
		grp1.GET("game", Controllers.GetGames)
		grp1.GET("game/:id", Controllers.GetGameByID)

	}
	grp2 := r.Group("/view-absence")
	{
		grp2.GET("absence", Controllers.GetAbsences)
		grp2.GET("absence/:id", Controllers.GetAbsenceByID)

	}
	return r
}
