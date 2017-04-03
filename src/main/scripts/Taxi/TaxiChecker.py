# -*- coding:utf-8 -*-
# 预处理程序，将明显不符合要求的数据删除
import json
from dao.taxi.TaxiDao import TaxiDao


class TaxiChecker(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    '''
    获取到所有出租车的数据
    '''
    def overalltaxi(self):
        vehicleidlist = self.taxidao.get_records('DISTINCT VehicleID', 'nanjingtaxi', '')
        num = len(vehicleidlist)
        # 完成判断的数量
        i = 0
        # 不符合的vehicleid列表
        delvid = [[], [], []]
        for vehicleid in vehicleidlist:
            print u"当前计算车辆 "+str(vehicleid)
            i += 1
            print u"还剩 "+str(num - i)
            print u"---------------------------------"
            # 判断经纬度是否有出界的情况
            if self.checklonlat(vehicleid):
                self.taxidao.delvehicle(vehicleid)
                # delvid[0].append(vehicleid)
                continue
            # 判断载客状态是否有出界的情况
            if self.checkpassengerstate(vehicleid):
                self.taxidao.delvehicle(vehicleid)
                # delvid[1].append(vehicleid)
                continue
            # 判断重复记录
            if self.checktime(vehicleid):
                self.taxidao.delvehicle(vehicleid)
                # delvid[2].append(vehicleid)
                continue
        # datafile = open(name="error.json", mode='w')
        # datafile.write(json.dumps(delvid))

    '''
    1 判断经纬度的判断
    '''
    def checklonlat(self, vehicleid):
        # 经度
        templon = self.taxidao.get_records('DISTINCT Longitude',
                                           'nanjingtaxi',
                                           "WHERE VehicleID='%s' ORDER BY Longitude" % vehicleid)
        longitude1 = templon[0][0]
        longitude2 = templon[-1][0]
        if longitude1 < 118.36:
            return True
        if longitude2 > 119.23:
            return True
        # 纬度
        templat = self.taxidao.get_records('DISTINCT Latitude',
                                           'nanjingtaxi',
                                           "WHERE VehicleID='%s' ORDER BY Latitude" % vehicleid)
        latitude1 = templat[0][0]
        latitude2 = templat[-1][0]
        if latitude1 < 31.23:
            return True
        if latitude2 > 32.61:
            return True
        return False

    '''
    2 判断乘客状态的判断
    '''
    def checkpassengerstate(self, vehicleid):
        temparr = self.taxidao.get_records('DISTINCT PassengerState',
                                           'nanjingtaxi',
                                           "WHERE VehicleID='%s' ORDER BY PassengerState" % vehicleid)
        if len(temparr) != 2:
            return True
        if temparr[0][0] != 0:
            return True
        if temparr[1][0] != 1:
            return True
        return False

    '''
    3 判断时间和经纬度无变化的情况
    '''
    def checktime(self, vehicleid):
        templist = self.taxidao.get_records('Time,count(*) num',
                                            'nanjingtaxi',
                                            "WHERE VehicleID='%s' group by Time HAVING num>1 ORDER BY num DESC" % vehicleid)
        # temparr = self.taxidao.get_records('DISTINCT Time', 'nanjingtaxi', "WHERE VehicleID='%s' ORDER BY Time" % vehicleid)
        if templist[0][1] > 5:
            return True
        return False

if __name__ == "__main__":
    taxichecker = TaxiChecker()
    taxichecker.overalltaxi()