# **Python - Simple SQL Connector**

**simpleSQL** is a very simple & easy to use python library as it contains all the simple functions to communicate between your python scripts & your SQL server.

# Current Functionalities

 - Create Database
 - Drop Database
 - Create Table
 - Drop Table
 - Select All & Where
 - Insert
 - Update
 - Delete


# **Documentation**

## **Getting Started**

Setting up simpleSQL is simple, the syntax stays the same and is based on a simple concept :

There is a **Connection** that connects to your *Server*.
From this *Connection* you create **DatabaseConnections** to connect to specific *Databases*.

**Connection** is managed by a **SQLConnection** class.
**Databases Connections** are managed by a **SQLDatabase** class.


### The Basic Code would be :

	from pSQL import SQLConnection, SQLDatabase

	config = {
		"host": "<your host address>",
		"username": "<your database username>",
		"password": "<your user password>"
	}

	connection = SQLConnection().CONNECT(config)
	database = connection.DB_CONNECT("<your database name>")

-------------------------

`from pSQL import SQLConnection, SQLDatabase`  
**↑** This imports the library to be used

`config = { "host": "<your host address>", "username": "<your database username>", "password": "<your user password>"}`  
**↑** This is the basic configuration of your *Connection* to the server.

`connection = SQLConnection().CONNECT(config)`  
**↑** This establishes a connection to the server, with the given configuration dict.

`database = connection.DB_CONNECT("<your database name>")`  
**↑** This creates a *DatabaseConnection* to a given database name from the *Connection* to the server.

---

## **Advanced Functionalities** 

### **Debug Option**

This will display all operations made by the *Connection* & *DatabaseConnection*.

Simply add `debug=True` in :  
	
	connection = SQLConnection(debug=True).CONNECT(config)

--- 

### **Permissions**

All operation need a permission to be active so they can be executed, all thoses permissions are stored in a *SQLPermissions* class that is also an attribute of a *Connection* class named `permissions`.

By default all permissions are allowed , but changing it to a preset or setting it up manually is strongly recomanded as it prevents unwanted actions.

**To manage permissions you need to import `SQLPermissions` class .**

	from pSQL import SQLConnection, SQLDatabase, SQLPermissions

Then you can either create a custom made SQLPermission, by tweaking the booleans inside the class, or use a preset.

**→ Using a preset :**

	perms = SQLPermissions().preset(SQLPermissions.READ_ONLY)
	connection = SQLConnection( custom_permissions=perms).CONNECT(config)

***Presets are :***  
- ALL_ACCESSES
- READ_ONLY
- WRITE_AND_READ
- TABLE_ONLY


**→ Customizing permissions :**

	perms = SQLPermissions()

	perms.CreateTablePermission = True
	perms.DropDatabasePermission = True

	connection = SQLConnection( custom_permissions=perms).CONNECT(config)

By generating a SQLPermission all is set to False by default , you have no rights until you manually set them.

***Permissions are :***

- SelectPermission
- UpdatePermission
- InsertPermission
- DeletePermission
- CreateDatabasePermission
- CreateTablePermission
- DropTablePermission
- DropDatabasePermission

# **Syntaxes**

## **SQL Connection** (Server Operations)

### → **CREATE_DATABASE** :

`connection.CREATE_DATABASE("<database name>")`

**code::** 
	
> SQLConnection.CREATE_DATABASE( **str** *db_name* )

**return::**

> *Nothing*

---

### → **GET_DATABASES** :

`connection.GET_DATABASES()`

**code::** 
	
> SQLConnection.GET_DATABASES()

**return::**

> *List*  
> `["<database1 name>", "<database2 name>", "<database3 name>", ...]`

---

### → **DROP_DATABASE** :

`connection.DROP_DATABASE("<database name>")`

**code::** 
	
> SQLConnection.DROP_DATABASE( **str** *db_name* )

**return::**

> *Nothing*

---

## **SQL Database** (Database & Table Operations)

### → **SHOW_COLUMNS** :

`connection.SHOW_COLUMNS("<table name>")`

**code::** 
	
> SQLConnection.SHOW_COLUMNS( **str** *table* )

**return::**

> *tuple*  
> `('column1', 'column2', ...)`

--- 

### → **SELECT_WHERE** :

> **Note : For now it only selects the first occurence !**

`connection.SELECT_WHERE("<table name>", "<column>", "<target value>")`

**code::** 
	
> SQLConnection.SELECT_WHERE( **str** *table* , **str** *key*, **str** *value*)

**return::**

> *dict*  
> `{"<column1>: "<value>", "<column2>": <value>, ...}`

---

### → **SELECT_ALL** :

`connection.SELECT_ALL("<table name>")`

**code::** 
	
> SQLConnection.SELECT_ALL( **str** *table* , (optional) **str** *ref*)

*ref* if a column name , its values will be used as key for the returned dict if provided 

**return::**

**With** ***ref*** **:**

> *2 dimensional dict*  
> `{"<value of ref column 1>" : {"<column 1>": "<value>", "<column 2>": "<value>", ...}, "<value of ref column 2>": {"<column 1>": "<value 2>", "<column 2>": "<value 2>", ...} }`

**Without** ***ref*** **:**
> `{0 : {"<column 1>": "<value>", "<column 2>": "<value>", ...}, 1: {"<column 1>": "<value 2>", "<column 2>": "<value 2>", ...} }`

---

### → **INSERT** :


`connection.INSERT("<table name>", {"column": "value", "column2": "value2"})`

**code::** 
	
> SQLConnection.INSERT( **str** *table* , **dict** *keyvalues*)

**return::**

> *Nothing*

---

### → **UPDATE** :


`connection.UPDATE("<table name>", {"column": "value", "column2": "value2"}, {"column3" : "referencevalue"})`

**code::** 
	
> SQLConnection.UPDATE( **str** *table* , **dict** *keyvalues*, **dict** *references*)

**return::**

> *Nothing*

---

### → **DELETE** :

`connection.DELETE("<table name>", {"column": "value"})`

**code::** 
	
> SQLConnection.DELETE( **str** *table* , **dict** *references*)

**return::**

> *Nothing*

---

### → **CREATE_TABLE** :

> **Note : This script only handles databases with TEXT values in tables , it automaticly sets all columns value type to TEXT when using this function !**

`connection.CREATE_TABLE("<table name>", ["column1", "column2"])`

**code::** 
	
> SQLConnection.CREATE_TABLE( **str** *table_name* , **list** *columns*)

**return::**

> *Nothing*

---

### → **GET_TABLES** :

`connection.GET_TABLES()`

**code::** 
	
> SQLConnection.GET_TABLES()

**return::**

> *list*  
> `['table1', 'table2', ...]`

---

### → **DROP_TABLE** :

`connection.DROP_TABLE("<table name>")`

**code::** 
	
> SQLConnection.DROP_TABLE( **str** *table_name* )

**return::**

> *Nothing*