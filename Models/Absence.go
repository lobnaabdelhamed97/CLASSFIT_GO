package Models

import (
	"CLASSFIT_GO/Config"

	_ "github.com/go-sql-driver/mysql"
)

func GetAllAbsences(absence *[]Absence) (err error) {
	if err = Config.DB.Find(absence).Error; err != nil {
		return err
	}
	return nil
}
func GetAbsenceByID(absence *Absence, id string) (err error) {
	if err = Config.DB.Where("absence_id = ?", id).First(absence).Error; err != nil {
		return err
	}
	return nil
}

func CreateAbsence(absence *Absence) (err error) {
	if err = Config.DB.Create(absence).Error; err != nil {
		return err
	}
	return nil
}