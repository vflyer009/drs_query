import mysql.connector as mysql_connector


# SQL Database Config
db_connection = mysql_connector.connect(
  host="localhost",
  user="root",
  database="dev_drs_ad"
)


def lookup_ad(make, model):
    if make and model:
        print(f"Starting AD Lookup for {make} {model}")
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            f"SELECT `AD Number`, UNID FROM AD LIMIT 1"
        )
        ad_results = db_cursor.fetchall()
        db_cursor.close()

        return ad_results # Returns list of tuples
    return []
