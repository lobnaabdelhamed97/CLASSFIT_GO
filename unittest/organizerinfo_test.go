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

func TestOrganizerInfo(t *testing.T) {
	var views = []Models.ViewGame{
		{
			GmID:          279731,
			PlyID:         6236,
			ProjectSecret: "1234",
			ProjectKey:    "1234",
			Tkn:           "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
			DevID:         "windows_Chrome_172.31.35.236",
			Source:        "Web",
		},
		{
			GmID:          -1,
			PlyID:         6236,
			ProjectSecret: "1234",
			ProjectKey:    "1234",
			Tkn:           "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
			DevID:         "windows_Chrome_172.31.35.236",
			Source:        "Web",
		},
		{
			GmID:          29707,
			PlyID:         6236,
			ProjectSecret: "1234",
			ProjectKey:    "1234",
			Tkn:           "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
			DevID:         "windows_Chrome_172.31.35.236",
			Source:        "Web",
		},
		{
			GmID:          29707,
			PlyID:         -1,
			ProjectSecret: "1234",
			ProjectKey:    "1234",
			Tkn:           "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
			DevID:         "windows_Chrome_172.31.35.236",
			Source:        "Web",
		},
		{
			GmID:          5486,
			PlyID:         848,
			ProjectSecret: "1234",
			ProjectKey:    "1234",
			Tkn:           "106e2ee8454a2257f1bc52c251245ba009cadb67",
			DevID:         "fcc78fd5d99ead13",
			Source:        "Web",
		},
	}
	for i := range views {
		var err error
		Config.DB, err = gorm.Open("mysql", Config.DbURL(Config.BuildDBConfig()))
		if err != nil {
			fmt.Println("Status:", err)
		}
		defer func(DB *gorm.DB) {
			err := DB.Close()
			if err != nil {

			}
		}(Config.DB)
		var buf bytes.Buffer
		err = json.NewEncoder(&buf).Encode(views[i])
		if err != nil {
			t.Fatalf("encoding problem")
		}
		// Switch to test mode, so you don't get such noisy output

		gin.SetMode(gin.TestMode)

		// Set up your router, just like you did in your main function, and
		// register your routes
		r := gin.Default()
		r.POST("/organizer-info", Controllers.Organizer_info)

		// Create the mock request you'd like to test. Make sure the second argument
		// here is the same as one of the routes you defined in the router setup
		// block!
		req, err := http.NewRequest(http.MethodPost, "/organizer-info", &buf)
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
			t.Logf("Expected to get status %d but instead got %d\n", http.StatusOK, w.Code)
		}
	}
}
