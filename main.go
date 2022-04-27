package main

import (
	"fmt"

	"github.com/jinzhu/gorm"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Config"
	"github.com/lobnaabdelhamed97/CLASSFIT_GO/Routes"
)

var err error

func main() {
	Config.DB, err = gorm.Open("mysql", Config.DbURL(Config.BuildDBConfig()))
	if err != nil {
		fmt.Println("Status:", err)
	}
	defer func(DB *gorm.DB) {
		err := DB.Close()
		if err != nil {

		}
	}(Config.DB)
	r := Routes.SetupRouter()
	//running
	err := r.Run()
	if err != nil {
		return
	}
}
