package Unittest

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Controllers"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Models"
)

func Test_Player_data(t *testing.T) {
	gin.SetMode(gin.TestMode)
	views := []Models.PP{
		{
			Gm_id: 252470,
		},
		{
			Gm_id: 5286,
		},
		{
			Gm_id: 279731,
		},
		{
			Gm_id: 0,
		},
	}

	for i := range views {
		var err error
		Config.DB, err = gorm.Open("mysql", Config.DbURL(Config.BuildDBConfig()))
		if err != nil {
			fmt.Println("Status:", err)
		}
		defer Config.DB.Close()
		var buf bytes.Buffer
		err = json.NewEncoder(&buf).Encode(views[i])
		if err != nil {
			t.Fatalf("encoding problem")

		}
		// Set up your router, just like you did in your main function, and register your
		// routes
		r := gin.Default()
		r.POST("/game-data", Controllers.Game_data)

		// Create the mock request you'd like to test. Make sure the second argument
		// here is the same as one of the routes you defined in the router setup
		// block!
		req, err := http.NewRequest(http.MethodPost, "/game-data", &buf)
		if err != nil {
			t.Fatalf("Couldn't create request: %v\n", err)
		}

		// Create a response recorder so you can inspect the response
		w := httptest.NewRecorder()

		// Perform the request
		r.ServeHTTP(w, req)
		fmt.Println(w.Body)

		// Check to see if the response was what you expected
		if w.Code == http.StatusOK {
			t.Logf("Expected to get status %d is same as %d\n", http.StatusOK, w.Code)
		} else {
			t.Fatalf("Expected to get status %d but instead got %d\n", http.StatusOK, w.Code)
		}
	}
}
