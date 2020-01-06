import mysql.connector


class SQLConnection:
    def __init__(self, debug = False):
        self.debugmode = debug
        self.config = { "host": None, "username": None, "password": None }
    
    def CONNECT(self, config):
        if self.debugmode: print("[ pSQL ] + Attempting connection to {} with user {} ...".format(config["host"], config["username"]))
        self.db = mysql.connector.connect(host=config["host"], user=config["username"], passwd=config["password"])
        if self.debugmode: print("[ pSQL ] + Connection to {} established successfully !".format(config["host"]))
        self.config = config
        self.db_cursor = self.db.cursor()
        return self

    def DB_CONNECT(self, db_name):
        _db = SQLDatabase(debugMode = self.debugmode)
        _db.config = self.config
        _db.config["db_name"] = str(db_name)
        _db.INIT()
        return _db


class SQLDatabase:
    def __init__(self, debugMode = False):
        self.debugmode = debugMode
        self.config = { "host": None, "username": None, "password": None, "db_name": None }
    
    def INIT(self):
        if self.debugmode: print("[ pSQL ] + Creating database connection to {} from {} ...".format(self.config["db_name"], self.config["host"]))
        self.db = mysql.connector.connect(host=self.config["host"], user=self.config["username"], passwd=self.config["password"], database=self.config["db_name"])
        if self.debugmode: print("[ pSQL ] + Connection to {} from {} established !".format(self.config["db_name"], self.config["host"]))
        self.cursor = self.db.cursor()

    def SHOW_COLUMNS(self, table):
        self.cursor.execute("SHOW COLUMNS FROM `" + str(table) + "`")
        res = self.cursor.fetchall()
        final = [i[0] for i in res]
        return tuple(final)

    def SELECT_WHERE(self, table, key, value):
        self.cursor.execute("SELECT * FROM `" + str(table) + "` WHERE " + str(key) + "='" + str(value) +"'")
        ret = self.cursor.fetchall()
        if len(ret) <= 0: return {}
        columns = self.SHOW_COLUMNS(table)
        final = {}
        for x in range(len(ret[0])):
            final[columns[x]] = ret[0][x]
        return final

    def SELECT_ALL(self, table, ref = None):
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
        return final

    def INSERT(self, table, keyvalues):
        keys = [k for k,v in keyvalues.items()]
        values = [v for k,v in keyvalues.items()]
        self.cursor.execute("INSERT INTO `" + str(table) + "`" + str(tuple(keys)).replace("'", "`") + " VALUES " + str(tuple(values)) + "")
        self.db.commit()

    def UPDATE(self, table, keyvalues, references):
        strtemp, reftemp = "", ""
        for k,v in keyvalues.items():
            strtemp += "`"+str(k)+'`="'+str(v)+'",'
        for k,v in references.items():
            reftemp += "`" + str(k) + '`="' + str(v) + '" &&'
        self.cursor.execute("UPDATE `" +str(table)+ "` SET " +strtemp[:-1]+ " WHERE " + reftemp[:-2])
        self.db.commit()
