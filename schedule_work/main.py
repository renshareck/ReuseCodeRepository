import pymysql
import schedule
import time
import configparser
import threading


class file_operate:
# this model should be singleton beacause its a genearator by 'yield'
# 这个模块必须为单例模式，这是由yield创建的生成器

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("new_setting.conf")

        self.file_path = conf.get("section", "new_file")
        self.i = 0
        self.time_flag = 1

    def get_file(self):
        with open(self.file_path, 'rt') as f:
            for content in f:
                if content:
                    yield content
                else:
                    return


class mysql_operate:

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("new_setting.conf")

        self.host = conf.get("section", "host")
        self.user = conf.get("section", "user")
        self.passwd = conf.get("section", "passwd")
        self.port = int(conf.get("section", "port"))
        self.charset = conf.get("section", "charset")
        self.database = conf.get("section", "database")

        self.i = 0
        self.time_flag = 1

        # instance 'file_operate'
        # 实例化
        self.file_op = file_operate()
        self.file_handle = self.file_op.get_file()

    def connect_db(self):
        # ---------------------------
        print("Begin connect!", time.ctime())
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database, charset=self.charset, port=self.port)
        self.cursor = self.conn.cursor()
        self.conn.autocommit(1)
        print("connect to " + self.host)
        # ---------------------------

    def disconnect_db(self):
        # ---------------------------
        print("Commit and disconnect!", time.ctime())
        self.cursor.close()
        self.conn.close()
        print("disconnect with " + self.host)
        # ---------------------------

    def excute_sql(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    def import_data(self):
        self.connect_db()
        self.excute_sql("set wait_timeout = 28800;")
        self.excute_sql("show variables like '%timeout%';")
        for content in self.file_handle:
            self.i = self.i + 1
            if(self.time_flag == 0):
                self.disconnect_db()
                return
            else:
                try:
                    test.excute_sql(content)
                    # time.sleep(23)
                    print(self.i, time.ctime())
                except Exception as e:
                    print(self.i, e, time.ctime())
        print("All end!", time.ctime())
        self.disconnect_db()

    def start_import(self):
        print("Begin!", time.ctime())
        self.time_flag = 1

    def pause_import(self):
        print("Pause!", time.ctime())
        self.time_flag = 0

    def import_task(self):
        threading.Thread(target=self.import_data).start()

    def start_task(self):
        threading.Thread(target=self.start_import).start()

    def pause_task(self):
        threading.Thread(target=self.pause_import).start()

    def main(self):
        schedule.every().day.at("8:00").do(self.start_task)
        schedule.every().day.at("21:00").do(self.pause_task)
        schedule.every().day.at("10:00").do(self.import_task)
        
        # schedule.every().day.at("15:02").do(self.start_task)
        # schedule.every().day.at("15:00").do(self.pause_task)
        # schedule.every().day.at("15:04").do(self.import_task)
        # schedule.every().day.at("15:07").do(self.pause_task)        
        # schedule.every().day.at("15:09").do(self.start_task)
        # schedule.every().day.at("15:11").do(self.import_task)
        
        threading.Thread(target=self.import_task).start()
        while(True):
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    test = mysql_operate()
    test.main()
