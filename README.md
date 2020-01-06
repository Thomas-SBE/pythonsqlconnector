# Python - Simple SQL Connector

**pSQL** is a very simple & easy to use python library as it contains all the simple functions to communicate between your scripts & your SQL server.

> **Note** : There is a permission system to prevent certain actions if you do not want them to occure.
> by default , all actions are locked , you need to use a SQLPermissions preset or set one up manualy as explained below ↓

## Current Functionalities 

 - Create Database
 - Drop Database
 - Create Table
 - Drop Table
 - Select All & Where
 - Insert
 - Update
 - Delete
## Example Script

    from src.SQL import SQLConnection, SQLDatabase, SQLPermissions
    
    config = {
	    "host": "localhost",
	    "username": "<your username>",
	    "password": "<your password>"
	}

	connection = SQLConnection().CONNECT(config)
	connection.permissions = SQLPermissions().preset(SQLPermissions.ALL_ACCESSES)
	database = connection.DB_CONNECT("<your db name>")

	results = database.SELECT_ALL("<table name>")

