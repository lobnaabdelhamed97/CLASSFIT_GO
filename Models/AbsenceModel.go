package Models

type Absence struct {
	Absence_id      int    `json:"absence_id"`
	Absence_gm_id   int    `json:"absence_gm_id"`
	Absence_mem_id  int    `json:"absence_mem_id"`
	Absence_created string `json:"absence_created"`
}

func (b *Absence) TableName() string {
	return "absence"
}
