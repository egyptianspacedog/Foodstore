#!/usr/bin/env python3

import pyodbc
import pandas as pd
import datetime
import sys

def main():
    if len(sys.argv) != 2:
        print("USAGE: py food.py MODE (add/delete). Please try again.")
        exit()

    if sys.argv[1].lower() == "add":
        add_food()
    elif sys.argv[1].lower() == "delete":
        delete_food()
    else:
        print("USAGE: py food.py MODE (add/delete). Please try again.")
        exit()
   


# adds food + attributes to [foodstoreDB].[dbo].[products]
def add_food():
    item = input("Food type: ")
    expiry_date = datetime.datetime.strptime(input("Expiry Date: "),"%d/%m/%Y")
    notice = int(input("Warning time (months): "))
    
    cnxn = pyodbc.connect("Driver={SQL Server Native client 11.0};"               
               "Server=SERVER_NAME;"
               "username=SERVER_NAME\USER"
               "Database=foodstoreDB;"
               "Trusted_Connection=yes;")
    cursor = cnxn.cursor()

    cursor.execute(
            """
            INSERT INTO [foodstoreDB].[dbo].[products] (product_name, end_date, notice_months)
            VALUES (?, ?, ?);
            """,
            item, expiry_date, notice
        )
    cnxn.commit()

    print("\nItem added.\n\n")
    exit()


# removes food from [foodstoreDB].[dbo].[products]
def delete_food():
    item = str(input("Food type: "))
    
    cnxn = pyodbc.connect("Driver={SQL Server Native client 11.0};"               
               "Server=SERVER_NAME;"
               "username=SERVER_NAME\USER"
               "Database=foodstoreDB;"
               "Trusted_Connection=yes;")
    cursor = cnxn.cursor()

    items = select_food(item, cnxn).values.tolist()

    to_delete = choose_item(items)

    cursor.execute(
            """
            DELETE FROM [foodstoreDB].[dbo].[products]
            WHERE product_id=?;
            """,
            to_delete
        )
    cnxn.commit()

    print("\nItem removed.\n\n")
    exit()


# select statement based on input, returning list of all matching items
def select_food(item, cnxn):
    data = pd.read_sql_query(
            """
            SELECT * FROM [foodstoreDB].[dbo].[products]
            WHERE product_name='%s'
            """ % item, cnxn
        )

    return data


# allows user to choose specific item to remove, returning its list index
def choose_item(items):
    print("\n")

    for i in range(len(items)):
        date = ordinaliser(items[i][2])
        print(f"[{i+1}] {items[i][1].title()} - Expiry Date: {date}")
    
    print("\n")

    index = items[int(input("Please choose an item to remove [N]: "))-1][0]

    return int(index)


# returns str of date + "ordinal suffix" i.e. st, nd, rd, etc.
def ordinaliser(date):
    day = int(date.strftime("%d"))
    suffixes = ["th", "st", "nd", "rd"]

    if day % 10 in [1,2,3] and day not in [11,12,13]:
        day = str(day) + suffixes[day % 10]
    else:
        day = str(day) + suffixes[0]

    return str(day + str(date.strftime(" %b %Y")))


main()
