## ALNavigation API 

### Method list

이 모듈은 ALModule API로부터 Method를 상속받는다. 이 모듈은 다음과 같은 구체적인 Method들을 포함한다.

#### class ALNavigationProxy

#### Navigation API:
- ALNavigationProxy::navigateTo
- ALNavigationProxy::moveAlong
- ALNavigationProxy::getFreeZone
- ALNavigationProxy::findFreeZone

#### Exploration and localization API:
- ALNavigationProxy::explore
- ALNavigationProxy::stopExploration
- ALNavigationProxy::saveExploration
- ALNavigationProxy::getMetricalMap
- ALNavigationProxy::navigateToInMap
- ALNavigationProxy::getRobotPositionInMap
- ALNavigationProxy::loadExploration
- ALNavigationProxy::relocalizeInMap
- ALNavigationProxy::startLocalization
- ALNavigationProxy::stopLocalization

#### Deprecated methods:
- ALNavigationProxy::startFreeZoneUpdate
- ALNavigationProxy::stopAndComputeFreeZone


#### Event list
- Navigation/AvoidanceNavigator/Status()
- Navigation/AvoidanceNavigator/ObstacleDetected()
- Navigation/AvoidanceNavigator/MovingToFreeZone()
- Navigation/AvoidanceNavigator/TrajectoryProgress()
- Navigation/AvoidanceNavigator/AbsTargetModified()
- Navigation/MotionDetected()


---
### Methods

#### bool ALNavigationProxy::navigateTo(const float& x, const float& y)

FRAME_ROBOT에 표시된 상대적인 측량으로 2D 상에서 로봇을 이동하게 만든다. 로봇은 환경과 충돌하지 않도록 안전한 움직임을 취할 것이다. 얘를 들어, 머리로 보고, 멈춘 뒤 경로를 다시 설게한다. 따라서 머리의 리소스를 사용하는 동작은 네비게이션과 같은 타임라인에서 실행할 수 없다.

ALMotionProxy::moveTo와 달리 로봇은 이동하면서 자신의 경로와 속도를 선택한다. 속도는 로봇이 장애물에 가까이 접근할 경우 감소한다. 장애물 회피가 위험해지면(security 영역에서 장애물이 감지되자마자) ALMotionProxy::moveTo와 같이 로봇이 정지한다.

대상(목표 지점)은 로봇으로 부터 3m 이상 떨어져 있어야 하며, 그렇지 않으면 명령이 무시되고 경고가 발생한다.

이것은 blocking call이다.

#### Parameters:	
- x – X축으로 떨어져 있는 거리(meter)
- y – Y축으로 떨어져 있는 거리(meter)
#### Returns:	
로봇이 마지막 목표에 도달한 경우, 장애물에 의해 정지한 경우 또는 목표에 대해 경로를 찾을 수 없는 경우라면 True를 반환한다. 

~~~ python
navigationProxy.navigateTo(2.0, 0.0)
~~~
---
#### bool ALNavigationProxy::moveAlong(const AL::ALValue& trajectory)

#### Parameters:	
- trajectory –
direct trajectory [“Holonomic”, pathXY, finalTheta, finalTime] 또는 composed trajectory [“Composed”, direct trajectories]을 기술하는 ALValue.

    pathXY는 2D path를 기술하는 ALValue이고, direct path 또는 composed 중 하나이다: [“Composed”, direct paths]

    Direct path는: [“Line”, [finalX, finalY]], [“Circle”, [centerX, centerY], spanAngle]로 구성된 선 또는 원(호)일 수 있다.

#### Returns: 
로봇이 trajectory 완전히 수행했을 경우, 그리고 장애물에 의해 정지했을 경우에 True를 반환한다.

다음 커맨드는 5초안에 1미터 앞으로, 10초 안에 1미터 뒤로 정지 없이 이동한다.

~~~ python
navigationProxy.moveAlong(["Composed", ["Holonomic", ["Line", [1.0, 0.0]], 0.0, 5.0], ["Holonomic", ["Line", [-1.0, 0.0]], 0.0, 10.0]])
~~~
---
#### AL::ALValue ALNavigationProxy::getFreeZone(float desiredRadius, float displacementConstraint)

로봇의 주변 free zone을 출력한다. 로봇이 움직이지 않는다. free space 또는 free zone은 로봇이 이동가능한 공간을 의미한다.

#### Parameters:
- desiredRadius – 우리가 원하는 free space 반경(meter)
- displacementConstraint – 발견된 장소에 도달하기 위해 우리가 이동하는 최대 거리(meter)다.
- Returns: ALValue [Free Zone Error Code, result radius (meters), [worldMotionToRobotCenterX (meters), worldMotionToRobotCenterY (meters)]] 
---
#### qi::Future<AL::ALValue> ALNavigationProxy::findFreeZone(float desiredRadius, float displacementConstraint)

지정한 이동보다 크지 않는, 지정된 반경의 free circular zone를 찾는다. 이를 위해 로봇은 스스로 움직이고 주위를 둘러본다. 
(blocking call)

#### Parameters:	
- desiredRadius – 우리가 원하는 free space의 반경(meter)
- displacementConstraint – 발견된 장소에 도달하기 위해 우리가 이동하는 최대 거리(meter)다.

#### Returns:	
cancelable qi::Future<ALValue> [Free Zone Error Code, result radius (meters), [worldMotionToRobotCenterX (meters), worldMotionToRobotCenterY (meters)]]

~~~ python
desiredRadius = 0.6
displacementConstraint = 0.5
navigationProxy.findFreeZone(desiredRadius, displacementConstraint)
~~~
#### AL::ALValue ALNavigationProxy::startFreeZoneUpdate() (2.5 verson 이후로 사용 X)
***
### Python script을 위한 파이썬 스크립트

다음 코드가 정상적으로 동작한다면 로봇은 free zone의 중심으로 이동한다.

alnavigation.py

~~~ python

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""예제 : findFreeZone Method"""

import qi
import argparse
import sys
import almath
import math


def main(session):

    # ALNavigation, ALMotion, ALRobotPosture를 프록시로 할당한다.

    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # 로봇 깨우기 구동.
    motion_service.wakeUp()

    # 로봇 자세 초기화.
    posture_service.goToPosture("StandInit", 0.5)

    # 환경 탐색
    # navigation_service.startFreeZoneUpdate()
    navigation_service.getFreeZone()
    ###########################################################################
    # 이곳에 timeline과 이동하는 animation을 추가한다. #
    # For example : 360도 회전
    motion_service.moveTo(0.0, 0.0, 2.0 * math.pi) 
    ###########################################################################
    desiredRadius = 0.6
    displacementConstraint = 0.5
    result = navigation_service.findFreeZone(desiredRadius, displacementConstraint)

    errorCode = result[0]
    if errorCode != 1:
        # 코드가 정상 동작시 Freezone의 중앙으로 이동.
        worldToCenterFreeZone = almath.Pose2D(result[2][0], result[2][1], 0.0)
        worldToRobot = almath.Pose2D(motion_service.getRobotPosition(True))
        robotToFreeZoneCenter = almath.pinv(worldToRobot) * worldToCenterFreeZone
        motion_service.moveTo(robotToFreeZoneCenter.x, robotToFreeZoneCenter.y, 0.0)
    else :
        print "Problem during the update of the free zone."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
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
~~~

### Events
---
#### Event: "Navigation/AvoidanceNavigator/Status"
#### callback(std::string eventName, AL::ALValue status, std::string subscriberIdentifier)

local navigator 상태가 변화할 때 발생한다.

#### Parameters:	
- eventName (std::string) – “Navigation/AvoidanceNavigator/Status”
- status – 새로운 local navigator의 상태이다. ALNavigation에서 자세한 내용을 참고해라.
- subscriberIdentifier (std::string) –

***
#### Event: "Navigation/AvoidanceNavigator/ObstacleDetected"
#### callback(std::string eventName, AL::ALValue position, std::string subscriberIdentifier)

닫힌 지역에서 장애물이 감지됐을 때 발생한다.

#### Parameters:	
- eventName (std::string) – “Navigation/AvoidanceNavigator/ObstacleDetected”
- position – Array 형태의 [x, y], FRAME_ROBOT에서 검출된 장애물의 위치를 나타낸다.
subscriberIdentifier (std::string) –
***
#### Event: "Navigation/AvoidanceNavigator/MovingToFreeZone"
#### callback(std::string eventName, AL::ALValue status, std::string subscriberIdentifier)

로봇이 근처에 장애물을 두고 움직임을 시작하거나 멈출 때 발생한다.

#### Parameters:	
- eventName (std::string) – “Navigation/AvoidanceNavigator/MovingToFreeZone”
- status – 로봇이 움직이기 시작하면 1.0, 멈추면 0.0을 반환한다.
subscriberIdentifier (std::string) –

---


#### Event: "Navigation/AvoidanceNavigator/TrajectoryProgress"
#### callback(std::string eventName, AL::ALValue progress, std::string subscriberIdentifier)
trajectory progress가 업데이트 되면 발생한다.

#### Parameters:	
- eventName (std::string) – “Navigation/AvoidanceNavigator/TrajectoryProgress”
- progress – trajectory를 달성한 비율에 따라서 0.0에서 1.0 사이로 변화한다.
- subscriberIdentifier (std::string) –
---

#### Event: "Navigation/MotionDetected"
- callback(std::string eventName, AL::ALValue sensorData, std::string subscriberIdentifier)

로봇 금처에 움직이는 무언가가 센서에 감지됬을 때 발생한다.

현재 수행은 오로지 페퍼의 Infra-Red(레이저 센서)에 기반을 둔다.

#### Parameters:	
- eventName (std::string) – “Navigation/MotionDetected”
- sensorData – [Sensor, Position, Detected]로 구성된 array, Sensor는 움직임을 감지한 센서의 이름, Position은 FRAME_WORLD에서 탐지된 페퍼의 주변 이동 물체의 3D 위치, Detected는 움직이는 물체가 페퍼와 멀어진다면 False, 가까워 진다면 True이다.(boolean equals)
- subscriberIdentifier (std::string) –

--- 

### Free Zone Error Code

1. 좋다. 너는 결과의 좌표와 반경을 믿을 수 있다. 
2. 좋지 않다. 문제가 있었다. 반환된 좌표와 반경을 믿지 마라.
3. 일부 좋지 않다. 문제는 없었지만, 제약 조건은 만족하지 않았지만 최선의 해결책으로 선택했다. 