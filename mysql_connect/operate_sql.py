import pymysql
import configparser

class mysql_operate:

    def __init__(self):

        conf = configparser.ConfigParser()
        conf.read("setting.conf")

        self.host = conf.get("section", "host")
        self.user = conf.get("section", "user")
        self.passwd = conf.get("section", "passwd")
        self.port = int(conf.get("section", "port"))
        self.charset = conf.get("section", "charset")
        self.database = conf.get("section", "database")


    def connect_db(self):
        # ---------------------------
        print("Begin connect!")
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database, charset=self.charset, port=self.port)
        self.cursor = self.conn.cursor()
        print("connect to " + self.host)
        # ---------------------------

    def disconnect_db(self):
        # ---------------------------
        print("Commit and disconnect!")
        #self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print("disconnect with " + self.host)
        # ---------------------------

    def excute_sql(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            print(row)

if __name__ == "__main__":
    test = mysql_operate()
    test.connect_db()
    test.excute_sql("select * from fips")
    test.disconnect_db()