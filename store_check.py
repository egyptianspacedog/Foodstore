#!/usr/bin/env python3

import pyodbc
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import messagebox


def main():
    # gets all dbo.products data as an array
    products = sql_read()

    # check each product to see if it's close to expiring
    to_expire = expiry_check(products)

    # generates the pop-up alerting of any soon-to-expire foods
    alert(to_expire)



def sql_read():
    # Connects to [foodstoreDB].[dbo].[products], and reads in all data, returning it as an array #

    cnxn = pyodbc.connect("Driver={SQL Server Native client 11.0};"               
               "Server=SERVER_NAME;"
               "username=SERVER_NAME\USER"
               "Database=foodstoreDB;"
               "Trusted_Connection=yes;")

    data = pd.read_sql_query(
        """
        SELECT * FROM [foodstoreDB].[dbo].[products];
        """, cnxn
        )
    
    products = data.values.tolist()

    return products



def expiry_check(list):
    # checks whether it's the right date to notify of impending expiration, then returns list of all such items (via (EXPIRATION DATE - MONTHS NOTICE) <= TODAY ) #
    expiring = []

    for line in list:
        warning_date = line[2] - relativedelta(months=line[3])
        
        if warning_date <= datetime.date.today():
            expiring.append(line)
    
    expiring = sorted(expiring, key = lambda x: x[2])

    return expiring



def ordinaliser(day):
    # returns str of day + "ordinal suffix" i.e. st, nd, rd, etc. #
    suffixes = ["th", "st", "nd", "rd"]

    if day % 10 in [1,2,3] and day not in [11,12,13]:
        return str(day) + suffixes[day % 10]
    else:
        return str(day) + suffixes[0]



def alert(items):
    # creates a pop-up window displaying expiring products #
    window=tk.Tk()
    window.withdraw()

    list = []

    for line in items:
        day = int(line[2].strftime("%d"))
        list.append(line[1].title() + " will expire on " + ordinaliser(day) + str(line[2].strftime(" %b %Y")))

    message = "\n\n".join(list)

    tk.messagebox.showinfo(
        "Expiring Products:",
        message
    )



main()