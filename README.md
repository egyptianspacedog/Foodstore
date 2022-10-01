# Foodstore
Programs designed to update and maintain a virtual pantry database, and a startup script to alert of any pending expirations.

The 3 programs utilise Python (with SQL queries housed within).

1) food_inserter_remover:
    A straightforward program allowing the user to choose between adding or removing a food item to/from the database's [Products] table.
    
2) bulk_inserter:
    A program written to insert an initial .csv food dataset into the created database.
    
3) store_checker:
    A script designed to run at computer startup, which reads and scans through the entire [Products] table, identifying which (if any) products to notify the user about.
