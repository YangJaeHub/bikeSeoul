# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:48:57 2018

@author: LG
"""

import csv
from haversine import haversine
import numpy as np



####### Read the station locations and its elevations #########
def read_csv1(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=' ')
        next(reader)
        lon1 = []
        lat1 = []
        elv1 = []
        for row in reader:
            lon1.append(float(row[0]))
            lat1.append(float(row[1]))
            elv1.append(float(row[2]))
    return lon1, lat1, elv1



def read_csv2(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter= ' ')
        next(reader)
        lon2 = []
        lat2 = []
        elv2 = []
        for row in reader:
            lon2.append(float(row[0]))
            lat2.append(float(row[1]))
            elv2.append(float(row[2]))
    return lon2, lat2, elv2



def concat_lonlat(lon1, lat1, elv1, lon2, lat2, elv2):
    lon = lon1 + lon2 
    lat = lat1 + lat2 
    elv = elv1 + elv2 

    tlon = []
    tlat = []
    telv = []
    i = 1
    while i < len(lon):
        i += 1
        if i < len(lon):
            tlon.append(lon[i])
            tlat.append(lat[i])
            telv.append(elv[i])
    return tlon, tlat, telv


######## Bike locations #########
def read_bike(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        bnum = []
        blat = []
        blon = []
        brack = []
        for row in reader:
            bnum.append(int(row[2]))
            brack.append(int(row[5]))
            blat.append(float(row[6]))
            blon.append(float(row[7]))
    return bnum, brack, blat, blon



def deviation_elv(tlon, tlat, telv, bnum, brack, blon, blat):
#    dist = []
    elvd = []
    bnumd = []
    brackd = []
    blatd = []
    blond = []
    for ibnum, ibrack, iblon, iblat in zip(bnum, brack, blon, blat): #자전거 보관서 위치
        elv_cal = []
        for ilon, ilat, ielv in zip(tlon, tlat, telv): # 고도정보 
            pointb = (iblat, iblon)
            point2 = (ilat, ilon)
            dist_i = haversine(pointb, point2)
            if dist_i < 1.0: # 자전거 위치와 고도 정보가 1킬로 이내
                elv_cal.append(ielv)
        bnumd.append(ibnum)
        brackd.append(ibrack)
        blatd.append(iblat)
        blond.append(iblon)
        elvd.append(np.array(elv_cal).std())
    return bnumd, brackd, blatd, blond, elvd



def make_csv(bnumd, brackd, blatd, blond, elvd):
    ouput_list = []
    for bnumdi, brackdi, blatdi, blondi, elvdi in zip(bnumd, brackd, blatd, blond, elvd):
        ouput_list.append([float(bnumdi), float(brackdi), float(blatdi), float(blondi), float(elvdi)])
    with open('bike_elv_trial.csv', "w") as ouput:
        writer = csv.writer(ouput, quoting=csv.QUOTE_ALL, lineterminator = '\n')
        writer.writerow(['대여소 번호', '거치대', '위도', '경도', '고도 표준편차(1km)'])
        writer.writerows(ouput_list)
        
    


if __name__ == '__main__':
    lon1, lat1, elv1 = read_csv1('../../ASTGTM2_N37E126/ASTGTM2_N37E126_dem.xyz')
    lon2, lat2, elv2 = read_csv2('../../ASTGTM2_N37E127/ASTGTM2_N37E127_dem.xyz')

    bnum, brack, blat, blon = read_bike('../../따릉이대여소목록.csv')
    tlon, tlat, telv = concat_lonlat(lon1, lat1, elv1, lon2, lat2, elv2)
    bnumd, brackd, blatd, blond, elvd = deviation_elv(tlon, tlat, telv, bnum, brack, blon, blat)
    make_csv(bnumd, brackd, blatd, blond, elvd)

        

