package Unittest
import (
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Controllers"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Models"
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"net/http"
	"net/http/httptest"
	"testing"
)
func Test_Mem_info(t *testing.T) {
	gin.SetMode(gin.TestMode)
	views := []Models.Mem_info{
		{
			PlyID: "5286",
			Gm_id: "279731",
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
		// Setup your router, just like you did in your main function, and
		// register your routes
		r := gin.Default()
		r.POST("/mem-info", Controllers.Mem_info)

    // Create the mock request you'd like to test. Make sure the second argument
    // here is the same as one of the routes you defined in the router setup
    // block!
    req, err := http.NewRequest(http.MethodPost, "/mem-info", &buf)
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
