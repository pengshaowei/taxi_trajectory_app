# -*- coding:utf-8 -*-
# 将某一辆车的数据转换为百度坐标系

from dao.taxi.TaxiDao import TaxiDao
import service.CoordinateTransferService

class Transfer(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    '''
    获取到所有出租车的数据
    '''
    def overalltaxi(self):
        gpslist = self.taxidao.get_records('*', 'nanjingtaxi', "where VehicleID = '806814011053' ")
        for gps in gpslist:
            rid = gps[0]
            lon = gps[3]
            lat = gps[4]
            l = service.CoordinateTransferService.wgs84togcj02(lon, lat)
            l = service.CoordinateTransferService.gcj02tobd09(l[0], l[1])
            self.taxidao.callonlat(rid, l[0], l[1])


if __name__ == "__main__":
    taxi = Transfer()
    taxi.overalltaxi()
