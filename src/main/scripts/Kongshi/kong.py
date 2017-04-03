# -*- coding:utf-8 -*-

from dao.taxi.TaxiDao import TaxiDao


class KongShi(object):
    def __init__(self):
        self.taxidao = TaxiDao(host='localhost', db='taxi', user='root', password='1234')

    def kongshirun(self):
        pass

if __name__ == '__main__':
    ks = KongShi()
    ks.kongshirun()
