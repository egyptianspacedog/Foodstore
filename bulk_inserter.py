import csv
import pyodbc

def main():
    with open("FILE_PATH\food_store.csv", 'r') as foods:
        food_read = csv.reader(foods)
        productlist = []

        for line in food_read:
            item = line[0]
            expiry_date = line[1]
            notice = line[2]

            sql_insert(item, expiry_date, notice)


# insert statement to populate table
def sql_insert(item, expiry_date, notice):
    conn = pyodbc.connect("Driver={SQL Server Native client 11.0};"               
               "Server=SERVER_NAME;"
               "username=SERVER_NAME\USER"
               "Database=foodstoreDB;"
               "Trusted_Connection=yes;")

    cursor = conn.cursor()

    cursor.execute(
            """
            USE foodstoreDB;
            INSERT INTO products (product_name, end_date, notice_months)
            VALUES (?, ?, ?);
            """,
            item, expiry_date, notice
        )
    conn.commit()

main()
