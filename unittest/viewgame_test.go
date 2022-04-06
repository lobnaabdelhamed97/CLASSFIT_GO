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
func TestViewGame(t *testing.T) {
    views := []Models.ViewGame{
        {
            GmID: 279731,
            PlyID: 6236,
            ProjectSecret: "1234",
            ProjectKey: "1234",
            Tkn: "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
            DevID: "windows_Chrome_172.31.35.236",
            Source: "Web",
        },
        {
            GmID: -1,
            PlyID: 6236,
            ProjectSecret: "1234",
            ProjectKey: "1234",
            Tkn: "d9a4013b9cba108f12ae950f8ae38a5c0aec3622",
            DevID: "windows_Chrome_172.31.35.236",
            Source: "Web",
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
	r.POST("/view-game", Controllers.ViewGame)

    // Create the mock request you'd like to test. Make sure the second argument
    // here is the same as one of the routes you defined in the router setup
    // block!
    req, err := http.NewRequest(http.MethodPost, "/view-game", &buf)
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
