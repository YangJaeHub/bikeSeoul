from src.util.Geography import get_distance_from_coordinate
import csv
import math


def get_park_info():
    f = open('data/park_info.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f, delimiter='\t')
    # 3 면적 17 x좌표 18 y좌표
    list = []
    is_first = True
    for line in rdr:
        if is_first:
            is_first = False
            continue
        list.append((float(line[3]), float(line[18]), float(line[17])))
    return list


def get_min_distance(list, coor):
    min_distance = 99999999
    area = 0
    for line in list:
        distance = get_distance_from_coordinate((line[2], line[1]), coor)
        radius = math.sqrt(line[0] / math.pi) / 1000
        calc_distance = distance - radius
        if min_distance > calc_distance:
            min_distance = calc_distance
            area = line[0]
    return min_distance, area


list = get_park_info()

f = open('data/bike_river.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
nf = open('data/bike_river_park.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(nf)

is_first = True
for line in rdr:
    if is_first:
        line.append("가까운 공원 거리")
        line.append("공원 넓이 m^")
        wr.writerow(line)
        is_first = False
        continue
    min_distance = get_min_distance(list, (float(line[7]), float(line[6])))
    line.append(min_distance[0])
    line.append(min_distance[1])
    wr.writerow(line)

f.close()
nf.close()