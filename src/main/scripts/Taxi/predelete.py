# -*- coding:utf-8 -*-
# 删除经纬度为零的数据
# 首先运行

from dao.taxi.TaxiDao import TaxiDao


class TaxiDeleter(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    def overalltaxi(self):
        ridls = self.taxidao.get_records('ID', 'nanjingtaxi', 'WHERE Latitude=0 or Longitude=0')
        self.taxidao.deleteid(ridls)


if __name__ == "__main__":
    taxideleter = TaxiDeleter()
    taxideleter.overalltaxi()
