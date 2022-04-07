package Responses

import (
	//"encoding/json"
	//"fmt"
	//"net/http"
)

func JSON(statusCode int, data interface{}) {

	//err := json.NewEncoder(w).Encode(data)
	//if err != nil {
	//	fmt.Fprintf(w, "%s", err.Error())
	//}
}

func JsonContext ()

func ERROR(statusCode int, err error) {
	if err != nil {
		JSON(statusCode, struct {
			Error string `json:"error"`
		}{
			Error: err.Error(),
		})
		return
	}
}