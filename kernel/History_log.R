suppressPackageStartupMessages(library(reticulate))
reticulate::source_python("utils/common_utils.py")
reticulate::source_python("database/config.py")
reticulate::source_python("database/execution.py")
reticulate::source_python("database/response.py")
Sys.setenv(TZ = "UTC")
library(stringi)
library(stringr)
suppressPackageStartupMessages(library(foreach))
suppressPackageStartupMessages(library(Dict))
suppressPackageStartupMessages(library(purrr))
suppressPackageStartupMessages(library(jsonlite))
suppressPackageStartupMessages(library(urltools))

getActionLog <- function(data) {
  tryCatch({
    if (purrr::is_empty(data['org_id']) == FALSE  & purrr::is_empty(data['type']) == FALSE) {
      if(purrr::is_empty(data['searchArr']) == FALSE){
      searchTxt <- if(data[['searchArr']]$searchTxt != '') {data[['searchArr']]$searchTxt} else {''}
      searchArr <- c("actionFrom" = data[["searchArr"]]$actionFrom,"limit"=data[["searchArr"]]$limit,"searchTxt"=searchTxt)}
      date_data<- NULL
      data <- unlist(data)
      org_id <- data["org_id"]
      type <- data["type"]
      orgData <- paste0("SELECT ply_id AS orgID ,CONCAT(ply_fname,' ',ply_lname) AS adminName,ply_email As adminEmail ,ply_business As adminStudio,DATE(ply_created) AS accCreatedAt,TIME(ply_created) AS actionTime  ,timezone FROM players FULL JOIN ply_timezone ON ply_id=player_id WHERE ply_id=(", org_id, ");")
      orgData <- py$execute(orgData)
      if (length(orgData) == 0) {
        warning("Error in getting Org data")
      }
      if (purrr::is_empty(searchArr[["limit"]]) == FALSE) {
        suppressWarnings(Limit_Start <- (as.numeric(searchArr[["limit"]]) - 1) * 100 )
      }
      if (purrr::is_empty(orgData[[1]]$timezone) == TRUE) {
        orgData[[1]]$timezone <- append(timezone, 'UTC')
      }
      else {
        orgData[[1]]$timezone <- URLdecode(orgData[[1]]$timezone)
      }
      if (type == 'dash') {
        searchArr[["limit"]] <- 1
        sqlLimit <- "LIMIT 0 , 4"
        searchArr[["actionFrom"]]<- 1
      }
      else {
        sqlLimit <- paste0("LIMIT ", Limit_Start, " , 100")
      }
       sqlWhere <- ""
      if (is.null(searchTxt) == FALSE && searchTxt != '') {
        searchtext <- URLdecode(searchTxt)
        sqlWhere <- paste0("AND (players.ply_fname LIKE ('",searchtext,"') OR players.ply_lname LIKE ('",searchtext,"')
                           OR game.gm_title LIKE ('",searchtext,"') OR admin_subscriptions.name LIKE ('",searchtext,"')
                           OR Concat(players.ply_fname , '%20' ,players.ply_lname) LIKE ('",searchtext,"') )")
      }
      if (purrr::is_empty(searchArr[["actionFrom"]]) == FALSE && searchArr[["actionFrom"]] != 'NA') {
        if (searchArr[["actionFrom"]] == 1) {
          sqlWhere <- paste0(" ",sqlWhere," ")
        }
        else if (searchArr[["actionFrom"]] == 2) {
          sqlWhere <- paste0(" ",sqlWhere," AND (actions_log_user_id= (",org_id,") OR actions_log_action_type_id IN (6,7,19,20,23,24,30))")
        }
        else if (searchArr[["actionFrom"]] == 3) {
          sqlWhere <- paste0(" ",sqlWhere," AND actions_log_user_id!=(",org_id,") AND actions_log_action_type_id NOT IN(6,7,23,24,30,34)")
        }
      }
      BundlesDeployDate <- as.Date('2021-12-20 08:50:00')
      sql <- paste0("SELECT actions_log_user_id AS usrID ,CONCAT( players.ply_fname , ' ', players.ply_lname ) AS usrName ,players.ply_country_id AS country_id , actions_log_class_id AS classID , game.gm_id,
                        game.gm_title AS classTitle ,game.gm_fees, game.gm_payment_type AS classPayType , game.gm_is_free AS classIsFree, attend_type AS classAttendType,
                        actions_log_subscription_id AS subsID , admin_subscriptions.name AS subsTitle , admin_subscriptions.type AS subsType ,
                        gm_policy_id AS gmRefundPlicyID , admin_subscriptions.expire AS subsClsexpire , actions_log_payment_type AS payType , actions_log_cost AS cost ,
                        CASE
                            WHEN actions_log_subscription_id > 0 THEN admin_subscriptions.currency
                            WHEN actions_log_class_id > 0 THEN game.gm_currency_symbol
                        END AS currID,
                        currencies.currency_name AS currName,
                        currencies.currency_symbol AS currSymbol,
                        actions_log_coupon_code AS coupon , actions_log_note AS notes , actions_log_action_type_id  AS actionTypeID ,
                        action_type_name , DATE(CONVERT_TZ(actions_log_datetime, 'UTC', '", orgData[[1]]$timezone,"')) AS dateCreated , TIME(CONVERT_TZ(actions_log_datetime, 'UTC','", orgData[[1]]$timezone,"')) AS actionTime ,
                        actions_log_org_id AS OrgID  , instructors.name AS instructorName , actions_log_policy_id AS chkInPolicyID , chkIn_policy_name ,
                        actions_log_is_medical AS IsMedical , actions_log_contact_id AS ContactID , actions_log_currency_symbol AS currency_symbol,
                        DATE(actions_log_datetime) AS actionCreateDate
                FROM actions_log
                LEFT JOIN players ON players.ply_id = actions_log.actions_log_user_id
                LEFT JOIN actions_type ON actions_type.action_type_id = actions_log.actions_log_action_type_id
                LEFT JOIN game ON game.gm_id = actions_log.actions_log_class_id
                LEFT JOIN admin_subscriptions ON admin_subscriptions.id = actions_log.actions_log_subscription_id
                LEFT JOIN instructors ON instructors.id = actions_log.actions_log_user_id
                                      AND (actions_log_action_type_id = 23 OR actions_log_action_type_id=24 OR actions_log_action_type_id = 25)
                LEFT JOIN currencies ON currencies.currency_id =(CASE
                                                                    WHEN actions_log_subscription_id > 0 THEN admin_subscriptions.currency
                                                                    WHEN actions_log_class_id > 0 THEN game.gm_currency_symbol
                                                                END)
                LEFT JOIN admin_checkin_policy ON admin_policy_id = actions_log_policy_id
                LEFT JOIN checkin_policy ON checkin_policy.chkIn_policy_id = admin_checkin_policy.admin_checkin_policy_id
                WHERE actions_log_org_id= ",org_id,"
                AND actions_log_action_type_id NOT IN (0,32,33,39,41) ",sqlWhere,"
                ORDER BY actions_log_datetime DESC ",sqlLimit," ;")
      data <- py$execute(sql)
      if (length(data) != 0) {
      for (i in data) {
        var <- i[["actionTypeID"]]
        if (var == 24 || var == 25) {
          var <- 23
        }
        else if (var == 27 || var == 28) {
          var <- 26
        }
        else if(var==31){
          var <- 30
        }
        i[['appendDetail']] <- "true"
        i[['showNoteOnly']] <- "true"
        switch(paste(var),
               "1" =
               {
                 payment_data <- payment(i[["usrID"]], i[["gm_id"]], i[["actionCreateDate"]])
                 if (length(payment_data) != 0) {
                 if (stringr::str_detect(i[["classPayType"]], 'stripe') == TRUE && i[["cost"]] > 0) {
                   i[["payType"]] <- if (is.null(payment_data[[1]]$payment_id == FALSE)) { paste("Stripe ID ", payment_data[[1]]$payment_id, " ") } else { ' ' }
                 } }
                 else if (grepl("Bundle", i[["payType"]], fixed = TRUE) && i[["subsID"]] > 0) {
                   i[["remainingCredit"]] <- substr(i[["payType"]], stringr::str_locate(i[["payType"]], "-"), 1)
                   #actionCreateDate <- as.Date(as.character(i[["actionCreateDate"]]),format="%B %d %Y")

                   if (as.character(i[["actionCreateDate"]]) < BundlesDeployDate) {
                     bundle_data <- paste0("SELECT id,name FROM bundles WHERE old_bundle_id =",i[["subsID"]], " ")
                     bundle_data <- py$execute(bundle_data, db_name = py$mysql_bundle_db_name)

                     if (length(bundle_data) != 0) {
                       if (bundle_data[[1]]$id > 0) {
                         i[["subsID"]] <- bundle_data[[1]]$id
                       } } }
                   else {
                     bundleSql <- paste0("SELECT name FROM bundles WHERE id  = ",i[["subsID"]], ";")
                     bundle_data <- py$execute(bundleSql, db_name = py$mysql_bundle_db_name) }
                     if (length(bundle_data) != 0 && !is.null(i[["subsType"]])) {
                   if (stringr::str_detect(i[["subsType"]], 'pass') == TRUE) {
                     i[["payType"]] <- paste0("Class pack - ", stringr::str_trim(bundle_data[[1]]$name, side = "right"), " ")
                   }
                   else if (stringr::str_detect(i[["subsType"]], 'membership') == TRUE) {
                     i[["payType"]] <- paste0("Recurring membership - ", bundle_data[[1]]$name, " ")
                   }
                 }
                   }
                 if (i[["IsMedical"]] == 0) {
                   if (stringr::str_detect(i[["notes"]], 'Payment for single class') == TRUE && i[["coupon"]] != 'NA') {
                     i[["feesBeforeDiscount"]] <- i[["gm_fees"]]
                     i[["feesBeforeDiscount"]] <- format(round(strtoi(i[["feesBeforeDiscount"]]), 2), nsmall = 2)
                     i[["notes"]] <- paste0(" ",i[["notes"]]," using discount code ",i[["coupon"]], " ")
                   }
                 }
                 if (i[["subsID"]] > 0 && stringr::str_detect(i[["notes"]], 'Using bundle')) {
                   i[["showNoteOnly"]] <- 'true'
                 }
                 if (i[["notes"]] == 'discount') {
                   i[["notes"]] <- sprintf("Using bundle %s", URLdecode(i[["subsTitle"]]))
                 }
                 if (i[["payType"]] == 'Onsite') {
                   i[["payType"]] <- "in person payment"
                 }
                 if(i[['classIsFree']] =='y'){
                   i[['appendDetail']] <- 'false'
                 }
               },
               "2" =
               {
                 if (i[["IsMedical"]] == 1) {
                   if (!is.null(i[["notes"]])) {
                     i[["notes"]] <- URLdecode(i[["notes"]])
                   }
                 }
               },
               "4" = {
                 payment_data <- payment(i[["usrID"]],i[["gm_id"]],i[["actionCreateDate"]])
                 if (length(payment_data) != 0) {
                 RefundStatus <- paste0("SELECT gm_ply_refunded FROM gm_players WHERE gm_ply_ply_id  = ",i[["usrID"]], " AND gm_ply_gm_id = ",i[["gm_id"]], " AND DATE(gm_ply_leave)= '",i[["actionCreateDate"]],"';")
                 RefundStatus <- py$execute(RefundStatus)
                 addedAsClient <- FALSE
                 if (!is.null(i[["payType"]]) && (stringr::str_detect(i[["payType"]], "stripe") == TRUE || stringr::str_detect(i[["payType"]], "Stripe") == TRUE) &&
                   i[["subsID"]] <= 0 && i[["cost"]] > 0 && i[["gmRefundPlicyID"]] != 2) {
                   i[["notes"]] <- "User has been refunded via stripe as per refund policy"
                   i[["notes"]]<- if (length(RefundStatus) != 0 && !purrr::is_empty(RefundStatus[[1]]$refund_id)) { paste0(" ",i[["notes"]], " ,Refund type: Stripe refund ID ", payment_data[[1]]$refund_id, " ") } else { '' }
                   suppressWarnings(i[["notes"]] <- paste0(" ",i[["notes"]], " ,Refund amount: ",i[["currSymbol"]], " ", format(as.numeric(i[["cost"]]), big.mark = ","), " ") )
                   i[["payType"]] <- ""
                 } }
                 if (i[["subsID"]] > 0 && length(RefundStatus) != 0 && RefundStatus[[1]]$gm_ply_refunded == 1 && length(payment_data) != 0 &&
                   i[["gmRefundPlicyID"]] != 2) {
                    i[["payType"]] <- ''
                   if (!is.null(payment_data[[1]]$refund_id)) {
                     i[["notes"]] <- "User has been refunded via stripe as per refund policy"
                     i[["notes"]] <- paste0(" ",i[["notes"]]," Refund type: Stripe refund ID ", payment_data[[1]]$refund_id, " ")
                     suppressWarnings(i[["notes"]] <- paste0(" ",i[["notes"]]," ,Refund amount: ",i[["currSymbol"]], " ", format(as.numeric(i[["cost"]]), big.mark = ","), " ") )
                   }
                   else {
                     i[["notes"]] <- "User has been refunded via credit as per refund policy"
                     i[["notes"]] <- if (!purrr::is_empty(i[["subsTitle"]])) { paste0(" ",i[["notes"]]," ,Refund type: Credit from ",i[["subsTitle"]], " ") } else { '' }
                   } }
                 if (i[["subsID"]] <= 0) { i[["payType"]] <- " " }
                 if (length(RefundStatus) != 0 &&
                   RefundStatus[[1]]$gm_ply_refunded == 0 && i[["gmRefundPlicyID"]] != 2) {
                   i[["payType"]] <- " "
                   i[["notes"]] <- "User has not been refunded as per refund policy."
                 }
                 if (stringr::str_detect(i[["notes"]], "addedAsclient") == TRUE && i[["subsID"]] <= 0) {
                   addedAsClient <- TRUE
                   admin_name <- if (!purrr::is_empty(orgData[[1]]$adminStudio)) { orgData[[1]]$adminStudio } else { orgData[[1]]$adminName }
                    i[["notes"]] <- paste0("No refund is due as no payment was made for this class. ",i[["usrName"]], " was added to this class by ", admin_name, " with no payment made by Stripe or credit.")
                 }
                 if (!purrr::is_empty(i[["coupon"]]) && i[["cost"]] == 0)  {
                   i[["payType"]] <- ""
                    i[["notes"]] <- paste0("No refund is due as no payment was made for this class. ",i[["usrName"]], " joined this class with a 100% discount code.")
                 }
                 if (i[["subsID"]] > 0 && i[["gmRefundPlicyID"]] == 2) {
                   i[["payType"]] <- ""
                   i[["notes"]] <- "User has not been refunded as per refund policy."
                 }
                 if (stringr::str_detect(i[["classIsFree"]], "y") == TRUE &&
                   addedAsClient == FALSE &&
                   i[["notes"]] != "No refund is due as class is expired.") {
                   i[["payType"]] <- ""
                   i[["notes"]] <- "No refund is due as no payment was made for this class."
                 }
                 if (stringr::str_detect(i[["classIsFree"]], "y") == TRUE || stringr::str_detect(i[["classPayType"]], "onsite") == TRUE) {
                   i[["appendDetail"]] <- 'false'
                 }
               },
               "6" = {
                 if (!is.null(i[["subsType"]])) {
                   text <- ''
                   if (stringr::str_detect(i[["subsType"]], 'membership') == TRUE) {
                     if (i[["subsClsexpire"]] == 7) {
                       text <- 'weekly membership'
                       i[["cost"]] <- sprintf("%s per week", i[["cost"]])
                     }
                     else if (i[["subsClsexpire"]] == 30) {
                       text <- 'monthly membership'
                       i[["cost"]] <- sprintf("%s per month", i[["cost"]])
                     } }
                   if (i[["ContactID"]] > 0) {
                     user_data <- paste0("SELECT contact_ply_id , contact_email , contact_f_name ,contact_l_name from contacts
                                WHERE contact_org_id= ", org_id, " AND contact_id= ",i[["ContactID"]], ";")
                     user_data <- py$execute(user_data)
                     i[["user_name"]] <- if (purrr::is_empty(user_data) == FALSE) { paste0(" ", URLdecode(user_data[[1]]$contact_f_name), " ", URLdecode(user_data[[1]]$contact_l_name), "") } else { '' }
                   }
                   i[["action_type_name"]] <- sprintf("added a %s ", text)
                 } },
               "12" = {
                 payment_data <- payment(i[["usrID"]],i[["gm_id"]],i[["actionCreateDate"]])
                 if (stringr::str_detect(i[["payType"]], "stripe") == TRUE && i[["subsID"]] <= 0 && i[["cost"]] > 0) {
                   i[["notes"]] <- 'User has been refunded via stripe as per refund policy'
                   if (!purrr::is_empty(payment_data)) { i[["notes"]] <- paste0(" ",i[["notes"]]," ,Refund type: Stripe refund ID ",payment_data[[1]]$refund_id," ")  }
                 }
                 if (i[["subsID"]] > 0) {
                   if (length(payment_data)!=0 && !is.null(i[["subsTitle"]]) ) {
                     i[["notes"]] <- "User has been refunded via stripe as per refund policy"
                     i[["notes"]] <- paste0(" ",i[["notes"]]," ,Refund type: Stripe refund ID ",payment_data[[1]]$refund_id," ") }
                   else {
                     i[["notes"]] <- "User has been refunded via credit as per refund policy"
                     if (!is.null(i[["subsTitle"]]) ) { i[["notes"]] <- paste0(" ",i[["notes"]]," ,Refund type: Credit from ",i[["subsTitle"]]," ") }
                   }
                 }
                 if (i[["cost"]] > 0) {
                   suppressWarnings(i[["notes"]] <- paste0(" ",i[["notes"]]," ,Refund amount ",i[["currSymbol"]]," ",format(as.numeric(i[["cost"]]), big.mark = ",")) )
                 }
                 if (!is.null(i[["coupon"]]) & i[["cost"]] == 0) {
                    i[["notes"]] <- paste0("No refund is due as no payment was made for this class. ",i[["usrName"]]," joined this class with a ","%100"," discount code. ")
                 }
                 if (stringr::str_detect(i[["notes"]], "addedAsClient") == TRUE & i[["subsID"]] <= 0) {
                   if (orgData[[1]]$adminStudio != "") { i[["adminName"]] <- orgData[[1]]$adminStudio }
                   else {i[["adminName"]] <- orgData[[1]]$adminName }
                    i[["notes"]] <- paste0("No refund is due as no payment was made for this class. ",i[["usrName"]]," was added to this class by ",adminName," with no payment made by Stripe or credit.")
                 }
                 if (is.null(i[["coupon"]]) & i[["cost"]] == 0 & i[["subsID"]] <= 0 & stringr::str_detect(i[["notes"]], "No refund is due as class is expired.") == FALSE) {
                   i[["notes"]] <- "No refund is due as no payment was made for this class."
                 }
                 if (stringr::str_detect(i[["classIsFree"]], "y") == TRUE || stringr::str_detect(i[["classPayType"]], "onsite") == TRUE) {
                   i[["appendDetail"]] <- 'false'
                 }
               },
               "15" =
               {
                 cancel_players <- paste0("SELECT distinct gm_plys_log_ply_id , late_refund_ply_id , CONCAT( players.ply_fname , ' ', players.ply_lname ) AS cancelUsrName
                                     FROM cancel_gm_plys_log
                                     LEFT JOIN late_refund ON gm_plys_log_ply_id = late_refund_ply_id
                                     LEFT JOIN players ON players.ply_id = gm_plys_log_ply_id
                                     WHERE gm_plys_log_gm_id= ",i[["gm_id"]], " ;")

                 cancel_players <- py$execute(cancel_players)
                 if (length(cancel_players) != 0) {i[["canceledPlys"]] <- cancel_players}
                 else { i[["canceledPlys"]] <- 0 }
               },
               "18"={
                 #i[["canceledPlys"]] <- list()
                 i[["canceledPlys"]] <- recurr_classes_notes(i[["classID"]],i[["classIsFree"]],i[["currSymbol"]],i[["actionCreateDate"]])
               },
               "20" = {
                 subscriptionPlys <- list()
                 if (!purrr::is_empty(i[["notes"]])) {
                   if (grepl("@",i[["notes"]], fixed = TRUE)) {
                     array <- stringr::str_split(i[["notes"]], "@")
                     array <- unlist(array)
                     players_id <- if (nchar(array[2]) > 1) { array[2] } else { '' }
                     i[["notes"]] <- if (nchar(array[1]) != 0) { array[1] } else { '' }
                     players_id <- stringr::str_split(players_id, ",")
                     players_id <- unlist(players_id)
                     if (exists("players_id") == TRUE && length(players_id) > 0) {
                       i[["usrName"]] <- if (!purrr::is_empty(orgData[[1]]$adminName)) { orgData[[1]]$adminName } else { '' }
                       ids <- list()
                       emails <- list()
                       for (k in players_id) {
                         if((as.numeric(k) %% 1 == 0) && (as.numeric(k) > 0 ) && k != '') {
                           ids <- append(ids,as.numeric(k))
                         }
                         else if ((as.numeric(k) %% 1 != 0) && (as.numeric(k) > 0 && k != '')){
                           emails <- append(emails,k)}
                       }
                           where <- ''
                           if(length(emails) > 0){where <- paste0(' or (ply_email IN (",toString(emails),")  ') }
                           check_user_status <- paste0("SELECT status FROM bundles_subscriptions WHERE bundle_id= ",i[["subsID"]], " AND  ( ply_id IN (",toString(ids),") ",where," );")
                           check_user_status <- py$execute(check_user_status, db_name = py$mysql_bundle_db_name)
                           if (length(check_user_status) > 0 && check_user_status[[1]]$status != 2) {
                             if(length(ids) >=1 ){
                             subscription_member_names <- paste0("SELECT ply_id ,CONCAT(ply_fname , ' ', ply_lname ) AS subscMemName
                                                FROM players where players.ply_id IN (",toString(ids),") ")
                             subscription_member_names <- py$execute(subscription_member_names)
                             if(length(subscription_member_names) > 0){
                               for(j in subscription_member_names){
                               ply_data <- list(ply_id=j[['ply_id']],subscMemName=j[['subscMemName']])
                               ply_data <- py_dict(names(ply_data),ply_data)
                               subscriptionPlys <- append(subscriptionPlys,ply_data)
                             }
                             }
                             }
                            else {
                             subscription_member_names <- paste0("SELECT contact_id , CONCAT(contact_f_name,' ',contact_l_name) AS subscMemName
                                                  FROM contacts WHERE contact_org_id = ",org_id, " AND contact_email IN (",toString(emails),") ;")
                             subscription_member_names <- py$execute(subscription_member_names)
                             if (length(subscription_member_names) > 0) {
                               for(j in subscription_member_names){
                               ply_data <- list(ply_id=j[['contact_id']],subscMemName=j[['subscMemName']])
                               ply_data <- py_dict(names(ply_data),ply_data)
                               subscriptionPlys <- append(subscriptionPlys,ply_data)
                             } }
                       }
                 }
                 }
               }}
                 i[['subscriptionPlys']] <- subscriptionPlys
               },
               "21" =
               {
                 i[["action_type_name"]] <- "deleted a package"
               },
               "19" =
               {
                 i[["action_type_name"]] <- 'created package'
                 suppressWarnings(i[["notes"]] <- paste0("Cost: ",i[["currSymbol"]],"  ", format(as.numeric(i[["cost"]]), big.mark = ",")) )
               },
               "26" = {
                 where <- if (i[["actionTypeID"]] == 26 & !is.null(i[["dateCreated"]])) { paste0("AND DATE(coupons_log.created_at) LIKE ' ",i[["dateCreated"]], " ' ") } else { '' }
                 coupon_data <- paste0("SELECT coupon_id AS couponID,
                                          coupons_log.name,coupons_log.code AS couponCode,coupons_log.discount AS disVal,
                                          coupons_log.start_date,coupons_log.end_date,coupons_log.type,
                                          coupons_log.uses_per_coupon,coupons_log.uses_per_ply,coupons_log.status
                                          FROM coupons_log WHERE code = '",i[["coupon"]],"' AND admin_id = ", org_id," ", where, " ;")
                 coupon_data <- py$execute(coupon_data)
                 if (length(coupon_data) == 0) {
                   coupon_data <- paste0("SELECT id AS couponID ,name,code AS couponCode , discount AS disVal , start_date , end_date, type , uses_per_coupon , uses_per_ply , status
                                          FROM coupons WHERE code = '",i[["coupon"]], " ' AND admin_id = ", org_id, " ")
                   coupon_data <- py$execute(coupon_data)
                 }
                 if (length(coupon_data) != 0) {
                   couponName <- if (exists(coupon_data[[1]]$name) == TRUE) { URLdecode(coupon_data[[1]]$name) } else { i[["coupon"]] }
                   disType <- if (coupon_data[[1]]$type == 'p') { 'percentage' } else { 'Fixed amount' }
                   status <- if (coupon_data[[1]]$status == 1) { 'Enabled' } else { 'Disabled' }

                 i[["couponName"]] <- couponName
                 i[["disType"]] <- disType
                 i[["discountVal"]] <- paste0(coupon_data[[1]]$disVal, disType)
                 i[["uses_per_coupon"]] <- coupon_data[[1]]$uses_per_coupon
                 i[["couponCode"]] <- coupon_data[[1]]$couponCode
                 i[["uses_per_ply"]] <- coupon_data[[1]]$uses_per_ply
                 i[["status"]] <- status
                 i[["startDate"]] <- coupon_data[[1]]$start_date
                 i[["endDate"]] <- coupon_data[[1]]$end_date
               }
               },
               "40" = {
                 i[["appendDetail"]] <- 'false'
               },
               "42" =
               {
                 dataNote <- as.Date(i[["notes"]])
                 i[["notes"]] <- sprintf("Next billing date on %s", format(dataNote, format = ("%d %B %Y")))
                 if (format(round(i[["cost"]], 2), nsmall = 2) < 0.5) {
                   i[["cost"]] <- 0
                 }
               }
          ,
               "43" =
               {
                 dataNote <- as.Date(i[["notes"]])
                 i[["notes"]]<- sprintf("Next billing date on %s", format(dataNote, format = "%d %B %Y"))
               },
               "44" =
               {
                 i[["appendDetail"]] <- 'false'
               },
               "45" =
               {
                 dataNote <- as.Date(i[["notes"]])
                 i[["notes"]] <- sprintf("Next billing date on %s", format(dataNote, format = "%d %B %Y"))
                 if (format(round(i[["cost"]], 2), nsmall = 2) < 0.5) {
                   i[["cost"]] <- 0
                 }
               },
               "48" ={
                 #i[["pausedRecurrGames"]] <- list()
                 i[["pausedRecurrGames"]]  <-  recurr_classes_notes(i[["classID"]],i[["classIsFree"]],i[["currSymbol"]],i[["actionCreateDate"]])
               },
               "22" =
               {
                 data[["action_type_name"]] <- paste0("", data[["action_type_name"]], " ",i[["chkIn_policy_name"]], " ")
               },
               "23" = {
                 instructor_data <- paste0("SELECT name FROM instructors_log LEFT JOIN actions_log ON instructors_log.instructor_id = actions_log.actions_log_user_id WHERE instructor_id =",i[["usrID"]], " order by id DESC ")
                 instructor_data <- py$execute(instructor_data)
                 if (length(instructor_data) != 0) {
                   i[["instructorName"]] <- instructor_data[[1]]$name
                 } },
               "30" ={
                 where <- ""
                 if(i[["ContactID"]] > 0){
                   guest_data <- paste0("SELECT contact_email ,contact_f_name ,contact_l_name ,contact_ply_id from contacts
                                    WHERE contact_org_id=",org_id," AND contact_id=",i[["ContactID"]]," ;")
                   guest_data <- py$execute(guest_data)
                   guest_name <- if(length(guest_data)!=0 && guest_data[[1]]$contact_f_name != 'NA'){
                     where <- paste0("And bundles_subscriptions.ply_email= ",guest_data[[1]]$contact_email," ")
                     URLdecode(guest_data[[1]]$contact_f_name)} else {''}
                   i[["action_type_name"]] <- paste0(" added ",guest_name," as client in")
                   i[["usrName"]] <- guest_name
                   i[["guestPlyID"]] <- if(length(guest_data)!=0 && guest_data[[1]]$contact_ply_id > 0){guest_data[[1]]$contact_ply_id} else{0}
                 }
                 if(i[["subsID"]] > 0){
                   if(i[["usrID"]] > 0){where <- paste0("AND bundles_subscriptions.ply_id= ",i[["usrID"]]," ") }
                    sql <- paste0("SELECT available_credit , name , bundle_id
                                  FROM bundles
                                  LEFT JOIN bundles_subscriptions ON bundles_subscriptions.bundle_id = bundles.id
                                  WHERE bundles_subscriptions.is_removed = 0
                                  AND bundles.id = ",i[["subsID"]],"
                                  ",where,"
                                  ORDER BY bundles_subscriptions.created_at DESC LIMIT 1")
                   bundle_details <- py$execute(sql,db_name=py$mysql_bundle_db_name)
                   if(length(bundle_details) !=0){
                   i[["bundle_name"]] <- if(!purrr::is_empty(bundle_details[[1]]$name)){bundle_details[[1]]$name} else{''}
                   i[["bundle_id"]] <- if(!purrr::is_empty(bundle_details[[1]]$bundle_id)){bundle_details[[1]]$bundle_id} else{''}
                   if(!purrr::is_empty(bundle_details[[1]]$available_credit) && bundle_details[[1]]$available_credit < 100){
                     i[["bundle_available_credit"]] <- bundle_details[[1]]$available_credit}
                   else if(!purrr::is_empty(bundle_details[[1]]$available_credit) && bundle_details[[1]]$available_credit > 100 ){
                     i[["bundle_available_credit"]] <- "Unlimited"
                   }
                   else{
                     i[["bundle_available_credit"]] <- 0
                   }
                 }
                 }
                 i[["appendDetail"]] <- 'false'
               }
               ,
               "38" =
               {
                 notee <- strsplit(i[["notes"]], ':')
                 notee <- unlist(notee)
                 if (is.null(notee[1]) == FALSE & is.null(notee[2]) == FALSE) {
                   i[["notes"]] <- paste0("", notee[1], " ", notee[2], " ")
                   i[["action_type_name"]] <- ' cancelled their membership renewal - '
                 }
               },
               "5" =
               {
                 if (is.null(i[["usrID"]]) == FALSE && is.null(i[["subsID"]]) == FALSE && is.null(i[["actionCreateDate"]]) == FALSE) {
                   payment <- payment(i[["usrID"]],i[["classID"]],i[["actionCreateDate"]],i[["subsID"]])
                 }
                 if (length(payment) !=0 ) {
                   i[["payType"]] <- paste0("Stripe ID ", payment[[1]]$payment_id, " ")
                 }
                 if (is.null(i[["coupon"]]) == TRUE && i[["cost"]] <= 0) {
                    i[["notes"]] <- "N/A"
                 }
                 if(!is.null(i[["subsType"]])){
                 if (i[["subsType"]] == 'membership' || i[["subsType"]] == 'pass') {
                   i[["action_type_name"]] <- 'purchased a package'
                 }
                 if ( i[["notes"]] == "Client purchased this package from iframe price"  && i[["subsID"]] > 0 && i[["cost"]] > 0) {
                    i[["notes"]] <- ''
                 }
                 }
               },
               "77" =
               {
                 if (i[["ContactID"]] > 0) {
                   user_data <- paste0("SELECT contact_ply_id , contact_email , contact_f_name ,contact_l_name from contacts
                                WHERE contact_org_id= ", org_id, " AND contact_id= ",i[["ContactID"]], ";")
                   user_data <- py$execute(user_data)
                   if (length(user_data) != 0) {
                     if (is.null(user_data[[1]]$contact_f_name) == FALSE) {
                       i[["user_name"]] <- paste0(" ", URLdecode(user_data[[1]]$contact_f_name), " ", URLdecode(user_data[[1]]$contact_l_name), "")
                     }
                     if (is.null(user_data[[1]]$contact_ply_id) == FALSE & user_data[[1]]$contact_ply_id > 0) {
                       i[["user_id"]] <- user_data[[1]]$contact_ply_id
                       i[["ContactID"]] <- 0
                     }
                   }
                   else {
                     warning("Error in getting contact data")
                   }
                   i[["showNoteOnly"]] <- 'true'
                 }
               },
               "7" =
               {
                 if (i[["ContactID"]] > 0) {
                   user_data <- paste0("SELECT contact_ply_id , contact_email , contact_f_name ,contact_l_name from contacts
                                WHERE contact_org_id= ", org_id, " AND contact_id= ",i[["ContactID"]], ";")
                   user_data <- py$execute(user_data)
                   if (length(user_data) != 0) {
                     if (is.null(user_data[[1]]$contact_f_name) == FALSE) {
                       i[["user_name"]] <- paste0(" ", URLdecode(user_data[[1]]$contact_f_name), " ", URLdecode(user_data[[1]]$contact_l_name), "")
                     }
                     if (is.null(user_data[[1]]$contact_ply_id) == FALSE & user_data[[1]]$contact_ply_id > 0) {
                       i[["user_id"]] <- user_data[[1]]$contact_ply_id
                       i[["ContactID"]] <- 0
                     }
                   }
                   else {
                     warning("Error in getting contact data")
                   }
                   if (substr(i[["notes"]], 0, 1) == ",") {
                     notes <- stringr::str_remove(i[["notes"]], ',')
                     i[["notes"]] <- stringr::str_trim(notes)
                   }
                 }
               }

        )
if(!is.null(i[["currency_symbol"]])){ i[["currSymbol"]] <- i[["currency_symbol"]]}
currency_name <- if(!is.null(i[["currName"]]) && i[["currName"]] != ''){ i[["currName"]]} else{''}
currency_symbol <- if(!is.null(i[["currSymbol"]]) && i[["currSymbol"]]!='' ){ i[["currSymbol"]]} else{''}
currency_name_lowered <- if(currency_name != ''){ tolower(currency_name) } else {''}
if(i[["actionTypeID"]] %in% c(5,6,9,42,45)){
  if(currency_symbol != '$'){i[["currSymbol"]] <- currency_symbol}
  else if(currency_name_lowered == 'usd') {
    i[["currSymbol"]] <-'$'}
  else if(currency_name_lowered == 'aud') {
    i[["currSymbol"]] <-'AU$'}
  else if(currency_name_lowered == 'cad') {
    i[["currSymbol"]] <-'C$'}
  else if(currency_name_lowered == 'nzd') {
    i[["currSymbol"]] <-'NZ$'}
  else if(currency_name_lowered == 'sgd') {
    i[["currSymbol"]] <-'S$'}
  else if(currency_name_lowered == 'hkd') {
    i[["currSymbol"]] <-'HK$'}
  else if(currency_name_lowered == 'mxn') {
    i[["currSymbol"]] <-'Mex$'}
  else{
      i[["currSymbol"]] <- paste0("",toupper(currency_name)," ",currency_symbol," ") }
}

else{
  if('classID' %in% i && i[["classID"]] > 0){
    #IsAdmin <- if(data[[i]]$OrgID == org_id) {'true'} else {'false'}
    #player_ids <- if(data[[i]]$usrID != 0){data[[i]]$usrID} else{data[[i]]$ContactID}
    CurrSymbol <- CurrencySymbol(i[["country_id"]],currency_symbol,currency_name,org_id)
  }
  else{
    country_id <- if('country_id' %in% i && !is.null(i[["country_id"]])) {i[["country_id"]]} else {0}
    CurrSymbol <- getCurrencySymbol(country_id)
  }
  i[["CurrSymbol"]] <- if(CurrSymbol != '' && !is.null(CurrSymbol)){ CurrSymbol } else{ '$' }
}


     # appened date with dict of the log
        dect <- reticulate::py_dict(names(i),i)
        if (!is.na("date_data")){
                  date_data<-py$Notify_data(data=dect)
        }else{date_data<-py$Notify_data(dict_date=date_data,data=dect)}
      }
  }
      OrgData <- list(actionCreateDate=orgData[[1]]$accCreatedAt, accCreatedAt = orgData[[1]]$accCreatedAt, actionTime = orgData[[1]]$actionTime,adminEmail=orgData[[1]]$adminEmail,adminName = orgData[[1]]$adminName,adminStudio= orgData[[1]]$adminStudio,orgID = orgData[[1]]$orgID)
      if (length(data) == 0 && purrr::is_empty(orgData[[1]]$accCreatedAt)==FALSE && searchArr[[2]] >= 1 && purrr::is_empty(searchArr[[1]])==FALSE && (searchArr[[1]] == 2 || searchArr[[1]] == 1)) {
        # appened date with dict of the log
        NotifyData<-py$Notify_data(data=OrgData)
      }else{
      NotifyData <- date_data
      }
      return(py$success(result_data=r_to_py(list("NotifyData"=NotifyData,"OrgData"=OrgData))))
    }
    else { warning("Data is missing") }} ,
    error = function(err) {
      return(py$error(r_to_py(err)))},
    warning = function(warn) {
      return(py$error(r_to_py(warn)))
      }
  )
}

CurrencySymbol <- function(player_country_id,gameSymbol="",gameCurrencyName="",org_id=0){
org_country_id <- paste0("SELECT ply_country_id FROM players WHERE ply_id = ",org_id," ")
org_country_id <- py$execute(org_country_id)
  if(exists(player_country_id)==TRUE && is.null(player_country_id) ==TRUE){player_country_id <- 0}
  if(as.numeric(player_country_id) != as.numeric(org_country_id[[1]]$ply_country_id)){
    return(toupper(gameCurrencyName))
  }
  return(gameSymbol)
}

payment <- function(UserId, GameId, actionCreateDate="",subID=0) {
  where <- if(subID > 0){paste0("AND subscription_id= ",subID," ")} else {""}
  sql <- paste0("SELECT payment_id , refund_id , refund_amount,charge_currency FROM online_payments WHERE player_id  =", UserId, " AND game_id = ", GameId, " ",where," AND DATE(updated_at)= '", actionCreateDate, "'  ;")
  sql <- py$execute(sql, db_name = py$mysql_payment_db_name)
}

recurr_classes_notes <- function(class_id,gm_type,currency_symbol,actionCreateDate){
  tryCatch({
if(class_id < 0){
  return(warning("Class id required"))
}

games <- paste0("SELECT DISTINCT gm.gm_id , gm.gm_title , gm.gm_recurr_id , gm.gm_date FROM game AS gm JOIN game AS games ON (games.gm_date = gm.gm_date)
                      WHERE (gm.gm_id=",class_id," OR gm.gm_recurr_id=",class_id,")
                      AND games.gm_date >= gm.gm_date;")
games <- py$execute(games)
games_ids <- list()
games_title <- list()
if(length(games) > 0){
for(i in games){
  games_title <- append(games_title,i[['gm_title']])
  games_ids <- append(games_ids,i[['gm_id']])
}
}
guests_id <- list()
if(length(games_ids) > 0){
guests<- paste0("SELECT CONCAT(guest_fname  , ' ', guest_lname) AS cancelUsrName , guest_gm_id AS gm_ply_gm_id, guest_ply_id AS gm_ply_ply_id , 1 AS gm_ply_refunded
                        FROM guests
                        WHERE guest_gm_id IN (",toString(games_ids),")
                        UNION ALL
                        SELECT CONCAT(removed_guest_fname , ' ' , removed_guest_lname) AS cancelUsrName, removed_guest_gm_id AS gm_ply_gm_id , 0 AS gm_ply_ply_id , 1 AS gm_ply_refunded
                        FROM unregistered_removed_guests
                        WHERE removed_guest_gm_id IN (",toString(games_ids),") ")
guests <- py$execute(guests)

if (length(guests) > 0){
  for (i in guests){
    if(i[['gm_ply_ply_id']] > 0) {guests_id <- append(guests_id,as.numeric(i[['gm_ply_ply_id']]))}
  }
}
}
where <- if (length(guests_id) > 0) paste0("AND gm_ply_ply_id NOT IN (",toString(guests_id),") ") else ''
gm_players <- paste0("SELECT CONCAT( players.ply_fname , ' ', players.ply_lname ) AS cancelUsrName ,gm_ply_ply_id , gm_ply_gm_id ,gm_ply_refunded
                        FROM gm_players
                        LEFT JOIN players ON players.ply_id = gm_ply_ply_id
                        WHERE gm_ply_removed_by_admin = 1 ",where,"
                        AND gm_ply_status = 'r'
                        AND gm_ply_gm_id IN (",toString(games_ids),") ")
gm_players <- py$execute(gm_players)
guests <- append(guests,gm_players)

if(length(guests) > 0){
       guests <- refund_status(guests,gm_type,currency_symbol,actionCreateDate)
}
  #players_data <- list()

  final_pause_games_players <- vector(mode = "list", length = length(guests))
   for(j in 1:length(games)){
     foreach(k = guests, i = 1:length(final_pause_games_players)) %do% {
    if(games[[j]]$gm_id == k[['gm_ply_gm_id']]){
     k[['player_game_cancled_title']] <- games[[j]]$gm_title
     final_pause_games_players[[i]]$gm_date <- games[[j]]$gm_date
     final_pause_games_players[[i]]$gm_id <- games[[j]]$gm_id
     final_pause_games_players[[i]]$gm_recurr_id <- games[[j]]$gm_recurr_id
     final_pause_games_players[[i]]$gm_title <- games[[j]]$gm_title
     final_pause_games_players[[i]]$players_data <- append(final_pause_games_players[[i]]$players_data,py_dict(names(k),k))
    }
  }
   }
     return(final_pause_games_players)
  }
,error = function(err) {
      return(py$error(err))
      },
    warning = function(warn) {
      return(py$error(warn))}
  )
}

refund_status <- function(guests,gm_type,currency_symbol="",actionCreateDate){
players_ids <- list()
games_ids <- list()
refunded <- list()
for (j in guests){
if(j[["gm_ply_ply_id"]] > 0) { players_ids <- append(players_ids,as.numeric(j[["gm_ply_ply_id"]]))}
if(j[["gm_ply_gm_id"]] > 0) {games_ids <- append(games_ids,as.numeric(j[["gm_ply_gm_id"]]))}
if(j[["gm_ply_refunded"]] !="" && !is.null(j[["gm_ply_refunded"]])) { refunded <- append(refunded,as.numeric(j[["gm_ply_refunded"]]))}
}

for (k in 1:length(guests)){
  guests[[k]]$refunded_note <- ''
}

if(length(games_ids) == 0 ){ return ("") }


coupon <- paste0("SELECT ply_id,gm_id,(CASE WHEN (discount=100) THEN 'true' ELSE 'false' END) AS discount_value FROM coupon_uses LEFT JOIN coupons ON coupon_uses.coupon_id = coupons.id WHERE gm_id IN (",toString(games_ids),") AND ply_id IN (",toString(players_ids),") ORDER BY coupon_uses.updated_at DESC")
coupon <- py$execute(coupon)

coupon_list <- list()
if(length(coupon) > 0 ){
  for(k in coupon){
    if('discount_value ' %in% k && k[['discount_value']]!=''){
      coupon_list <- append(coupon_list,k)
    }
  }
  }
if(length(coupon_list) > 0){
      foreach(i = coupon_list,j = guests,k = refunded) %do% {
          if('refunded_note' %in% j && j[['refunded_note']] == '' && i[['ply_id']]==j[['gm_ply_ply_id']] && i[['gm_id']] == j[['gm_ply_gm_id']] && i[['discount_value']]== 'true' && k ==1){
            j[['refunded_note']] <- 'Used a 100% discount code - no refund due.'
          }
      }
}

sql <- paste0("SELECT player_id,game_id,refund_amount FROM online_payments WHERE player_id IN (",toString(players_ids),") AND game_id IN (",toString(games_ids),") AND DATE(updated_at) = '",actionCreateDate,"'  ;")
sql <- py$execute(sql, db_name = py$mysql_payment_db_name)

refund <- list()
if(length(sql) > 0){
  for(k in sql){
    if('refund_amount' %in% k && k[['refund_amount']]!=''){
      refund <- append(refund,k)
    }
  }
}
if(length(refund) > 0){
      foreach(i = refund,j = guests) %do% {
          if( 'refunded_note' %in% j  && j[['refunded_note']] == '' && i[['player_id']]==j[['gm_ply_ply_id']] && i[['game_id']]==j[['gm_ply_gm_id']] && i[['refund_amount']]!='' && i[['refund_amount']] > 0 ){
            j[['refunded_note']] <- paste0("Refunded ",currency_symbol," ",i[['refund_amount']],"" )
          }
        else if ('refunded_note' %in% j && j[['refunded_note']] == '' && i[['player_id']]==j[['gm_ply_ply_id']] && i[['game_id']]==j[['gm_ply_gm_id']] && i[['refund_amount']] !='' && i[['refund_amount']] == 0 ){
            j[['refunded_note']] <- paste0("No refund was due as the user did not pay to join the class.")
      }
}
}

GmPlysSql <- paste0("SELECT COUNT(gm_ply_id) AS numRows FROM gm_players WHERE gm_ply_gm_id IN (",toString(games_ids),") AND gm_ply_ply_id IN (",toString(players_ids),") AND gm_ply_refunded=0 AND gm_ply_created < '2021-12-20 08:50:00';")
GmPlysSql <- py$execute(GmPlysSql)
if(length(GmPlysSql) > 0 && GmPlysSql[[1]]$numRows > 0){
  subID <- paste0("SELECT adm_sub.id AS SubID,member_id,game_id FROM games_subscriptions gm_sub LEFT JOIN bundles.bundles adm_sub ON adm_sub.old_bundle_id = gm_sub.subscription_id
                                  WHERE (game_id IN (",toString(games_ids),") AND member_id IN (",toString(players_ids),") );")
  subID <- py$execute(subID)
  subs_ids <- list()
  for(k in subID){
    if( 'SubID' %in% k && k[['SubID']]!='' && k[['SubID']] > 0 && k[['refunded_note']] == '' ){
      subs_ids <- append(subs_id,k)
    }
  }
  if(length(subs_ids) > 0){
    foreach(i = subs_ids,j = guests) %do% {
        if('refunded_note' %in% j && j[['refunded_note']] == '' && i[['member_id']]== j[['gm_ply_ply_id']] && i[['game_id']]==j[['gm_ply_gm_id']] && i[['SubID']]!='' &&  i[['SubID']] > 0 ){
          j[['refunded_note']] <- paste0("Refunded via credit.")
        }
  }
}
}
else{
  subID <- paste0("SELECT gm_sub.subscription_id AS SubID,member_id,game_id FROM games_subscriptions gm_sub LEFT JOIN bundles.bundles adm_sub ON adm_sub.id = gm_sub.subscription_id
                                  WHERE (game_id IN (",toString(games_ids),") AND member_id IN (",toString(players_ids),") ) ;")
  subID<- py$execute(subID)
  subs_ids <- list()
if(length(subID) > 0){
  for(k in subID){
    if('SubID' %in% k && k[['SubID']]!='' && k[['SubID']] > 0 && k[['refunded_note']] == ''){
      subs_ids <- append(subs_id,k)
    }
  }
}
    if(length(subs_ids) > 0){
       foreach(i = subs_ids,j = guests) %do% {
          if('refunded_note' %in% j && j[['refunded_note']] == '' && i[['member_id']]==j[['gm_ply_ply_id']] && i[['game_id']]==j[['gm_ply_gm_id']] && i[['SubID']]!='' && i[['SubID']] > 0 ){
            j[['refunded_note']] <- paste0("Refunded via credit.") }
  }
    }
    }

foreach(i = refunded, j = guests ) %do% {
  if('refunded_note' %in% j && j[['refunded_note']] == ''  &&  i == 1){
    j[['refunded_note']] <- paste0("Added to class manually - no refund due.") }
  else if ('refunded_note' %in% j && j[['refunded_note']] == '' && exists(gm_type) && gm_type == 'y' && i==0 ) {j[['refunded_note']] <- paste0("No refund") }
}
  return(guests)
}

 getCurrencySymbol <- function(CountryID = 0) {
  tryCatch({
  if(CountryID %in% c(22,59,70,75,76,83,86,107,110,123,129,130,138,157,178,202,203,209)){CountryID <- 15}
  switch(paste0(CountryID),
             "15" =
               symbol <- '€',
             "14" =
               symbol <- '$',
             "32" =
               symbol <- 'R$',
             "235" =
               symbol <- '£',
             "35" =
               symbol <- 'лв',
             "40" =
               symbol <- 'C$',
             "60" =
               symbol <- 'Kč',
             "61" =
               symbol <- 'kr',
             "100" =
               symbol <- 'HK$',
             "103" =
               symbol <- '₹',
             "112" =
               symbol <- '¥',
             "135" =
               symbol <- 'RM',
             "144" =
               symbol <- '$',
             "159" =
               symbol <- 'NZ$',
             "166" =
               symbol <- 'kr',
             "177" =
               symbol <- 'zł',
             "182" =
               symbol <- 'lei',
             "200" =
               symbol <- 'S$',
             "215" =
               symbol <- 'kr',
             "216" =
               symbol <- 'CHF'
      )
      if (exists("symbol") == FALSE) {
        symbol <- '$'
      }
      return(symbol)
  }
    , error = function(err) {
      return(py$error(err))
      },
    warning = function(warn) {
      return(py$error(warn))}
 )
}
if (!interactive()) {
 args = commandArgs(trailingOnly=TRUE)
  if (length(args)==0) {
   print("error in arguments")
    quit()
  }else {
   data <- args[2]
    route <- args[1]
  if (route == "getActionLog") {
    print(getActionLog(py$json$loads(py$base64$b64decode(data)))) }}}
#print(getActionLog(py$json$loads(py$base64$b64decode('eyJvcmdfaWQiOiI1OTUyIiwidHlwZSI6ImFsbCIsInNlYXJjaEFyciI6eyJsaW1pdCI6MSwidHlwZSI6ImFsbCIsImFjdGlvbkZyb20iOiIxIiwiUGx5SUQiOiI1OTUyIiwic2VhcmNoVHh0IjoiYXlkaWUiLCJEZXZJRCI6IndpbmRvd3NfQ2hyb21lXzE3Mi4zMS40MS42MCIsIlRrbiI6ImE0Y2VlNGZiNjRlNzk3NzM1YmVkMzhjNzU4YjIzZTc2Yjc2MTJhNjEifX0=='))))
