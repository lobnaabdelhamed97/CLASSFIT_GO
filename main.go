package main

import (
	"CLASSFIT_GO/Config"
	"CLASSFIT_GO/Routes"
	"fmt"
	"github.com/go-sql-driver/mysql"
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
