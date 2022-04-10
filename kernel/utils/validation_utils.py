import database.response as response

def ViewGmsCalValidation(data):
    try:
        if data and type(data) is dict:
            m = 0
            date = 0
            gm = 0
            a = 0
            status = "ok"
            limit_start = 0
            try:
                if 'GmDate' in data and data['GmDate'] == "" or not isinstance(data['GmDate'], str):
                    pass
                else:
                    gm = 1
            except:
                status = "Invalid GmDate"

            if not isinstance(data['source'], str):
                status = "Invalid source"
            elif data['source'] == "ios" or data['source'] == "android":
                m += 1
            try:
                try:
                    if 'Month' not in data or int(data['Month']) < 0 or data['Month'] == "":
                        pass
                    else:
                        m += 1
                        date += 1
                    if 'Year' not in data or int(data['Year']) < 0 or data['Year'] == "":
                        pass
                    else:
                        m += 1
                        date += 1
                except:
                    pass

                try:
                    if 'Number' in data and int(data['Number']) <= 0:
                        Number = 1000000
                    else:
                        Number = data['Number']
                except:
                    Number = 1000000
                if 'limit' in data and int(data['limit']) < 0 and int(data['limit']) >Number:
                    status = "Invalid limit"
                else:
                    limit_start = data['limit']

                    # limit_start = (limit-1)*50
                if 'PlyID' in data and int(data['PlyID']) <= 0:
                    status = "Invalid PLyID"
                if 'daygroup' in data and int(data['daygroup']) <= 0:
                    status = "Invalid daygroup"
                try:
                    if 'aid' in data and int(data['aid']) <= 0:
                        pass
                    else:
                        a = 1
                except:
                    a = 0

                valid = {
                            "status": status, "m": m, "limit_start": limit_start,
                            "Number": Number, "date": date, "gm": gm, "a": a
                        }
                return valid

            except:
                valid = {
                            "status": "Invalid Input 1"
                        }
                return valid
    except Exception as e:
        valid = {
            "status": "Invalid Input 2"
        }
        return valid
