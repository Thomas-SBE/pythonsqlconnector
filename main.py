from src.SQL import SQLConnection, SQLDatabase

# ---------------------------------
#       CONFIGURATION
# ---------------------------------

config = {
    "host": "localhost",
    "username": "root",
    "password": ""
}

# ---------------------------------
#      CONNECTING TO SERVER
#          & DATABASE
# ---------------------------------

connection = SQLConnection(debug=True).CONNECT(config)
database = connection.DB_CONNECT("memoryleak")


print(database.SHOW_COLUMNS("users"))
print(database.SELECT_ALL("users", ref="mail"))
print(database.SELECT_WHERE("users", "uid", "1"))