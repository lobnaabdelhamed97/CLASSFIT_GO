package Controllers
import (
        "testing"
        "fmt"
        "CLASSFIT_GO/Controllers"

)
func Test_Mem_info(t *testing.T){
     num := Controllers.Mem_info("5")

        fmt.Println(num);


}