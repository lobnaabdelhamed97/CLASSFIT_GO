package Config

import (
	"fmt"
    "log"
	"github.com/jinzhu/gorm"
	"database/sql"
	_"github.com/go-sql-driver/mysql"

)

var DB *gorm.DB

// DBConfig represents db configuration
type DBConfig struct {
	Host     string
	Port     int
	User     string
	DBName   string
	Password string
}

func BuildDBConfig2() *DBConfig {
	dbConfig := DBConfig{
		Host:     "127.0.0.1",
		Port:     3306,
		User:     "elbadawy",
		Password: "qazxcdews",
		DBName:   "users",
	}
	return &dbConfig
}
func BuildDBConfig() *DBConfig {
	dbConfig := DBConfig{
		Host:     "classfit-clone.cluster-ro-cjwhdnfvi5np.us-east-2.rds.amazonaws.com",
		Port:     3306,
		User:     "admin",
		Password: "admin3030",
		DBName:   "fastplayapp_test",
	}
	return &dbConfig
}
func DbURL(dbConfig *DBConfig) string {
	return fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		dbConfig.User,
		dbConfig.Password,
		dbConfig.Host,
		dbConfig.Port,
		dbConfig.DBName,
	)
}

func init() {
    var db *sql.DB
	var err error
	db, err = sql.Open("mysql","admin:admin3030@tcp(classfit-clone.cluster-ro-cjwhdnfvi5np.us-east-2.rds.amazonaws.com)/fastplayapp_test")
	if err != nil {
		log.Fatalf("could not connect to database: %v", err)
	}
	// To verify the connection to our database instance, we can call the `Ping`
	// method. If no error is returned, we can assume a successful connection
	if err := db.Ping(); err != nil {
		log.Fatalf("unable to reach database: %v", err)
	}
	fmt.Println("database is reachable")
}
