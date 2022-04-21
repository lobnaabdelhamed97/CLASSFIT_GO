package Responses

import (
	"encoding/json"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Respond struct {
	Result  string `json:"Result"`
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func ERROR(c *gin.Context, message string) {
	ErrorRespond := Respond{
		Result:  "error",
		Code:    http.StatusUnprocessableEntity,
		Message: message,
	}
	data, _ := json.Marshal(ErrorRespond)
	c.JSON(http.StatusUnprocessableEntity, string(data))

}

func SUCCESS(c *gin.Context, message string) {
	SuccessRespond := Respond{
		Result:  "True",
		Code:    http.StatusOK,
		Message: message,
	}
	data, _ := json.Marshal(SuccessRespond)
	c.JSON(http.StatusOK, string(data))
}
