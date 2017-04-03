# -*- coding:utf-8 -*-
import service.CoordinateTransferService

m = [[118.750, 32.100],
     [118.744,32.094],
     [118.749,32.091]]
for i in m:
    print i
    xy = service.CoordinateTransferService.wgs84towebmercator(i[0], i[1])
    print xy

ll = [[13219239.180,3776423.457],
      [13218481.540,3775603.625],
      [13219114.280,3775227.302]]
for l in ll:
    print l
    lnglat = service.CoordinateTransferService.webmercatortowgs84(l[0], l[1])
    print lnglat
