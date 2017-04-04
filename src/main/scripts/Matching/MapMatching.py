# -*- coding:utf-8 -*-
# 地图匹配算法 + 最热出行道路的算法（待修缮）
# 路网所在路径 roadpath
# 轨迹点在数据库中 db=taxi table=nanjingtaxi
from dao.taxi.TaxiDao import TaxiDao
from shapely.geometry import LineString
from shapely.geometry import Point
import service.CoordinateTransferService
import shapefile
import time
roadshppath = 'E:/MyData/road/nanjing.shp'

class Matching(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    def main(self, radius):
        # 存储最热道路的键值对
        hotrate = {}
        sf = shapefile.Reader(roadshppath)
        shapes = sf.shapes()
        road = []
        print "Read road data..."
        for shape in shapes:
            temp = []
            for ps in shape.points:
                temp.append(service.CoordinateTransferService.wgs84towebmercator(ps[0], ps[1]))
            road.append(LineString(temp))
        # 键值对初始化
        for h in range(len(road)):
            hotrate[h] = 0
        vehicleidlist = self.taxidao.get_records('DISTINCT VehicleID', "nanjingtaxi", "LIMIT 0, 100")
        num = len(vehicleidlist)
        # 完成的数量
        c = 0
        # 循环车辆列表
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        records = []
        for vehicleid in vehicleidlist:
            print u"当前计算车辆 "+str(vehicleid[0])
            c += 1
            print u"---------------------------------"
            gpslist = self.taxidao.get_records('*','nanjingtaxi',"WHERE VehicleID='%s' AND PassengerState=1"%vehicleid)
            j = 0
            for record in gpslist:
                j += 1
                print str(c) + u'/' + str(num) + u"-----" + str(j) + u'/' + str(len(gpslist))
                rid = record[0] # id
                # lon = record[3] # 经度
                # lat = record[4] # 纬度
                xy = service.CoordinateTransferService.wgs84towebmercator(record[3], record[4])
                cp = Point(xy[0], xy[1])
                buffercir = self.buffercircle(cp, radius)
                # 相交的道路集合
                insroad = []
                for i in range(len(road)):
                    # TODO 相交查询的速度太慢，或可对道路网建空间索引
                    if buffercir.intersects(road[i]):
                        insroad.append(i)
                # 最短的距离
                mindis = 99999999
                # 所匹配的道路的id
                minroad = -1
                # 查找最近的道路
                if len(insroad) != 0:
                    for r in insroad:
                        t = cp.distance(road[r])
                        if t < mindis:
                            mindis = t
                            minroad = r
                    xy = self.calxy(cp, road[minroad])
                    hotrate[minroad] += 1
                    lnglat = service.CoordinateTransferService.webmercatortowgs84(xy[0], xy[1])
                    # self.taxidao.calMatchlonlat(rid, lnglat[0], lnglat[1])
                    records.append([rid, lnglat[0], lnglat[1]])
                else:
                    records.append([rid, record[3], record[4]])
                    pass
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "cal complete"
        # 保存计算后的数据
        self.taxidao.calMatchlonlats(records)
        fp = open("hotrate.txt", 'w')
        fp.write("id"+"\t"+"value"+"\n")
        for k, v in hotrate.iteritems():
            fp.write(str(k)+"\t"+str(v)+"\n")
        fp.close()

    def buffercircle(self, p, r):
        '''
        圆弧弥合法构建缓冲圆，在此调用object.buffer方法，也可再写
        point（0，0）.buffer(50.0)返回的polygon有66个点
        :param p: shapely中的点，即中心点
        :param r: 半径
        :return: 返回shapely中的polygon
        '''
        return p.buffer(r)

    def calxy(self, p, road):
        '''
        垂直投影计算方法
        :param p: 待计算点
        :param road: 投影道路
        :return:
        '''
        minp1 = 0
        tempd = 99999999
        for i in range(len(road.coords)-1):
            tempdis = Point(road.coords[i]).distance(p)+Point(road.coords[i+1]).distance(p)
            if tempdis < tempd:
                tempd = tempdis
                minp1 = i
        a = Point(road.coords[minp1])
        b = Point(road.coords[minp1+1])
        # 斜率
        kx = a.x-b.x
        ky = a.y-b.y
        if kx == 0:
            k = 999999999
        elif ky == 0:
            k = 0
        else:
            k = (a.y-b.y)/kx
        # 偏移量
        offset = (k*(p.y-a.y)+p.x-a.x)/(k*k+1)
        x = offset + a.x
        y = k * offset + a.y
        return [x, y]


if __name__ == '__main__':
    mapmatching = Matching()
    mapmatching.main(radius=50.0)
