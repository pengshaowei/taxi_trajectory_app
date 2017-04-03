# -*- coding:utf-8 -*-
import traceback
import MySQLdb


class BaseDAO(object):
    def __init__(self, host, db, user, password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
    '''
    save a record.
    '''
    def save_record(self, table_name, record):
        db = MySQLdb.connect(self.host, self.db, self.user, self.password)
        cursor = db.cursor()
        try:
            placeholders = ','.join(['%s'] * len(record))
            columns = ','.join(record.keys())
            sql = "insert into %s( %s ) values ( %s )" % (table_name, columns, placeholders)
            cursor.execute(sql, record.values())
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()
    '''
    save a lot records.
    '''
    def save_records(self, table_name, records):
        db = MySQLdb.connect(host=self.host, db=self.db, user=self.user,passwd = self.password)
        cursor = db.cursor()
        for record in records:
            placeholders = ','.join(['%s'] * len(record))
            columns = ','.join(record.keys())
            sql = "insert into %s ( %s ) values ( %s )" % (table_name, columns,placeholders)
            try:
                cursor.execute(sql, record.values())
            except Exception, e:
                traceback.print_exc()
                print e
                break
        db.commit()
        cursor.close()
        db.close()
    '''
    get a lot records.
    '''
    def get_records(self, cols, table_name, where):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        records = []
        try:
            cursor.execute("select %s from %s %s" % (cols, table_name, where))
            records = cursor.fetchall()
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()
        return records
