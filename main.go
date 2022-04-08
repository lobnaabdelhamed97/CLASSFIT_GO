package main

import (
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Routes"
	"fmt"
	"github.com/jinzhu/gorm"
)

var err error

func main() {
	Config.DB, err = gorm.Open("mysql", Config.DbURL(Config.BuildDBConfig()))
	if err != nil {
		fmt.Println("Status:", err)
	}
	defer Config.DB.Close()
	r := Routes.SetupRouter()
	//running
	r.Run()
}
