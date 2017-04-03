# -*- coding:utf-8 -*-
# 将某一辆车的轨迹输出成json文件
# 经纬度为百度坐标系下
import json
from dao.taxi.TaxiDao import TaxiDao

class TaxiExport(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')
        self.datafile = open(name="E:/MyProject/WebStorm/taxi_trajectory_web/data/nanjing.json", mode='w')
        self.trajlist = []

    '''
    获取到所有出租车的数据
    '''
    def overalltaxi(self):
        vehicleidlist = self.taxidao.get_records('DISTINCT VehicleID', 'nanjingtaxi', '')
        num = len(vehicleidlist)
        i = 0
        for vehicleid in vehicleidlist:
            # 测试某一辆车
            if vehicleid[0] != "806814011053":
                continue
            #
            gpslist = self.taxidao.get_records('*', 'nanjingtaxi', "WHERE VehicleID='%s' ORDER BY Time" % vehicleid)
            print u"当前计算车辆 "+str(vehicleid)
            traj = []
            for point in gpslist:
                lon = point[8]
                lat = point[9]
                coord = {"coord": [lon, lat]}
                traj.append(coord)
            i += 1
            if i == 10:
                break
            print u"还剩 "+str(num -i)
            self.trajlist.append(traj)
    '''
    写入
    '''
    def writelonlat(self):
        self.datafile.write(json.dumps(self.trajlist))

if __name__ == "__main__":
    taxi = TaxiExport()
    taxi.overalltaxi()
    taxi.writelonlat()
