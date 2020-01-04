import mysql.connector


class SQLConnection:
    def __init__(self, debug = False):
        self.debugmode = debug
        self.config = { "host": None, "username": None, "password": None }
    
    def connect(self, config):
        if self.debugmode: print("[ pSQL ] + Attempting connection to {} with user {} ...".format(config["host"], config["username"]))
        self.db = mysql.connector.connect(host=config["host"], user=config["username"], passwd=config["password"])
        if self.debugmode: print("[ pSQL ] + Connection to {} established successfully !".format(config["host"]))
        self.config = config
        self.db_cursor = self.db.cursor()
        return self

    def db_connect(self, db_name):
        _db = SQLDatabase(debugMode = self.debugmode)
        _db.config = self.config
        _db.config["db_name"] = str(db_name)
        _db.init()
        return _db


class SQLDatabase:
    def __init__(self, debugMode = False):
        self.debugmode = debugMode
        self.config = { "host": None, "username": None, "password": None, "db_name": None }
    
    def init(self):
        if self.debugmode: print("[ pSQL ] + Creating database connection to {} from {} ...".format(self.config["db_name"], self.config["host"]))
        self.db = mysql.connector.connect(host=self.config["host"], user=self.config["username"], passwd=self.config["password"], database=self.config["db_name"])
        if self.debugmode: print("[ pSQL ] + Connection to {} from {} established !".format(self.config["db_name"], self.config["host"]))
        self.db_cursor = self.db.cursor()

