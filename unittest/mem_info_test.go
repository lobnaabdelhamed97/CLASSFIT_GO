package Unittest
import (
  "testing"
  "fmt"
  "github.com/gin-gonic/gin"
  "CLASSFIT_GO/Controllers"
  "CLASSFIT_GO/Models"
  "net/http"
  "net/http/httptest"
  "bytes"
  "encoding/json"

)
func Test_Mem_info(t *testing.T) {
    views := []Models.Mem_info{
        {
            Gm_id: 279731,
        },
        {
            Gm_id: -1,
        },
    }
    for i := range views{
    var buf bytes.Buffer
    err := json.NewEncoder(&buf).Encode(views[i])
    if err != nil {
        t.Fatalf("encoding problem")
    }
        // Switch to test mode so you don't get such noisy output

    gin.SetMode(gin.TestMode)

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
        t.Fatalf("Expected to get status %d but instead got %d\n", http.StatusOK, w.Code)
    }
}
}
