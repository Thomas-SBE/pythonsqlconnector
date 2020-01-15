"""
    SimpleSQL Connections & Database Management

    Full-Documentation on : https://github.com/Thomas-SBE/pythonsqlconnector

"""

import mysql.connector
import colorama

__version__ = "0.0.1"

# ----------------------------------
#     Simple coloured messages
# ----------------------------------

def succ(s):
    return colorama.Fore.GREEN + str(s) + colorama.Style.RESET_ALL
def err(s):
    return colorama.Fore.RED + str(s) + colorama.Style.RESET_ALL
def warn(s):
    return colorama.Fore.YELLOW + str(s) + colorama.Style.RESET_ALL


# ----------------------------------
#     Custom Exception Messages
# ----------------------------------

class SQLPermissionNotGranted:
    def __init__(self, accessed, perm, debugmode):
        if debugmode: print("{} [ {} ] - You cannot do this as the permission {} does not allow it !".format(err("-"), err("pSQL → " + accessed), warn(perm)))
class SQLActionResult:
    def __init__(self, action, table, amount, debugmode):
        if debugmode: print("{} [ {} ] - {} affected {} of {}.".format(succ("+"), succ("pSQL → " + action), action, warn(amount), warn(table)))
class SQLAlreadyExist:
    def __init__(self, typ, action, name, debugmode):
        if debugmode: print("{} [ {} ] - Cannot {} {} because the name {} already exists !".format(err("-"), err("pSQL → " + action + typ), warn(action), warn(typ), warn(name)))


# ----------------------------------
#     SQL Framework
# ----------------------------------

class SQLPermissions:
    
    ALL_ACCESSES = "#999"
    READ_ONLY = "#000"
    WRITE_AND_READ = "#050"
    TABLE_ONLY = "#005"
    
    def __init__(self):
        self.SelectPermission = False
        self.UpdatePermission = False
        self.InsertPermission = False
        self.DeletePermission = False
        self.CreateDatabasePermission = False
        self.CreateTablePermission = False
        self.DropTablePermission = False
        self.DropDatabasePermission = False

    def preset(self, mode):
        if mode == SQLPermissions.ALL_ACCESSES: 
            self.SelectPermission = True
            self.UpdatePermission = True
            self.InsertPermission = True
            self.DeletePermission = True
            self.CreateDatabasePermission = True
            self.CreateTablePermission = True
            self.DropTablePermission = True
            self.DropDatabasePermission = True
        elif mode == SQLPermissions.READ_ONLY:
            self.SelectPermission = True
            self.UpdatePermission = False
            self.InsertPermission = False
            self.DeletePermission = False
            self.CreateDatabasePermission = False
            self.CreateTablePermission = False
            self.DropTablePermission = False
            self.DropDatabasePermission = False
        elif mode == SQLPermissions.WRITE_AND_READ:
            self.SelectPermission = True
            self.UpdatePermission = True
            self.InsertPermission = True
            self.DeletePermission = True
            self.CreateDatabasePermission = False
            self.CreateTablePermission = False
            self.DropTablePermission = False
            self.DropDatabasePermission = False
        elif mode == SQLPermissions.TABLE_ONLY:
            self.SelectPermission = True
            self.UpdatePermission = True
            self.InsertPermission = True
            self.DeletePermission = True
            self.CreateDatabasePermission = False
            self.CreateTablePermission = True
            self.DropTablePermission = True
            self.DropDatabasePermission = False
        return self

class SQLConnection:
    def __init__(self, debug = False, custom_permissions = None):
        self.debugmode = debug
        colorama.init()
        self.config = { "host": None, "username": None, "password": None }
        self.permissions = SQLPermissions()
        self.permissions.preset(SQLPermissions.ALL_ACCESSES)
        if custom_permissions != None and type(custom_permissions) is type(SQLPermissions()): self.permissions = custom_permissions

    def CONNECT(self, config):
        if self.debugmode: print("{} [ {} ] - Attempting connection to {} with user {} ...".format(succ("+"), succ("pSQL"), warn(config["host"]), warn(config["username"])))
        self.db = mysql.connector.connect(host=config["host"], user=config["username"], passwd=config["password"])
        if self.debugmode: print("{} [ {} ] - Connection to {} established successfully !".format(succ("+"), succ("pSQL"), warn(config["host"])))
        self.config = config
        self.db_cursor = self.db.cursor()
        return self

    def DB_CONNECT(self, db_name):
        _db = SQLDatabase(self)
        _db.INIT(str(db_name))
        return _db

    def CREATE_DATABASE(self, db_name):
        if not self.permissions.CreateDatabasePermission: SQLPermissionNotGranted("CREATE DATABASE", "CreateDatabasePermission", self.debugmode);return
        if db_name in self.GET_DATABASES(): SQLAlreadyExist("DATABASE", "CREATE", db_name);return
        self.db_cursor.execute("CREATE DATABASE " + str(db_name))
        SQLActionResult("CREATE DATABASE", db_name, 1, self.debugmode)

    def GET_DATABASES(self):
        self.db_cursor.execute("SHOW DATABASES")
        return [x[0] for x in self.db_cursor]

    def DROP_DATABASE(self, db_name):
        if not self.permissions.DropDatabasePermission: SQLPermissionNotGranted("DROP DATABASE", "DropDatabasePermission", self.debugmode);return
        affected = 0
        if db_name in self.GET_DATABASES(): affected = 1
        self.db_cursor.execute("DROP DATABASE IF EXISTS " + str(db_name))
        SQLActionResult("DROP DATABASE", db_name, affected, self.debugmode)

class SQLDatabase:
    def __init__(self, master):
        self.master = master
    
    def INIT(self, db_name):
        self.mastername = db_name
        if self.master.debugmode: print("{} [ {} ] - Creating database connection to {} from {} ...".format(succ("+"), succ("pSQL"), warn(db_name), warn(self.master.config["host"])))
        self.db = mysql.connector.connect(host=self.master.config["host"], user=self.master.config["username"], passwd=self.master.config["password"], database=db_name)
        if self.master.debugmode: print("{} [ {} ] - Connection to {} from {} established !".format(succ("+"), succ("pSQL"), warn(db_name), warn(self.master.config["host"])))
        self.cursor = self.db.cursor()

    def SHOW_COLUMNS(self, table):
        self.cursor.execute("SHOW COLUMNS FROM `" + str(table) + "`")
        res = self.cursor.fetchall()
        final = [i[0] for i in res]
        return tuple(final)

    def SELECT_WHERE(self, table, key, value):
        if not self.master.permissions.SelectPermission: SQLPermissionNotGranted("SELECT", "SelectPermission", self.master.debugmode);return
        self.cursor.execute("SELECT * FROM `" + str(table) + "` WHERE " + str(key) + "='" + str(value) +"'")
        ret = self.cursor.fetchall()
        if len(ret) <= 0: return {}
        columns = self.SHOW_COLUMNS(table)
        final = {}
        for x in range(len(ret[0])):
            final[columns[x]] = ret[0][x]
        SQLActionResult("SELECT", str(table), len(ret), self.master.debugmode)
        return final

    def SELECT_ALL(self, table, ref = None):
        if not self.master.permissions.SelectPermission: SQLPermissionNotGranted("SELECT", "SelectPermission", self.master.debugmode);return
        self.cursor.execute("SELECT * FROM `" + str(table) + "` WHERE 1")
        res = self.cursor.fetchall()
        columns = self.SHOW_COLUMNS(table)
        refindex = -1
        if ref != None:
            for i in range(len(columns)):
                if columns[i] == ref: refindex = i; break
        final = {}
        for x in range(len(res)):
            _temp = {}
            for w in range(len(res[x])):
                _temp[columns[w]] = res[x][w]
            if refindex != -1:
                final[res[x][refindex]] = _temp
            else:
                final[x] = _temp
        SQLActionResult("SELECT", str(table), len(res), self.master.debugmode)
        return final

    def INSERT(self, table, keyvalues):
        if not self.master.permissions.InsertPermission: SQLPermissionNotGranted("INSERT", "InsertPermission", self.master.debugmode);return
        keys, values = "(", "("
        for k,v in keyvalues.items():
            keys += "`"+str(k)+"`,"
            values += '"'+str(v)+'",'
        self.cursor.execute("INSERT INTO `" + str(table) + "`" + keys[:-1] + ")" + " VALUES " + values[:-1] + ")" + "")
        self.db.commit()
        SQLActionResult("INSERT", str(table), self.cursor.rowcount, self.master.debugmode)

    def UPDATE(self, table, keyvalues, references):
        if not self.master.permissions.UpdatePermission: SQLPermissionNotGranted("UPDATE", "UpdatePermission", self.master.debugmode);return
        strtemp, reftemp = "", ""
        for k,v in keyvalues.items():
            strtemp += "`"+str(k)+'`="'+str(v)+'",'
        for k,v in references.items():
            reftemp += "`" + str(k) + '`="' + str(v) + '" &&'
        self.cursor.execute("UPDATE `" +str(table)+ "` SET " +strtemp[:-1]+ " WHERE " + reftemp[:-2])
        self.db.commit()
        SQLActionResult("UPDATE", str(table), self.cursor.rowcount, self.master.debugmode)

    def DELETE(self, table, references):
        if not self.master.permissions.DeletePermission: SQLPermissionNotGranted("DELETE", "DeletePermission", self.master.debugmode);return
        reftemp = ""
        for k,v in references.items():
            reftemp += "`" + str(k) + '`="' + str(v) + '" &&'
        self.cursor.execute("DELETE FROM `" +str(table)+ "` WHERE " + reftemp[:-2])
        self.db.commit()
        SQLActionResult("DELETE", str(table), self.cursor.rowcount, self.master.debugmode)

    def CREATE_TABLE(self, table_name, columns):
        if not self.master.permissions.CreateTablePermission: SQLPermissionNotGranted("CREATE TABLE", "CreateTablePermission", self.master.debugmode);return
        if table_name in self.GET_TABLES(): SQLAlreadyExist("TABLE", "CREATE", table_name, self.master.debugmode);return
        formatd = "("
        for v in columns:
            formatd += str(v) + " TEXT,"
        self.cursor.execute("CREATE TABLE " + str(table_name) + formatd[:-1] + ")")
        SQLActionResult("CREATE TABLE", self.mastername, 1, self.master.debugmode)

    def GET_TABLES(self):
        self.cursor.execute("SHOW TABLES")
        return [x[0] for x in self.cursor]

    def DROP_TABLE(self, table_name):
        if not self.master.permissions.DropTablePermission: SQLPermissionNotGranted("DROP TABLE", "DropTablePermission", self.master.debugmode);return
        affected = 0
        if table_name in self.GET_TABLES(): affected = 1
        self.cursor.execute("DROP TABLE IF EXISTS " + str(table_name))
        SQLActionResult("DROP TABLE", self.mastername, affected, self.master.debugmode)

