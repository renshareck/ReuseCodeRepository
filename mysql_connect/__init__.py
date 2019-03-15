import MySQLdb
import ConfigParser

class import_sql:

    def __init__(self):

        conf = ConfigParser.ConfigParser()
        conf.read("setting.conf")

        self.db_host = conf.get("section", "dhost")
        self.db_user = conf.get("section", "user")
        self.db_passwd = conf.get("section", "passwd")
        self.db_port = conf.get("section", "port")
        self.db_charset = conf.get("section", "charset")
        self.database = conf.get("section", "database")
