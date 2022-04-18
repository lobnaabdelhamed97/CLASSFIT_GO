package Helper

import (
	"github.com/stripe/stripe-go"
	"github.com/stripe/stripe-go/card"
	"github.com/stripe/stripe-go/paymentmethod"
	//"fmt"
	"strings"

)
func RetrieveData(customer_id string,card_id string)(string,string,error){
stripe.Key = "sk_test_XEz4HN5CyoeV0gVgYn9TrpRH"
if strings.Contains(card_id,"card"){

 params := &stripe.CardParams{
	Customer: stripe.String(customer_id),
  }
  c, err := card.Get(
	card_id,
	params,
  )
if err != nil{
return "nil","nil",err
}
return c.Name,c.Last4,nil
} else {
pm, err := paymentmethod.Get(
	card_id,
	nil,
  )
  if err != nil{
	return "nil","nil",err
	}
	return pm.BillingDetails.Name,pm.Card.Last4,nil
	}

}


