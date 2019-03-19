#!/usr/bin/env python
# coding: utf-8

# In[1]:



#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""예제 : 탐색 method를 사용한다. """

import qi
import argparse
import sys
import numpy
import Image
from matplotlib import pyplot as plt

def main(session):
    """
    이것은 탐색 method를 사용하는 예제이다.
    """
    # ALNavigation, ALMotion를 프록시로 할당한다.
    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")

    # 로봇 깨우기 구동.
    motion_service.wakeUp()

    # 반경 2m 내의 주변 환경 탐색
    radius = 0.3
    error_code = navigation_service.explore(radius)
    if error_code != 0:
        print "Exploration failed."
        return
    # 탐색을 디스크에 저장.
    path = navigation_service.saveExploration()
    print "Exploration saved at path: \"" + path + "\""
    # 위치 추정을 사용해 지도에서 길찾기.
    navigation_service.startLocalization()
    # 초기 위치로 돌아온다.
    navigation_service.navigateToInMap([0., 0., 0.])
    # 위치 추정 중지.
    navigation_service.stopLocalization()
    # 로봇이 만든 지도 검색 및 표시
    result_map = navigation_service.getMetricalMap()
    map_width = result_map[1]
    map_height = result_map[2]
    img = numpy.array(result_map[4]).reshape(map_width, map_height)
    img = (100 - img) * 2.55 # from 0..100 to 255..0
    plt.imshow(img)
    plt.show()
    #numpy.save('img', img)
    #Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()

# 로봇 연결 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.160.0.38",
                        help="Robot IP address. On robot or Local Naoqi: use '192.160.0.38'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)


# In[ ]:




