package Controllers

import (
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Models"
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

	var absence Models.Absence
	err := Models.GetAbsenceByID(&absence, id)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, absence)
	}
}

func CreateAbsence(c *gin.Context) {
	var absence Models.Absence
	c.BindJSON(&absence)
	err := Models.CreateAbsence(&absence)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, absence)
	}
}

