# -*- coding:utf-8 -*-
# 层次聚类模型
# 输入 样本集合 总数 28979*2=57958  ，聚类距离度量函数Dmin, 聚类簇的数量下限 K
#
import math
import json
from dao.taxi.TaxiDao import TaxiDao


class Clustering(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')
        self.datafile = open(name="E:/MyProject/PycharmProjects/taxi_trajectory_app/src/main/scripts/Clustering/c.json", mode='w')

    def main(self,K):
        # 簇集c
        c = []
        # 样本集d
        d = self.taxidao.get_records('SLon,SLat,ELon,ELat', 'record', "WHERE STime > '2010-09-12 14:00:00' AND STime < '2010-09-12 15:00:00'")
        for a in d:
            c.append([[a[0], a[1]]])
            c.append([[a[2], a[3]]])
        l = len(c)
        # 簇集之间的距离矩阵m
        m = [[0 for col in range(l)] for row in range(l)]
        # m = []

        for i in range(l):
            for j in range(l):
                m[i][j] = self.distance(c[i], c[j])
                m[j][i] = m[i][j]
        q = l
        # TODO 聚类算法在数据量庞大时，效率极慢
        while q > K:
            print q
            # 找出距离最近的两个聚类簇ci* 和cj*
            tempi = 0
            tempj = 0
            closedistance = 999999
            for i in range(len(m)):
                for j in range(len(m[i])):
                    if m[i][j] != 0:
                        if m[i][j] < closedistance:
                            closedistance = m[i][j]
                            tempi = i
                            tempj = j
            # 合并ci* 和cj*
            for t in c[tempj]:
                c[tempi].append(t)
            # 将tempj后面的簇向前一位
            for j in range(tempj+1, q):
                c[j-1] = c[j]
            # 删除矩阵m的第tempj行和第tempj列
            del m[tempj]
            for i in m:
                del i[tempj]
            # 更新距离矩阵m
            for j in range(q-1):
                m[tempi][j] = self.distance(c[tempi],c[j])
                m[j][tempi] = m[tempi][j]
            q = q - 1
        # for i in c:
        #     if len(i) < 100:
        #         del c[i]
        self.datafile.write(json.dumps(c))

    '''
    距离函数
    取两个簇集合中最近的两个点的欧式距离 为返回值
    ci与cj都是list包含多个[Lon,Lat]
    '''
    def distance(self, ci, cj):
        d = 999999
        for i in ci:
            for j in cj:
                # 计算i和j之间的距离
                temp = math.sqrt(((i[0]-j[0]) * (i[0]-j[0])) + ((i[1]-j[1]) * (i[1]-j[1])))
                if temp < d:
                    d = temp
        return d


if __name__ == '__main__':
    clutering = Clustering()
    clutering.main(K=300)
