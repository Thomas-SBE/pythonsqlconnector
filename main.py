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

connection = SQLConnection(debug=True).connect(config)
database = connection.db_connect("memoryleak")