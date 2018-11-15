import math
import sympy

map_width = 40000
map_height = 20000

coor_list = [(37.612272, 126.793791), (37.539566, 126.910025), (37.525175, 126.944681), (37.510429, 126.980797), (37.514969, 126.996249),
             (37.538069, 127.025324), (37.529966, 127.057134), (37.526416, 127.064192), (37.522280, 127.084732), (37.542765, 127.112343),
             (37.569235, 127.131811), (37.582823, 127.178053)]


def coordinate_to_point(tuple):
    lat = tuple[0]
    lon = tuple[1]

    x = (lon + 180) * (map_width / 360)
    # convert from degrees to radians
    lat_rad = lat * math.pi / 180

    # get y value
    merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    y = (map_height / 2) - (map_width * merc_n / (2 * math.pi))

    return (x -17000) * 1000, (y - 7700) * 1000


calculate_coor_list = []
for tu in coor_list:
    calculate_coor_list.append(coordinate_to_point(tu))


def get_distance_from_coordinate(coor1, coor2):
    print(coor1, coor2)
    lat1 = math.radians(coor1[0])
    lat2 = math.radians(coor2[0])
    lon1 = math.radians(coor1[1])
    lon2 = math.radians(coor2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6373.0  # 지구 km 반경
    km = R * c
    print(km)
    return km


def point_to_coordinate(x, y):
    lon = ((x / 1000 + 17000) / (map_width/360)) - 180
    lat = (math.atan(math.exp((((map_height/2) - (y / 1000 + 7700)) * (2*math.pi)) / map_width)) - (math.pi/4)) * 2 * 180 / math.pi

    return round(lat, 6), round(lon, 6)


# 두 지점 포인트 사이의 1차원 function 계수구하기. y = av * x + cv
def get_coefficient(tuple1, tuple2):
    lat1, lon1 = tuple1
    lat2, lon2 = tuple2
    x, y, c = sympy.symbols("x y c")
    av = (lon2 - lon1) / (lat2 - lat1)
    f = av * x - y + c
    f_result = f.subs({x: lat1, y: lon1})
    cv = sympy.solve(f_result, c)
    return av, cv[0]


def get_coefficient_two_dimension(tuple1, tuple2):
    lat1, lon1 = tuple1
    lat2, lon2 = tuple2
    a, x, y, c = sympy.symbols("a x y c")
    f = a * x * x - y + c
    f_result1 = f.subs({x: lat1, y: lon1})
    f_result2 = f.subs({x: lat2, y: lon2})
    result = sympy.solve([f_result1, f_result2], [a, c])

    return result[a], result[c]


def get_nearest_point_from_graph(av, cv, lat, lon):
    a, x, y, c = sympy.symbols("a x y c")
    f1 = a * x - y + c
    f1 = f1.subs({a: av, c: cv})
    reverse_a = -1 / av  # 위 함수와 직각으로 교차하는 기울기
    f2 = reverse_a * x - y + c  # 직각으로 교차하는 함수 f2
    f2_result = f2.subs({x: lat, y: lon})  # point값 대입해서
    cv2 = sympy.solve(f2_result, c)  # c 값 구하고
    f2 = f2.subs({c: cv2[0]})  # c 대입해서 f2 완성

    # 완성된 두 식 f1, f2의 교차점은 따릉이 대여소에서 한강까지의 최 단거리(직선) 지점
    result = sympy.solve([f1, f2], [x, y])
    return result[x], result[y]

# y=  av x^ + cv
def get_nearest_point_from_graph_two_dimension(av, cv, lat, lon):
    a, x, y, c = sympy.symbols("a x y c")
    '''
    (x, av * x^ + cv)와 (lat, lon) 두 점간의 최단 거리
    공식 : sqrt((x2 - x1)^ + (y2 - y1)^)
    '''
    distance_fuc = sympy.sqrt((lat - x)**2 + (lon - (av * x * x + cv))**2)   # 최단거리 함수
    yv = sympy.diff(distance_fuc, x)    # 함수 미분하면 최단거리 y 값이 나온다.v
    f = a * x * x - y + c
    f = f.subs({a: av, c: cv, y: yv})
    xv = sympy.solve(f, x)  # xv를 구하지 못해서 deprecated
    return xv, yv

'''
xy 좌표로 변환하기 전 방법.
def convert_coor_origin(coor):
    return convert_lat_origin(coor[0]), convert_lon_origin(coor[1])


def convert_lat_scala(lat):
    return (lat - 37) * 1000000


def conver_lon_scala(lon):
    return (lon - 126) * 1000000


def convert_lat_origin(lat):
    return round(lat / 1000000, 6) + 37


def convert_lon_origin(lon):
    return round(lon / 1000000, 6) + 126
'''
