import mysql.connector

import database.config as config


def execute(query, db_name=config.mysql_db_name):
    try:
        username = config.mysql_user
        password = config.mysql_password
        if "SELECT" in query or "select" in query:
            mydb = mysql.connector.connect(host=config.mysql_read_url, user=username, password=password,
                                           database=db_name)
            if mydb.is_connected():
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(query)
                result = mycursor.fetchall()
                return result
        elif "CALL" in query or "call" in query:
            mydb = mysql.connector.connect(host=config.mysql_read_url, user=username, password=password,
                                           database=db_name)
            if mydb.is_connected():
                mycursor = mydb.cursor(dictionary=True, buffered=True)
                mycursor.callproc("GamePlayers", ('3521', '1', '0', '50'))
                for result in mycursor.stored_results():
                    return result.fetchall()
        else:
            mydb = mysql.connector.connect(host=config.mysql_write_url, user=username, password=password,
                                           database=db_name)
            if mydb.is_connected():
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(query)
                mydb.commit()
    except mysql.connector.Error as err:
        return f"Something went wrong: {err}"
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
