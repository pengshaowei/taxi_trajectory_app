# -*- coding:utf-8 -*-
# 识别上下车行为，将其输出到record表
#
import uuid
from dao.taxi.TaxiDao import TaxiDao


class ExportTrip(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')
        self.recordls = []

    def caltrip(self):
        vehicleidlist = self.taxidao.get_records('DISTINCT VehicleID', 'nanjingtaxi', '')
        num = len(vehicleidlist)
        # 完成判断的数量
        i = 0
        for vehicleid in vehicleidlist:
            print u"当前计算车辆 "+str(vehicleid[0])
            i += 1
            print u"还剩 "+str(num - i)
            print u"---------------------------------"
            prestate = 0
            # 循环判断车的单个轨迹点的
            gpslist = self.taxidao.get_records('*', 'nanjingtaxi', "WHERE VehicleID='%s' ORDER BY Time" % vehicleid)
            for point in gpslist:
                # 载客状态point[7]
                state = point[7]
                if state != prestate:
                    # 上车行为
                    if state == 1:
                        vid = point[1]
                        stime = point[2]
                        slon = point[3]
                        slat = point[4]
                    # 下车行为
                    if state == 0:
                        etime = point[2]
                        elon = point[3]
                        elat = point[4]
                if state == 0 and prestate == 1:
                    record = {
                        "Guid": uuid.uuid1(),
                        "VehicleID": vid,
                        "STime": stime,
                        "SLon": slon,
                        "SLat": slat,
                        "ETime": etime,
                        "ELon": elon,
                        "ELat": elat,
                        "OverTime": (etime-stime).total_seconds()
                    }
                    if len(record) == 9:
                        self.recordls.append(record)
                    else:
                        print '执行错误'
                    record = {}
                prestate = state

    def saverecord(self):
        self.taxidao.save_records('record', self.recordls)
        pass


if __name__ == "__main__":
    taxiexporter = ExportTrip()
    taxiexporter.caltrip()
    taxiexporter.saverecord()
