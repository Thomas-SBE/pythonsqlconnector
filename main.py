from src.SQL import SQLConnection, SQLDatabase, SQLPermissions

# ---------------------------------
#       CONFIGURATION
# ---------------------------------

config = {
    "host": "localhost",
    "username": "root",
    "password": ""
}

perms = SQLPermissions().preset(SQLPermissions.READ_ONLY)

# ---------------------------------
#      CONNECTING TO SERVER
#          & DATABASE
# ---------------------------------

connection = SQLConnection(debug=True, custom_permissions=perms).CONNECT(config)
database = connection.DB_CONNECT("memoryleak")

# ---------------------------------
#      SERVER & DATABASE
#         MANAGEMENT
# ---------------------------------

connection.CREATE_DATABASE("abcd")
connection.DROP_DATABASE("abcd")

database.CREATE_TABLE("abc", ("uid", "uideux"))
database.DROP_TABLE("abc")

database.SELECT_WHERE("users", "uid", "1")
database.SELECT_ALL("users")
database.UPDATE("users", {"uid": "1"}, {"uid": "abc"})
database.DELETE("users", {"uid": "abc"})
database.INSERT("users", {"uid": "1234"})
