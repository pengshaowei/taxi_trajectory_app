# -*- coding:utf-8 -*-

import MySQLdb
import traceback
from dao.BaseDAO import BaseDAO


class TaxiDao(BaseDAO):

    def __init__(self, host, db, user, password):
        BaseDAO.__init__(self, host, db, user, password)

    # 修改经纬度
    def callonlat(self, rid, lon, lat):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE nanjingtaxi SET Longitude = '%s',Latitude='%s' WHERE ID = '%s' " % (lon, lat, rid))
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()

    # 更新百度经纬度
    def calbdlonlat(self, rid, lon, lat):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE nanjingtaxi SET BDLon = '%s',BDLat='%s' WHERE ID = '%s' " % (lon, lat, rid))
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()

    # 更新匹配后的经纬度
    def calMatchlonlat(self, rid, lon, lat):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE nanjingtaxi SET MatchingLon = '%s',MatchingLat='%s' WHERE ID = '%s' " % (lon, lat, rid))
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()
    # 更新匹配后的经纬度
    def calMatchlonlats(self, records):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        for r in records:
            try:
                cursor.execute(
                    "UPDATE nanjingtaxi SET MatchingLon = '%s',MatchingLat='%s' WHERE ID = '%s' " % (r[1], r[2], r[0]))
            except Exception, e:
                traceback.print_exc()
                print e
                break
        db.commit()
        cursor.close()
        db.close()

    # 删除整车记录
    def delvehicle(self, vehicleid):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        vehicleidlist = []
        try:
            cursor.execute("delete from nanjingtaxi where VehicleID='%s'" % vehicleid)
            vehicleidlist = cursor.fetchall()
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()
        return vehicleidlist
    # 删除整车记录
    def deleteid(self,ridls):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        try:
            for rid in ridls:
                cursor.execute("delete from nanjingtaxi where ID='%s'" % rid[0])
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()

    # 计算字段数量
    def calFieldtime(self, field, vehicleid):
        db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        cursor = db.cursor()
        resultlist = []
        try:
            cursor.execute("select DISTINCT %s FROM nanjingtaxi WHERE VehicleID='%s'" % field, vehicleid)
            resultlist = cursor.fetchall()
        except Exception, e:
            print e
        db.commit()
        cursor.close()
        db.close()
        return resultlist






