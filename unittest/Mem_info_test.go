package Unittest
import (
        "testing"
        "fmt"
        "CLASSFIT_GO/Controllers"

)


func Test_Mem_info(t *testing.T){
     num,err := Controllers.Mem_info(5,5)
     if (err != nil) {
        fmt.Println(err);
     } else {
        fmt.Println(num);
    }

}