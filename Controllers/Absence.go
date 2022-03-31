package Controllers

import (
	"CLASSFIT_GO/Models"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetAbsences(c *gin.Context) {
	var absence []Models.Absence
	err := Models.GetAllAbsences(&absence)
	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, absence)
	}
}

func GetAbsenceByID(c *gin.Context) {
	id := c.Params.ByName("absence_id")
	fmt.Println(id)

	var absence Models.Absence
	err := Models.GetAbsenceByID(&absence, id)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, absence)
	}
}
