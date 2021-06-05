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
        conn = pymysql.Connect(host=const.DB_HOST, port=int(const.DB_PORT), user=const.DB_ACCOUNT, passwd=const.DB_PASSWORD, db='migrate',charset='utf8')
        # conn = pymysql.Connect(host='172.105.230.31', user='root', passwd='password', db='university',charset='utf8')
        # conn = pymysql.Connect(host='172.105.230.31',user='root',passwd='password',db='university',charset='utf8')
        self.conn = conn
    def getMigrate(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("select * from `migrate`.`migrate`;")
            data = []
            result=[]
            for row in cursor.fetchall():
                obj = {}
                for i, value in enumerate(row):
                    log.debug(cursor.description[i][0] + ':'+ str(value))
                    obj[cursor.description[i][0]]= value.strftime("%Y/%m/%d %H:%M:%S") if type(value) is datetime.date else str(value)
                data.append(obj)
            for record in data:
                result.append(record.get('name'))
            return result
        except Exception as e:
            log.info( "getMigrate error: " + cursor._executed)
            utils.except_raise(e)
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def addMigrate(self,name):
        cursor = self.conn.cursor()
        sql = "INSERT INTO `migrate`.`migrate` (name) VALUES ( %s )"
        val = (name)
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