from src.util.Geography import calculate_coor_list, coordinate_to_point, point_to_coordinate, get_distance_from_coordinate
from src.util.Geography import get_coefficient, get_nearest_point_from_graph, get_coefficient_two_dimension, get_nearest_point_from_graph_two_dimension
import csv

'''
거리 1.15
3 
37.612272 126.793791	김포대교
37.539566 126.910025	여의도쪽 두껍게 시작
37.510429 126.980797	원효대교 아래쪽
37.510429 126.980797	동작대교(가장 아래지점) 1 / 50 x^
37.514969 126.996249	반포대교
37.538069 127.025324	동호대교 위쪽
37.529966 127.057134	영동대교
37.526416 127.064192	청담대교	
37.522280 127.084732	한강시민공원쪽 1 / 15 x^
37.542765 127.112343	천호대교 - 1 / 5 x^
37.569235 127.131811	구리암사대교 
37.582823 127.178053	끝
'''

# 따릉이의 좌표(lat, lon)으로부터 한강까지 km 거리 반환
def get_distance_from_han_river(tuple):
    lat, lon = coordinate_to_point(tuple)
    print(lat, lon)

    if lat < calculate_coor_list[0][0]:    # 김포대교 ~ 여의도쪽 두껍게 시작
        point = get_coefficient(calculate_coor_list[0], calculate_coor_list[1])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[1][0]:  # 여의도쪽 두껍게 시작 ~ 원효대교 아래쪽
        point = get_coefficient(calculate_coor_list[1], calculate_coor_list[2])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[2][0]:  # 원효대교 아래쪽 ~ 동작대교(가장 아래지점)
        point = get_coefficient(calculate_coor_list[2], calculate_coor_list[3])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[3][0]:  # 동작대교(가장 아래지점) ~ 반포대교  (near 1 / 50 x^)
        point = get_coefficient(calculate_coor_list[3], calculate_coor_list[4])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[4][0]:  # 반포대교 ~ 동호대교 위쪽
        point = get_coefficient(calculate_coor_list[4], calculate_coor_list[5])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[5][0]:  # 동호대교 위쪽 ~ 영동대교
        point = get_coefficient(calculate_coor_list[5], calculate_coor_list[6])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[6][0]:  # 영동대교 ~ 청담대교
        point = get_coefficient(calculate_coor_list[6], calculate_coor_list[7])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[7][0]:  # 청담대교 ~ 한강시민공원쪽
        point = get_coefficient(calculate_coor_list[7], calculate_coor_list[8])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[8][0]:  # 한강시민공원쪽 ~ 천호대교    (near 1 / 15 x^)
        point = get_coefficient(calculate_coor_list[8], calculate_coor_list[9])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    elif lat < calculate_coor_list[9][0]:  # 천호대교 ~ 구리암사대교 (near -1 / 5 x^)get_coefficient_two_dimension
        point = get_coefficient(calculate_coor_list[9], calculate_coor_list[10])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)
    else:   # 구리암사대교 ~ 끝
        point = get_coefficient(calculate_coor_list[10], calculate_coor_list[11])
        nearest_point = get_nearest_point_from_graph(point[0], point[1], lat, lon)

    print(point)
    return get_distance_from_coordinate(tuple, point_to_coordinate(nearest_point[0], nearest_point[1]))

# result = get_distance_from_han_river((37.534429, 126.904624))
# result = get_distance_from_han_river((37.510626, 126.958361))
# result = get_nearest_point_from_graph_two_dimension(1,3, 0,0)
# print(result)


f = open('data/bike_info.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
nf = open('data/re_bike_info.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(nf)
wr.writerow(["대여소 번호", "거치대", "위도", "경도", "한강 거리"])

is_first = True
for line in rdr:
    if is_first:
        is_first = False
        continue
    wr.writerow([line[1], line[4], line[5], line[6], get_distance_from_han_river((float(line[5]), float(line[6])))])

f.close()
nf.close()
