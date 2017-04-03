# -*- coding:utf-8 -*-
# 地图匹配算法
# 路网所在路径 roadpath
# 轨迹点在数据库中 db=taxi table=nanjingtaxi
from dao.taxi.TaxiDao import TaxiDao
from shapely.geometry import LineString
from shapely.geometry import Point
import service.CoordinateTransferService
import shapefile
roadpath = 'E:/MyData/road/nanjing.shp'


class Matching(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    def main(self, radius):
        sf = shapefile.Reader(roadpath)
        shapes = sf.shapes()
        road = []
        print "read road data..."
        for shape in shapes:
            temp = []
            for ps in shape.points:
                temp.append(service.CoordinateTransferService.wgs84towebmercator(ps[0], ps[1]))
            road.append(LineString(temp))
        vehicleidlist = self.taxidao.get_records('DISTINCT VehicleID', "nanjingtaxi", "where VehicleID='806814011053'")
        num = len(vehicleidlist)
        # 完成的数量
        c = 0
        # 循环车辆列表
        for vehicleid in vehicleidlist:
            print u"当前计算车辆 "+str(vehicleid[0])
            c += 1
            print u"---------------------------------"
            gpslist = self.taxidao.get_records('*', 'nanjingtaxi', "WHERE VehicleID='%s' ORDER BY Time" % vehicleid)
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
                minroad = 0
                for r in insroad:
                    t = cp.distance(road[r])
                    if t < mindis:
                        mindis = t
                        minroad = r
                xy = self.calxy(cp, road[minroad])
                lnglat = service.CoordinateTransferService.webmercatortowgs84(xy[0], xy[1])
                self.taxidao.calMatchlonlat(rid, lnglat[0], lnglat[1])

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
        k = (a.y-b.y)/(a.x-b.x)
        # 偏移量
        offset = (k*(p.y-a.y)+p.x-a.x)/(k*k+1)
        x = offset + a.x
        y = k * offset + a.y
        return [x, y]


if __name__ == '__main__':
    mapmatching = Matching()
    mapmatching.main(radius=50.0)
