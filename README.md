# Python SDK - Overview

## Python SDK는 무엇인가.

Aldebaran 로봇을 위한 Python SDK는 다음 기능을 수행한다.

원격 머신의 C++ API를 모두 사용하게 하거나
원격 또는 로봇에서 작동 가능한 Python 모듈을 생성한다.

Python을 사용하는 것은 Aldebaran 로봇을 프로그래밍하는 가장 빠른 방법 중 하나이다.


### 핵심 개념 마스터하기

먼저 핵심 개념을 읽어보십시오.

기본 접근법은 다음과 같다.

1. ALProxy 
2. 사용할 모듈에 ALProxy 생성 
3. method 호출

이는 다음 예에서 확인 할 수 있으며, 자세한 것은 튜토리얼에서 설명합니다.

~~~
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "<IP of your robot>", 9559)
tts.say("Hello, world!")
~~~

Python SDK의 일부는 Choregraphe 내부적으로 사용하거나 자동으로 생성되므로, 이곳에 문서화되지 않은 것은 사용하지말거나, API 변경을 기다리십시오.


### ALProxy 

이것은 Python의 메인 모듈이다.

ALProxy 객체를 통해 모듈에 대한 프록시(클라이언트와 서버 사이에 데이터를 전송하는)를 생성할 수 있다.

사용가능한 Broker instance가 있는지 여부에 따라 두 개의 다른 constructors를 지원한다. 

~~~
ALProxy(name, ip, port)
~~~
~~~
ALProxy(name)
~~~

- name 은 모듈의 이름이며,
- ip는 모듈이 동작하는 Broker의 IP이고,
- port는 Broker의 port이다.
  

주먹구구식으로, Choregraphe에 코드를 작성할때 ALProxy를 사용해야한다.



# 튜토리얼
## API 사용하기

### NAO 말하게 만들기

다음 코드를 실행해보시오 :

~~~
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "<IP of your robot>", 9559)
tts.say("Hello, world!")
~~~

### 프록시 사용하기 

ALProxy는 당신이 연결할 모듈에 적응하는 객체이다.
~~~
class ALProxy(name, ip, port)
~~~

- name - 모듈의 이름
- ip - 로봇의 IP
- port - 명령하는 NAOqi의 Port (Default : 9559)

모듈의 모든 Method는 다음과 같이 객체를 통해 직접 접근 가능하다.

~~~
almemory = ALProxy("ALMemory", "nao.local", 9559)
pings = almemory.ping()
~~~

## 병렬처리 - NAO를 움직이고 말하게 하기

### NAO를 얼리게 설정하기

관절의 강성을 0이 아닌 다른 값으로 설정하면, 로봇이 움직이지 않는다. (1~0)

이것을 실행해보시오. 간단하게  ALMotionProxy::setStiffnesses Method를 호출하면 된다.

~~~
from naoqi import ALProxy
motion = ALProxy("ALMotion", "nao.local", 9559)
motion.setStiffnesses("Body", 1.0)
~~~

API가 'ALValue'를 사용한다는 것을 알 수 있다.
데이터 타입의 변환은 자동이다.

### NAO를 움직이게 만들기

NAO를 걷게 하고 싶다면, 너는 ALMotionProxy::moveInit (로봇이 바른 자세를 설정하기 위해) 그리고 ALMotionProxy::moveTo를 사용해야한다.

~~~
from naoqi import ALProxy
motion = ALProxy("ALMotion", "nao.local", 9559)
motion.moveInit()
motion.moveTo(0.5, 0, 0)
~~~

### NAO를 움직이고 동시에 말하게 만들기

당신이 만든 모든 프록시는 'Post'라는 속성이 있는데, 백그라운드에 긴 메소드를 호출할 수 있다.

이것은 너가 로봇에게 몇 가지 일들을 동시에 시킬 수 있다.

~~~
from naoqi import ALProxy
motion = ALProxy("ALMotion", "nao.local", 9559)
tts    = ALProxy("ALTextToSpeech", "nao.local", 9559)
motion.moveInit()
motion.post.moveTo(0.5, 0, 0)
tts.say("I'm walking")
~~~

특정 작업이 완료될 때까지 대기할 필요가 있는 경우, Post 사용에서 반환하는 테스크 ID를 사용하여 ALProxy를 대기시킬 수 있다.
~~~
from naoqi import ALProxy
motion = ALProxy("ALMotion", "nao.local", 9559)
motion.moveInit()
id = motion.post.moveTo(0.5, 0, 0)
motion.wait(id, 0)
~~~


## Event에 반응하기.

우리는 로봇이 사람 얼굴을 감지했을 때마다 'Hello, you'라고 말하게 하고 싶다.

이것을 하기 위해서, 우리는 ALFacedetection모듈이 만드는 ‘FaceDetected’ Event를 요청받아 Callback에 링크해야 한다. Callback은 Event가 발생할 때마다 실행되는 기능이다.

예시는 아래에 있다 : 스크립트를 실랭하고 로봇앞에 얼굴을 내밀어라. 너는 'hello, you' 라는 말을 들을 수 있다.

reacting_to_events.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse


class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            self.tts.say("Hello, you!")
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                print "Face Extra Infos :" + str(faceExtraInfo)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()

~~~

참고 : 어떤 식으로든 요청한 변수를 메모리에 저장해야한다. 그렇지 않으면 요청한 변수는 사라지고 연결은 끊어진다. 여기서는 그것을 Class 변수로만 유지한다.


## 데이터 기록 : 머리 각도.

로봇의 다양한 센서 값을 기록하는 것은 쉽다.

간단한 예시는 다음과 같다:

data_recording.py
~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Record some sensors values and write them into a file."""

import qi
import argparse
import sys
import os
import time


# MEMORY_VALUE_NAMES is the list of ALMemory values names you want to save.
ALMEMORY_KEY_NAMES = ["Device/SubDeviceList/HeadYaw/Position/Sensor/Value",
                      "Device/SubDeviceList/HeadYaw/Position/Actuator/Value"]

def recordData(memory_service):
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    print "Recording data ..."
    data = list()
    for range_counter in range (1, 100):
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory_service.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(0.05)
    return data

def main(session):
    """ Parse command line arguments, run recordData
    and write the results into a csv file.
    """
    # Get the services ALMemory and ALMotion.

    memory_service = session.service("ALMemory")
    motion_service = session.service("ALMotion")

    # Set stiffness on for Head motors
    motion_service.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian  in two seconds
    motion_service.angleInterpolation(
        ["HeadYaw"],
        [1.0, 0.0],
        [1  , 2],
        False,
        _async=True
    )
    data = recordData(memory_service)
    # Gently set stiff off for Head motors
    motion_service.setStiffnesses("Head", 0.0)

    output = os.path.abspath("record.csv")

    with open(output, "w") as fp:
        for line in data:
            fp.write("; ".join(str(x) for x in line))
            fp.write("\n")

    print "Results written to", output


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


ALMemoryProxy:::getData를 50 ms마다 호출하고, 값을 매트릭스에 저장하고 작성하면 된다.

## 파이썬 코드 로봇에서 실행하기

Event에 반응하기를 Naoqi 시작할 때 자동으로 동작하게 할 수 있다. 

로봇에 스크립트를 업로드하고 (/home/nao/reacting_to_events.py) /home/nao/naoqi/preferences/autoload.ini 파일을 수정하여 다음을 수행할 수 있다.

참고 : pip 와 pport는 스크립트가 실행되는 동안 NAOqi에서 자동으로 실행한다. 

## 파이썬 SDK 예제
## core
### non-ASCII 텍스트 읽기
로봇이 프랑스어로 말하도록 설정하고 데이터 파일에서 몇 가지 문장을 말하게 한다고 가정하자.
인코딩 처리를 해야하기 때문에 조금 까다롭다.

### 예시 
먼저, 다음 파일을 다운로드하여 로봇내에 같은 디렉토리에 넣는다:

- coffee_en.txt
- coffee_fr_utf-8.txt
- coffee_fr_latin9.txt
- non_ascii.py

coffee_en.txt는 “I like coffee”이란 스트링 문자를 포함하고, coffee_fr_utf-8.txt와 coffee_fr_latin9.txt는 J’aime le café를 인코딩한 문자를 포함한다.

코드를 살펴보자

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Non ascii Characters"""

import qi
import argparse
import sys
import codecs


def say_from_file(tts_service, filename, encoding):
    with codecs.open(filename, encoding=encoding) as fp:
        contents = fp.read()
        # warning: print contents won't work
        to_say = contents.encode("utf-8")
    tts_service.say(to_say)


def main(session):
    """
    This example uses non ascii characters.
    """
    # Get the service ALTextToSpeech.

    tts_service = session.service("ALTextToSpeech")

    try :
        tts_service.setLanguage('French')
    except RuntimeError:
        print "No French pronunciation because French language is not installed. Pronunciation will be incorrect."
    say_from_file(tts_service, 'coffee_fr_utf-8.txt', 'utf-8')
    say_from_file(tts_service, 'coffee_fr_latin9.txt', 'latin9')

    tts_service.setLanguage('English')
    # the string "I like coffee" is encoded the exact same way in these three
    # encodings
    say_from_file(tts_service, 'coffee_en.txt', 'ascii')
    say_from_file(tts_service, 'coffee_en.txt', 'utf-8')
    say_from_file(tts_service, 'coffee_en.txt', 'latin9')


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

첫째, 우리가 코덱을 어떻게 사용하지 않는지 확인해라. 열어서 인코딩을 특정한다.

또한 파일에서 판독한 결과를 어떻게 디코딩 하는지 주의해라. fp.read에 의해 반환된 객체는 유니코드 객체인데, 우리는 그것을 다시 인코딩해서 ’UTF-8’로 인코딩된 str 객체를 TTS 프록시가 사용할 수 있도록 만들어야한다.

파이썬은 'ASCII'(로봇의 현재 로컬)을 사용하여 문자열을 디코딩하려고 시도하므로 Print를 실행하면 작동하지 않는다:

~~~
Traceback (most recent call last):
  File "non_ascii.py", line 22, in <module>
    main()
  File "non_ascii.py", line 18, in main
    say_from_file(filename)
  File "non_ascii", line 10, in say_from_file
    print contents
UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position
13: ordinal not in range(128)
~~~

마지막 파일의 인코딩에 관계없이 TTS 프록시로 전송되기 전에 ’UTF-8’로 인코딩된다.


### 예시 돌려보기

로봇의 SSH를 열어 다음을 실행한다.

~~~
$ python non_ascii.py
~~~

### 더 나아가기 

파일이 UTF-8로 인코딩됬는지 확인 되지 않으면 다음과 같은 방법으로 확인할 수 있다.
~~~
with codecs.open(filename, encoding="utf-8") as fp:
    try:
        contents = fp.read()
    except UnicodeDecodeError:
        print filename, "is not UTF-8 encoded"
        return
~~~
## Motion

## 자세

이 섹션은 NAO가 Pose lnit 및 Pose Zero 를 취하도록 만드는 방법을 보여준다.

### Pose Init

NAO를 초기 자세로 만든다. 

almotion_poseInit.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: PoseInit - Small example to make Nao go to an initial position."""

import qi
import argparse
import sys


def main(session):
    """
    PoseInit: Small example to make Nao go to an initial position.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    # Go to rest position
    motion_service.rest()


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

### Pose Zero

모든 NAO의 모터를 0으로 만든다.

almotion_poseZero.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: PoseZero: Set all the motors of the body to zero."""

import qi
import argparse
import sys


def main(session):
    """
    Use the goToPosture Method to PoseZero.
    Set all the motors of the body to zero.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Zero
    posture_service.goToPosture("StandZero", 0.5)

    # We use the "Body" name to signify the collection of all joints and actuators
    #pNames = "Body"

    # Get the Number of Joints
    #numBodies = len(motion_service.getBodyNames(pNames))

    # We prepare a collection of floats
    #pTargetAngles = [0.0] * numBodies

    # We set the fraction of max speed
    #pMaxSpeedFraction = 0.3

    # Ask motion to do this with a blocking call
    #motion_service.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    # Go to rest position
    motion_service.rest()


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

## 강성
강성을 켜거나 끌 수 있다.

### 강셩 켜기

almotion_stiffnessOn.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Stiffness On - Active Stiffness of All Joints and Actuators"""

import qi
import argparse
import sys
import time


def main(session):
    """
    Stiffness On - Active Stiffness of All Joints and Actuators.
    This example is only compatible with NAO.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")

    # We use the "Body" name to signify the collection of all joints
    names = "Body"
    stiffnessLists = 1.0
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    # print motion state
    print motion_service.getSummary()

    time.sleep(2.0)

    # Go to rest position
    motion_service.rest()


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

### 강성 끄기

경고 : 이것을 시도하기 전에 로봇이 서있지 않은지 확인하십시오.

almotion_stiffnessOff.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example : Stiffness Off - remove stiffness of all joints and actuators"""

import qi
import argparse
import sys


def main(session):
    """
    Stiffness Off - remove stiffness of all joints and actuators.
    This example is only compatible with NAO.
    """
    # Get the service ALMotion.

    motion_service = session.service("ALMotion")

    # We use the "Body" name to signify the collection of all joints
    names = "Body"
    stiffnessLists = 0.0
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    # print motion state
    print motion_service.getSummary()


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


## 움직이고 걷기

이 섹션에는 표준 보행과 맟춤 보행, 모두에 대한 몇가지 파이썬 예제가 담겨있다.

### 간단히 걷기

이 예제는 알데바란에서 만든 기준 보행을 어떻게 하는지 보여준다.

#### 걷기
NAO를 뒤 앞 그리고 회전하여 걷게 한다.

almotion_move.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Walk - Small example to make Nao walk"""

import qi
import argparse
import sys
import motion
import time
import almath


def userArmsCartesian(motion_service):
    effector   = ["LArm", "RArm"]
    frame      = motion.FRAME_TORSO
    useSensorValues = False

    # just control position
    axisMask   = [motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL]

    # LArm path
    pathLArm = []
    initTf   = almath.Transform(motion_service.getTransform("LArm", frame, useSensorValues))
    targetTf = almath.Transform(motion_service.getTransform("LArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 -= 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))

    # RArm path
    pathRArm = []
    initTf   = almath.Transform(motion_service.getTransform("RArm", frame, useSensorValues))
    targetTf = almath.Transform(motion_service.getTransform("RArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 += 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))

    pathList = []
    pathList.append(pathLArm)
    pathList.append(pathRArm)

    # Go to the target and back again
    timesList = [[1.0, 2.0, 3.0, 4.0],
                 [1.0, 2.0, 3.0, 4.0]] # seconds

    motion_service.transformInterpolations(effector, frame, pathList,
                                       axisMask, timesList)


def userArmArticular(motion_service):
    # Arms motion from user have always the priority than walk arms motion
    JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    Arm1 = [-40,  25, 0, -40]
    Arm1 = [ x * motion.TO_RAD for x in Arm1]

    Arm2 = [-40,  50, 0, -80]
    Arm2 = [ x * motion.TO_RAD for x in Arm2]

    pFractionMaxSpeed = 0.6

    motion_service.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    motion_service.angleInterpolationWithSpeed(JointNames, Arm2, pFractionMaxSpeed)
    motion_service.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)


def main(session):
    """
    Walk - Small example to make Nao walk
    This example is only compatible with NAO
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand
    posture_service.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Motion algorithm
    #####################
    motion_service.setMoveArmsEnabled(True, True)
    # motion_service.setMoveArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #TARGET VELOCITY
    X = -0.5  # backward
    Y = 0.0
    Theta = 0.0
    Frequency =0.0 # low speed
    try:
        motion_service.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    userArmsCartesian(motion_service)

    #TARGET VELOCITY
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # max speed
    try:
        motion_service.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    time.sleep(4.0)

    #TARGET VELOCITY
    X = 0.2
    Y = -0.5
    Theta = 0.2
    Frequency = 1.0

    try:
        motion_service.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    time.sleep(2.0)
    userArmArticular(motion_service)
    time.sleep(2.0)

    #####################
    ## End Walk
    #####################
    #TARGET VELOCITY
    X = 0.0
    Y = 0.0
    Theta = 0.0
    motion_service.moveToward(X, Y, Theta)

    motion_service.waitUntilMoveIsFinished()

    # Go to rest position
    motion_service.rest()


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

### 이동하기

NAO를 목표로 걷게한다.

almotion_moveTo.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Move To - Small example to make Nao Move To an Objective"""

import qi
import argparse
import sys
import math
import almath


def main(session):
    """
    Move To: Small example to make Nao Move To an Objective.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by move algorithm
    #####################
    motion_service.setMoveArmsEnabled(True, True)
    #~ motion_service.setMoveArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #####################
    ## get robot position before move
    #####################
    initRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))

    X = 0.3
    Y = 0.1
    Theta = math.pi/2.0
    motion_service.moveTo(X, Y, Theta, _async=True)
    # wait is useful because with _async moveTo is not blocking function
    motion_service.waitUntilMoveIsFinished()

    #####################
    ## get robot position after move
    #####################
    endRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    # return an angle between ]-PI, PI]
    robotMove.theta = almath.modulo2PI(robotMove.theta)
    print "Robot Move:", robotMove

    # Go to rest position
    motion_service.rest()


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

## Customized walk
## Footstep control

## 좌표 명령어

이 섹션에서는 NAO의 몸을 좌표 이동하는 예시를 보여준다.

### 팔
팔 궤적의 예시이다.

#### Trajectory 1
almotion_cartesianArm1.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Arm"""

import qi
import argparse
import sys
import motion
import almath


def main(session):
    """
    Use case of transformInterpolations API.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    effector   = "LArm"
    frame      = motion.FRAME_TORSO
    axisMask   = almath.AXIS_MASK_VEL # just control position
    useSensorValues = False

    path = []
    currentTf = motion_service.getTransform(effector, frame, useSensorValues)
    targetTf  = almath.Transform(currentTf)
    targetTf.r1_c4 += 0.03 # x
    targetTf.r2_c4 += 0.03 # y

    path.append(list(targetTf.toVector()))
    path.append(currentTf)

    # Go to the target and back again
    times      = [2.0, 4.0] # seconds

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_service.rest()


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

#### Trajectory 2
almotion_cartesianArm2.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Arm"""

import qi
import argparse
import sys
import motion
import almath


def main(session):
    """
    Use transformInterpolations Method on Arm
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    effector   = "LArm"
    frame      = motion.FRAME_TORSO
    axisMask   = almath.AXIS_MASK_VEL    # just control position
    useSensorValues = False

    path = []
    currentTf = motion_service.getTransform(effector, frame, useSensorValues)
    # point 1
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 -= 0.05 # y
    path.append(list(targetTf.toVector()))

    # point 2
    targetTf  = almath.Transform(currentTf)
    targetTf.r3_c4 += 0.04 # z
    path.append(list(targetTf.toVector()))

    # point 3
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 += 0.04 # y
    path.append(list(targetTf.toVector()))

    # point 4
    targetTf  = almath.Transform(currentTf)
    targetTf.r3_c4 -= 0.02 # z
    path.append(list(targetTf.toVector()))

    # point 5
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 -= 0.05 # y
    path.append(list(targetTf.toVector()))

    # point 6
    path.append(currentTf)

    times = [0.5, 1.0, 2.0, 3.0, 4.0, 4.5] # seconds

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_service.rest()


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
### 발

NAO의 왼쪽 발을 움직인다.
almotion_cartesianFoot.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Arm on Foot"""

import qi
import argparse
import sys
import almath
import motion


def main(session):
    """
    Use transformInterpolations Method on Foot.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    frame      = motion.FRAME_WORLD
    axisMask   = almath.AXIS_MASK_ALL   # full control
    useSensorValues = False

    # Lower the Torso and move to the side
    effector = "Torso"
    initTf   = almath.Transform(
        motion_service.getTransform(effector, frame, useSensorValues))
    deltaTf  = almath.Transform(0.0, -0.06, -0.03) # x, y, z
    targetTf = initTf*deltaTf
    path     = list(targetTf.toVector())
    times    = 2.0 # seconds
    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # LLeg motion
    effector = "LLeg"
    initTf = almath.Transform()

    try:
        initTf = almath.Transform(motion_service.getTransform(effector, frame, useSensorValues))
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    # rotation Z
    deltaTf  = almath.Transform(0.0, 0.04, 0.0)*almath.Transform().fromRotZ(45.0*almath.TO_RAD)
    targetTf = initTf*deltaTf
    path     = list(targetTf.toVector())
    times    = 2.0 # seconds

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_service.rest()


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

### 몸통

NAO의 몸통을 다른자세로 바꾼다.

#### Trajectory

~~~
almotion_cartesianTorso.py

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Torso"""

import qi
import argparse
import sys
import almath
import motion


def main(session):
    """
    Use transformInterpolations Method on Torso.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    effector   = "Torso"
    frame      =  motion.FRAME_WORLD
    axisMask   = almath.AXIS_MASK_ALL # full control
    useSensorValues = False

    # Define the changes relative to the current position
    dx         = 0.045 # translation axis X (meter)
    dy         = 0.050 # translation axis Y (meter)

    path = []
    currentTf = motion_service.getTransform(effector, frame, useSensorValues)

    # point 1
    targetTf  = almath.Transform(currentTf)
    targetTf.r1_c4 += dx
    path.append(list(targetTf.toVector()))

    # point 2
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 -= dy
    path.append(list(targetTf.toVector()))

    # point 3
    targetTf  = almath.Transform(currentTf)
    targetTf.r1_c4 -= dx
    path.append(list(targetTf.toVector()))

    # point 4
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 += dy
    path.append(list(targetTf.toVector()))

    # point 5
    targetTf  = almath.Transform(currentTf)
    targetTf.r1_c4 += dx
    path.append(list(targetTf.toVector()))

    # point 6
    path.append(currentTf)

    times = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] # seconds

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_service.rest()


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


### Hula Hoop
almotion_hulaHoop.py

~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method to play short animation"""

import qi
import argparse
import sys
import almath
import motion


def main(session):
    """
    Use transformInterpolations Method to play short animation.
    This example will only work on Nao.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # end initialize proxy, begin go to Stand Init

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    # end go to Stand Init, begin define control point
    effector        = "Torso"
    frame           =  motion.FRAME_ROBOT
    axisMask        = almath.AXIS_MASK_ALL
    useSensorValues = False

    currentTf = almath.Transform(motion_service.getTransform(effector, frame, useSensorValues))

    # end define control point, begin define target

    # Define the changes relative to the current position
    dx         = 0.03                    # translation axis X (meter)
    dy         = 0.03                    # translation axis Y (meter)
    dwx        = 8.0*almath.TO_RAD       # rotation axis X (rad)
    dwy        = 8.0*almath.TO_RAD       # rotation axis Y (rad)

    # point 01 : forward  / bend backward
    target1Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target1Tf *= almath.Transform(dx, 0.0, 0.0)
    target1Tf *= almath.Transform().fromRotY(-dwy)

    # point 02 : right    / bend left
    target2Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target2Tf *= almath.Transform(0.0, -dy, 0.0)
    target2Tf *= almath.Transform().fromRotX(-dwx)

    # point 03 : backward / bend forward
    target3Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target3Tf *= almath.Transform(-dx, 0.0, 0.0)
    target3Tf *= almath.Transform().fromRotY(dwy)

    # point 04 : left     / bend right
    target4Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target4Tf *= almath.Transform(0.0, dy, 0.0)
    target4Tf *= almath.Transform().fromRotX(dwx)

    path = []
    path.append(list(target1Tf.toVector()))
    path.append(list(target2Tf.toVector()))
    path.append(list(target3Tf.toVector()))
    path.append(list(target4Tf.toVector()))

    path.append(list(target1Tf.toVector()))
    path.append(list(target2Tf.toVector()))
    path.append(list(target3Tf.toVector()))
    path.append(list(target4Tf.toVector()))

    path.append(list(target1Tf.toVector()))
    path.append(list(currentTf.toVector()))

    timeOneMove  = 0.5 #seconds
    times = []
    for i in range(len(path)):
        times.append((i+1)*timeOneMove)

    # end define target, begin call motion api

    # call the cartesian control API

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_service.rest()


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

