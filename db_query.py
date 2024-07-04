import mysql.connector as mysql_connector


# SQL Database Config
db_connection = mysql_connector.connect(
  host="localhost",
  user="root",
  database="dev_drs_ad"
)


def lookup_ad(make, model, set_limit):
    if make and model:
        print(f"Starting AD Lookup for {make} {model}")
        db_cursor = db_connection.cursor()
        query = f"SELECT `AD Number`, UNID FROM AD WHERE Model LIKE '%{model}%' LIMIT {set_limit}" 
        db_cursor.execute(query)
        ad_results = db_cursor.fetchall()
        db_cursor.close()

        return ad_results  # Returns list of tuples
    return []
