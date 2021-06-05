import log
import pymysql
import datetime
import json
import const
import utils

log = log.logging.getLogger(__name__)


class Database(object):
    conn = {}
    def __init__(self):
        log.debug(const.DB_PORT)
        log.debug(const.DB_HOST)
        log.debug(const.DB_ACCOUNT)
        log.debug(const.DB_PASSWORD)
        conn = pymysql.Connect(host=const.DB_HOST, port=int(const.DB_PORT), user=const.DB_ACCOUNT, passwd=const.DB_PASSWORD, db='gogolook',charset='utf8')
        self.conn = conn
    def getTasks(self,data):
        cursor = self.conn.cursor()
        try:
            if data == None:
                cursor.execute("select * from `gogolook`.`tasks`;")
            elif data == 'add':
                cursor.execute("select * from gogolook.tasks order by 1 desc limit 1;")
            else:
                cursor.execute("select * from `gogolook`.`tasks` where id = %s;",data.get('id'))
            data = []
            for row in cursor.fetchall():
                obj = {}
                for i, value in enumerate(row):
                    log.debug(cursor.description[i][0] + ':'+ str(value))
                    obj[cursor.description[i][0]]= value.strftime("%Y/%m/%d %H:%M:%S") if type(value) is datetime.date else value
                data.append(obj)
            return data
        except Exception as e:
            log.info( "getTasks error: " + cursor._executed)
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def addTasks(self,data):
        cursor = self.conn.cursor()
        sql = "INSERT INTO `gogolook`.`tasks` (name) VALUES ( %s )"
        val = (data.get('name'))
        log.info(val)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            return True
        except Exception as e:
            log.info("query '{}' with params {} failed with {}".format(sql, val, e))
            log.info(cursor._executed)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def editTasks(self,data):
        cursor = self.conn.cursor()
        sql = "UPDATE `gogolook`.`tasks` SET name = %s, status = %s;"
        val = (data.get('name'), data.get('status'))
        log.info(val)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            return True
        except Exception as e:
            log.info("query '{}' with params {} failed with {}".format(sql, val, e))
            log.info(cursor._executed)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def delTasks(self,data):
        cursor = self.conn.cursor()
        sql = "DELETE FROM `gogolook`.`tasks` WHERE id = %s"
        val = (data)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            log.info(cursor.rowcount)
            return True
        except Exception as e:
            log.info( "delTasks error: " + cursor._executed)
            raise e
        finally:
            cursor.close()
            self.conn.close()