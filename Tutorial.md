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

예시는 아래에 있다 : 스크립트를 실행하고 로봇앞에 얼굴을 내밀어라. 너는 'hello, you' 라는 말을 들을 수 있다.

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


### 훌라후프
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

### 팔과 몸통

여러 개의 이펙터를 좌표 명령으로 움직일 수 있다.

#### Trajectory 1
almotion_cartesianTorsoArm1.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Arm and Torso"""

import qi
import argparse
import sys
import almath
import motion


def main(session):
    """
    Use transformInterpolations Method on Arm and Torso
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    frame      = motion.FRAME_WORLD
    coef       = 0.5                   # motion speed
    times      = [coef, 2.0*coef, 3.0*coef, 4.0*coef]
    useSensorValues = False

    # Relative movement between current and desired positions
    dy         = +0.03                 # translation axis Y (meters)
    dz         = -0.03                 # translation axis Z (meters)
    dwx        = +8.0*almath.TO_RAD   # rotation axis X (radians)

    # Motion of Torso with _async process
    effector   = "Torso"

    path = []
    initTf = almath.Transform(motion_service.getTransform(effector, frame, useSensorValues))
    # point 1
    deltaTf  = almath.Transform(0.0, -dy, dz)*almath.Transform().fromRotX(-dwx)
    targetTf = initTf*deltaTf
    path.append(list(targetTf.toVector()))

    # point 2
    path.append(list(initTf.toVector()))

    # point 3
    deltaTf  = almath.Transform(0.0, dy, dz)*almath.Transform().fromRotX(dwx)
    targetTf = initTf*deltaTf
    path.append(list(targetTf.toVector()))

    # point 4
    path.append(list(initTf.toVector()))

    axisMask   = almath.AXIS_MASK_ALL  # control all the effector axes
    motion_service.transformInterpolations(effector, frame, path,
                                           axisMask, times, _async=True)

    # Motion of Arms with block process
    frame     = motion.FRAME_TORSO
    axisMask  = almath.AXIS_MASK_VEL  # control just the position
    times     = [1.0*coef, 2.0*coef]  # seconds

    # Motion of Right Arm during the first half of the Torso motion
    effector  = "RArm"

    path = []
    currentTf = motion_service.getTransform(effector, frame, useSensorValues)
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 -= 0.04 # y
    path.append(list(targetTf.toVector()))
    path.append(currentTf)

    motion_service.transformInterpolations(effector, frame, path, axisMask, times)

    # Motion of Left Arm during the last half of the Torso motion
    effector   = "LArm"

    path = []
    currentTf = motion_service.getTransform(effector, frame, useSensorValues)
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 += 0.04 # y
    path.append(list(targetTf.toVector()))
    path.append(currentTf)

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

almotion_cartesianTorsoArm2.py

~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use transformInterpolations Method on Arm and Torso"""

import qi
import argparse
import sys
import motion
import almath


def main(session):
    """
    Use transformInterpolations Method on Arm and Torso.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    frame      = motion.FRAME_ROBOT
    useSensorValues = False

    effectorList = ["LArm", "RArm"]

    # Motion of Arms with block process
    axisMaskList = [almath.AXIS_MASK_VEL, almath.AXIS_MASK_VEL]

    timesList    = [[1.0], [1.0]] # seconds

    # LArm path
    pathLArm = []
    targetTf  = almath.Transform(motion_service.getTransform("LArm", frame, useSensorValues))
    targetTf.r2_c4 -= 0.04 # y
    pathLArm.append(list(targetTf.toVector()))

    # RArm path
    pathRArm = []
    targetTf  = almath.Transform(motion_service.getTransform("RArm", frame, useSensorValues))
    targetTf.r2_c4 += 0.04 # y
    pathRArm.append(list(targetTf.toVector()))

    pathList = []
    pathList.append(pathLArm)
    pathList.append(pathRArm)

    motion_service.transformInterpolations(effectorList, frame, pathList,
                                       axisMaskList, timesList)

    effectorList = ["LArm", "RArm", "Torso"]

    # Motion of Arms and Torso with block process
    axisMaskList = [almath.AXIS_MASK_VEL,
                    almath.AXIS_MASK_VEL,
                    almath.AXIS_MASK_ALL]

    timesList    = [[4.0],                  # LArm  in seconds
                    [4.0],                  # RArm  in seconds
                    [1.0, 2.0, 3.0, 4.0]]   # Torso in seconds

    # LArm path
    pathLArm = []
    pathLArm.append(motion_service.getTransform("LArm", frame, useSensorValues))

    # RArm path
    pathRArm = []
    pathRArm.append(motion_service.getTransform("RArm", frame, useSensorValues))

    # Torso path
    pathTorso = []
    currentTf = motion_service.getTransform("Torso", frame, useSensorValues)

    # 1
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 += 0.04 # y
    pathTorso.append(list(targetTf.toVector()))

    # 2
    targetTf  = almath.Transform(currentTf)
    targetTf.r1_c4 -= 0.03 # x
    pathTorso.append(list(targetTf.toVector()))

    # 3
    targetTf  = almath.Transform(currentTf)
    targetTf.r2_c4 -= 0.04 # y
    pathTorso.append(list(targetTf.toVector()))

    # 4
    pathTorso.append(currentTf)

    pathList = []
    pathList.append(pathLArm)
    pathList.append(pathRArm)
    pathList.append(pathTorso)

    motion_service.transformInterpolations(effectorList, frame, pathList,
                                       axisMaskList, timesList)

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

## Whole body motion 

## 충돌 감지

이 에시는 NAO의 팔에 대한 충돌 감지 반응에 대해 보여준다. 충돌 감지가 없다면 물체에 부딪히고, 충돌 감지가 있다면 물체를 피한다.

almotion_collisionDetection.py

~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

''' Example :Collision detection - Arm Collision Detection '''

import qi
import argparse
import sys
import almath
import time


def moveArm(motion_service, target, has_hands, chain_name):
    ''' Function to make NAO bump on his Torso or Head with his arm '''

    # Set the fraction of max speed for the arm movement.
    pMaxSpeedFraction = 0.5

    # Define the final position.
    if target == "Torso":
        shoulderPitchAngle = 50
    elif target == "Head":
        shoulderPitchAngle = -50
    else:
        print "ERROR: target is unknown"
        print "Must be Torso or Head"
        print "---------------------"
        exit(1)

    ShoulderRollAngle  = 6
    ElbowYawAngle      = 0
    ElbowRollAngle     = -150

    if chain_name == "LArm":
        targetAngles = [shoulderPitchAngle, +ShoulderRollAngle,
            +ElbowYawAngle, +ElbowRollAngle]
    elif chain_name == "RArm":
        targetAngles = [shoulderPitchAngle, -ShoulderRollAngle,
            -ElbowYawAngle, -ElbowRollAngle]
    else:
        print "ERROR: chainName is unknown"
        print "Must be LArm or RArm"
        print "---------------------"
        exit(1)

    # Set the target angles according to the robot version.
    if has_hands:
        targetAngles += [0.0, 0.0]

    # Convert to radians.
    targetAngles = [x * almath.TO_RAD for x in targetAngles]

    # Move the arm to the final position.
    motion_service.angleInterpolationWithSpeed(
        chain_name, targetAngles, pMaxSpeedFraction)


def main(session, chain_name):
    """
    Collision detection : arm collision detection
    """
    # Get the services ALMotion, ALRobotModel & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    model_service = session.service("ALRobotModel")

    if model_service.getRobotType() != "Nao" or not model_service.hasArms():
        print "This test is not available for your Robot"
        print "---------------------"
        exit(1)

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    has_hands = model_service.hasHands()

    ###############################
    # Arm motion bumping on torso #
    ###############################

    # Disable collision detection on chainName.
    is_enable = False
    success = motion_service.setCollisionProtectionEnabled(chain_name, is_enable)
    if (not success):
        print("Failed to disable collision protection")
    time.sleep(1.0)

    # Make NAO's arm move so that it bumps its torso.
    target = "Torso"
    moveArm(motion_service, target, has_hands, chain_name)
    time.sleep(1.0)

    # Go back to pose init.
    posture_service.goToPosture("StandInit", 1.0)

    # Enable collision detection on chainName.
    is_enable = True
    success = motion_service.setCollisionProtectionEnabled(chain_name, is_enable)
    if (not success):
        print("Failed to enable collision protection")
    time.sleep(1.0)

    # Make NAO's arm move and see that it does not bump on the torso.
    target = "Torso"
    moveArm(motion_service, target, has_hands, chain_name)

    ##############################
    # Arm motion bumping on head #
    ##############################

    time.sleep(1.0)
    # Go back to pose init.
    posture_service.goToPosture("StandInit", 1.0)
    # Disable collision detection on chainName.
    is_enable = False
    success = motion_service.setCollisionProtectionEnabled(chain_name, is_enable)
    if (not success):
        print("Failed to disable collision protection")
    time.sleep(1.0)
    # Make NAO's arm move so that it bumps its head.
    target = "Head"
    moveArm(motion_service, target, has_hands, chain_name)

    time.sleep(1.0)
    # Go back to pose init.
    posture_service.goToPosture("StandInit", 1.0)
    # Enable collision detection on chainName.
    is_enable = True
    success = motion_service.setCollisionProtectionEnabled(chain_name, is_enable)
    if (not success):
        print("Failed to enable collision protection")
    # Make NAO's arm move and see that it does not bump on the head.
    target = "Head"
    moveArm(motion_service, target, has_hands, chain_name)

    time.sleep(1.0)
    # Go back to pose init.
    posture_service.goToPosture("StandInit", 1.0)

    # Go to rest position
    motion_service.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--chain", type=str, default="LArm",
                        choices=["LArm", "RArm"], help="Chain name")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.chain)

~~~

## ALMath

이 섹션은 libalmath Python wrapping을 어떻게 사용하는지 보여준다. Wrapping은 이 라이브러리에 포함된 모든 기능을 사용할 수 있게 해주며, 이는 동작과 관련된 연산(예:이펙터 위치)에 유용하다.

### Python wrapping
libalmath는 파이썬으로 Wrapping 되어 있다. 예를 들어 Choregraphe 또는 Python 스크립트에서 이 라이브러리를 사용할 수 있게 한다. Almath를 import 하려면 다음 줄을 실행하십시오.(Choregraphe 외부에서 코딩하려면 Python SDK - Installation Guide를 통해 SDK를 올바르게 설정하십시오)
~~~
import almath
~~~
다음 방법으로 libalmath의 method를 모두 불러올 수 있다.
~~~
almath.methodName(arg0, arg1, ...)
~~~

libalmath는 까다로운 형태를 사용하기 때문에, 정확하게 사용하려면 유의해야한다. 이는 올바른 형식을 직접적으로 제공하지 않는 ALMotion과 같은 다른 모듈과 연계시 어려울 수 있다.

### ALMath와 ALMotion 함께 사용하기

예시로 ALMotionProxy::getTransform Method를 사용하여 ALMotion에서 transform을 찾는 방법과 ALMath로 계산한 transform을 ALMotionProxy::setTransform을 사용하여 다시 ALMotion으로 전송하는 방법을 보여준다. (transform을 사용하는 다른 Method에서도 원리는 동일)


almath_transform.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Show how to use almath with python and send the results to
    the robot by using a proxy to ALMotion"""

import qi
import argparse
import sys
import time
import almath


def main(session):
    """
    Show how to use almath with python and send the results to
    the robot by using a proxy to ALMotion.
    """
    # Get the services AlMotion and ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # WakeUp
    motion_service.wakeUp()

    # Stand up.
    posture_service.goToPosture("StandInit", 0.3)

    chainName = "RArm"
    frame = 1 # FRAME_WORLD
    useSensors = True

    ##############################################
    # Retrieve a transform matrix using ALMotion #
    ##############################################

    # Retrieve current transform from ALMotion.
    # Convert it to a transform matrix for ALMath.
    origTransform = almath.Transform(
        motion_service.getTransform(chainName, frame, useSensors))

    # Visualize the transform using overriden print from ALMath
    print "Original transform"
    print origTransform

    ##########################################################
    # Use almath to do some computations on transform matrix #
    ##########################################################

    # Compute a transform corresponding to the desired move
    # (here, move the chain for 5cm along the Z axis and the X axis).
    moveTransform = almath.Transform.fromPosition(0.05, 0.0, 0.05)

    # Compute the corresponding target transform.
    targetTransform = moveTransform * origTransform

    # Visualize it.
    print "Target transform"
    print targetTransform

    ##############################################
    # Send a transform to the robot via ALMotion #
    ##############################################

    # Convert it to a tuple.
    targetTransformList = list(targetTransform.toVector())

    # Send the target transform to NAO through ALMotion.
    fractionOfMaxSpeed = 0.5
    axisMask = almath.AXIS_MASK_VEL # Translation X, Y, Z
    motion_service.setTransforms(
        chainName,
        frame,
        targetTransformList,
        fractionOfMaxSpeed,
        axisMask)

    time.sleep(2.0)
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

### Using ALMath to generate footsteps

## Sensors

이 섹션에선 어떻게 파이썬에서 ALMemory로 부터 센서 값을 가져올 수 있는지를 보여준다.
이를 실행하기 위해 예제 파일 내에서 로봇의 IP 주소를 수정한다. 

### 압력센서 값

sensors_getFsrValues.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use getData Method to Use FSR Sensors"""

import qi
import argparse
import sys


def main(session):
    """
    This example uses the getData method to use FSR sensors.
    """
    # Get the service ALMemory.

    memory_service = session.service("ALMemory")

    # Get The Left Foot Force Sensor Values
    LFsrFL = memory_service.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    LFsrFR = memory_service.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    LFsrBL = memory_service.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    LFsrBR = memory_service.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

    print( "Left FSR [Kg] : %.2f %.2f %.2f %.2f" %  (LFsrFL, LFsrFR, LFsrBL, LFsrBR) )

    # Get The Right Foot Force Sensor Values
    RFsrFL = memory_service.getData("Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value")
    RFsrFR = memory_service.getData("Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value")
    RFsrBL = memory_service.getData("Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value")
    RFsrBR = memory_service.getData("Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value")

    print( "Right FSR [Kg] : %.2f %.2f %.2f %.2f" %  (RFsrFL, RFsrFR, RFsrBL, RFsrBR) )


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

### 관성 센서 값

sensors_getIntertialValues.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use getData Method to Get Inertial Values"""

import qi
import argparse
import sys


def main(session):
    """
    This example uses the getData method to get Inertial Values.
    """
    # Get the service ALMemory.

    memory_service = session.service("ALMemory")

    # Get the Gyrometers Values
    GyrX = memory_service.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
    GyrY = memory_service.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
    print ("Gyrometers value X: %.3f, Y: %.3f" % (GyrX, GyrY))

    # Get the Accelerometers Values
    AccX = memory_service.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
    AccY = memory_service.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
    AccZ = memory_service.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")
    print ("Accelerometers value X: %.3f, Y: %.3f, Z: %.3f" % (AccX, AccY,AccZ))

    # Get the Compute Torso Angle in radian
    TorsoAngleX = memory_service.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
    TorsoAngleY = memory_service.getData("Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value")
    print ("Torso Angles [radian] X: %.3f, Y: %.3f" % (TorsoAngleX, TorsoAngleY))


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

### 초음파

sensors_sonar.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use getData Method to Use Sonars Sensors"""

import qi
import argparse
import sys


def main(session):
    """
    This example uses the getData method to use sonars sensors.
    """
    # Get the services ALMemory and ALSonar.

    memory_service = session.service("ALMemory")
    sonar_service = session.service("ALSonar")

    # Subscribe to sonars, this will launch sonars (at hardware level)
    # and start data acquisition.
    sonar_service.subscribe("myApplication")

    # Now you can retrieve sonar data from ALMemory.
    # Get sonar left first echo (distance in meters to the first obstacle).
    memory_service.getData("Device/SubDeviceList/US/Left/Sensor/Value")

    # Same thing for right.
    memory_service.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    # Unsubscribe from sonars, this will stop sonars (at hardware level)
    sonar_service.unsubscribe("myApplication")

    # Please read Sonar ALMemory keys section
    # if you want to know the other values you can get.


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

## 오디오
## 오디오 장치

이 섹션은 ALAudioDevice가 가능한 일을 보여준다.

### 마이크 신호 처리
마이크 신호를 가져오고 RMS 레벨을 계산한다.

audio_soundprocessing.py

~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Get Signal from Front Microphone & Calculate its rms Power"""


import qi
import argparse
import sys
import time
import numpy as np


class SoundProcessingModule(object):
    """
    A simple get signal from the front microphone of Nao & calculate its rms power.
    It requires numpy.
    """

    def __init__( self, app):
        """
        Initialise services and variables.
        """
        super(SoundProcessingModule, self).__init__()
        app.start()
        session = app.session

        # Get the service ALAudioDevice.
        self.audio_service = session.service("ALAudioDevice")
        self.isProcessingDone = False
        self.nbOfFramesToProcess = 20
        self.framesCount=0
        self.micFront = []
        self.module_name = "SoundProcessingModule"

    def startProcessing(self):
        """
        Start processing
        """
        # ask for the front microphone signal sampled at 16kHz
        # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
        self.audio_service.setClientPreferences(self.module_name, 16000, 3, 0)
        self.audio_service.subscribe(self.module_name)

        while self.isProcessingDone == False:
            time.sleep(1)

        self.audio_service.unsubscribe(self.module_name)

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        """
        Compute RMS from mic.
        """
        self.framesCount = self.framesCount + 1

        if (self.framesCount <= self.nbOfFramesToProcess):
            # convert inputBuffer to signed integer as it is interpreted as a string by python
            self.micFront=self.convertStr2SignedInt(inputBuffer)
            #compute the rms level on front mic
            rmsMicFront = self.calcRMSLevel(self.micFront)
            print "rms level mic front = " + str(rmsMicFront)
        else :
            self.isProcessingDone=True

    def calcRMSLevel(self,data) :
        """
        Calculate RMS level
        """
        rms = 20 * np.log10( np.sqrt( np.sum( np.power(data,2) / len(data)  )))
        return rms

    def convertStr2SignedInt(self, data) :
        """
        This function takes a string containing 16 bits little endian sound
        samples as input and returns a vector containing the 16 bits sound
        samples values converted between -1 and 1.
        """
        signedData=[]
        ind=0;
        for i in range (0,len(data)/2) :
            signedData.append(data[ind]+data[ind+1]*256)
            ind=ind+2

        for i in range (0,len(signedData)) :
            if signedData[i]>=32768 :
                signedData[i]=signedData[i]-65536

        for i in range (0,len(signedData)) :
            signedData[i]=signedData[i]/32768.0

        return signedData


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
        app = qi.Application(["SoundProcessingModule", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    MySoundProcessingModule = SoundProcessingModule(app)
    app.session.registerService("SoundProcessingModule", MySoundProcessingModule)
    MySoundProcessingModule.startProcessing()

~~~

## Vision

이 섹션에는 NAO의 카메라에서 이미지를 얻는 방법과 PIL 또는 PyQt로 시각화 하는 방법을 보여준다. 

### 이미지 얻기
로봇의 이미지를 얻어오는 예시다.
videoInput_getImage.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Shows how images can be accessed through ALVideoDevice"""

import qi
import argparse
import sys
import time
import vision_definitions



def main(session):
    """
    This is just an example script that shows how images can be accessed
    through ALVideoDevice in Python.
    Nothing interesting is done with the images in this example.
    """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")

    # Register a Generic Video Module
    resolution = vision_definitions.kQQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 20

    nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

    print 'getting images in remote'
    for i in range(0, 20):
        print "getting image " + str(i)
        video_service.getImageRemote(nameId)
        time.sleep(0.05)

    video_service.unsubscribe(nameId)


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

### PIL을 사용해 이미지 시각화하기


vision_getandsaveimage.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Get an image. Display it and save it using PIL."""

import qi
import argparse
import sys
import time
import Image


def main(session):
    """
    First get an image, then show it on the screen with PIL.
    """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = video_service.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    video_service.unsubscribe(videoClient)


    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))

    # Create a PIL Image from our pixel array.
    im = Image.fromstring("RGB", (imageWidth, imageHeight), image_string)

    # Save the image.
    im.save("camImage.png", "PNG")

    im.show()


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

### PyQt 사용하여 NAO 이미지 실시간 시각화하기 

vision_showimages.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Shows how to show live images from Nao using PyQt"""

import qi
import argparse
import sys
from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter
import vision_definitions


def main(session, robot_ip, port):
    """
    This is a tiny example that shows how to show live images from Nao using PyQt.
    You must have python-qt4 installed on your system.
    """
    CameraID = 0

    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")
    app = QApplication([robot_ip, port])
    myWidget = ImageWidget(video_service, CameraID)
    myWidget.show()
    sys.exit(app.exec_())


class ImageWidget(QWidget):
    """
    Tiny widget to display camera images from Naoqi.
    """
    def __init__(self, video_service, CameraID, parent=None):
        """
        Initialization.
        """
        QWidget.__init__(self, parent)
        self.video_service = video_service
        self._image = QImage()
        self.setWindowTitle('Robot')

        self._imgWidth = 320
        self._imgHeight = 240
        self._cameraID = CameraID
        self.resize(self._imgWidth, self._imgHeight)

        # Our video module name.
        self._imgClient = ""

        # This will contain this alImage we get from Nao.
        self._alImage = None

        self._registerImageClient()

        # Trigget 'timerEvent' every 100 ms.
        self.startTimer(100)


    def _registerImageClient(self):
        """
        Register our video module to the robot.
        """
        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace
        self._imgClient = self.video_service.subscribe("_client", resolution, colorSpace, 5)

        # Select camera.
        self.video_service.setParam(vision_definitions.kCameraSelectID,
                                  self._cameraID)


    def _unregisterImageClient(self):
        """
        Unregister our naoqi video module.
        """
        if self._imgClient != "":
            self.video_service.unsubscribe(self._imgClient)


    def paintEvent(self, event):
        """
        Draw the QImage on screen.
        """
        painter = QPainter(self)
        painter.drawImage(painter.viewport(), self._image)


    def _updateImage(self):
        """
        Retrieve a new image from Nao.
        """
        self._alImage = self.video_service.getImageRemote(self._imgClient)
        self._image = QImage(self._alImage[6],           # Pixel array.
                             self._alImage[0],           # Width.
                             self._alImage[1],           # Height.
                             QImage.Format_RGB888)


    def timerEvent(self, event):
        """
        Called periodically. Retrieve a nao image, and update the widget.
        """
        self._updateImage()
        self.update()


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        self._unregisterImageClient()


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
    main(session, args.ip, args.port)

~~~

## Video recording

이 섹션은 다른 형식으로 NAO의 비디오를 녹화하는 예시이다.
### avi로 녹화하기
로봇에서 나오의 카메라를 .avi 형식으로 비디오로 녹화한다.

vision_videorecord.py

~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Demonstrates how to  to record a video file on the robot"""

import qi
import argparse
import sys
import time


def main(session):
    """
    This example demonstrates how to use the ALVideoRecorder module to record a
    video file on the robot.
    """
    # Get the service ALVideoRecorder.

    vid_recorder_service = session.service("ALVideoRecorder")

    # This records a 320*240 MJPG video at 10 fps.
    # Note MJPG can't be recorded with a framerate lower than 3 fps.
    vid_recorder_service.setResolution(1)
    vid_recorder_service.setFrameRate(10)
    vid_recorder_service.setVideoFormat("MJPG")
    vid_recorder_service.startRecording("/home/nao/recordings/cameras", "myvideo")

    time.sleep(5)

    # Video file is saved on the robot in the
    # /home/nao/recordings/cameras/ folder.
    videoInfo = vid_recorder_service.stopRecording()

    print "Video was saved on the robot: ", videoInfo[1]
    print "Num frames: ", videoInfo[0]


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

## 얼굴 감지와 따라가기

이 섹션은 ALFaceDetection가 가능한 일을 보여준다.

### 감지기

얼굴을 감지하고 얼굴에 대한 정보를 출력한다.

vision_faceDetection.py
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

### 따라가기

얼굴을 감지하고 NAO의 머리가 따라간다.

vision_setfacetracking.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Modify Face Tracking policy on the robot."""

import qi
import argparse
import sys


def main(session):
    """
    When tracking is activated, faces looking sideways, or located further away
    should be tracked for a longer period.
    Launch Monitor, Camera-Viewer, activate face detection, and see if it works better.
    """

    tracking_enabled = True

    # Get the service ALFaceDetection.

    face_service = session.service("ALFaceDetection")

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled

    # Enable or disable tracking.
    face_service.enableTracking(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", face_service.isTrackingEnabled()


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

ALLandMarkDetection의 예시이다.

### 랜드마크 감지하기

랜드마크를 감지하고, 랜드마크의 정보를 출력한다.

vision_landMarkDetection.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Demonstrates how to use the ALLandMarkDetection module."""

import qi
import time
import sys
import argparse


class LandmarkDetector(object):
    """
    We first instantiate a proxy to the ALLandMarkDetection module
    Note that this module should be loaded on the robot's naoqi.
    The module output its results in ALMemory in a variable
    called "LandmarkDetected".
    We then read this ALMemory value and check whether we get
    interesting things.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)
        # Get the services ALTextToSpeech and ALLandMarkDetection.
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0 )
        self.got_landmark = False

    def on_landmark_detected(self, value):
        """
        Callback for event LandmarkDetected.
        """
        if value == []:  # empty value when the landmark disappears
            self.got_landmark = False
        elif not self.got_landmark:  # only speak the first time a landmark appears
            self.got_landmark = True
            print "I saw a landmark! "
            self.tts.say("I saw a landmark! ")
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of mark_Info's.
            markInfoArray = value[1]
            for markInfo in markInfoArray:

                # First Field = Shape info.
                markShapeInfo = markInfo[0]

                # Second Field = Extra info (ie, mark ID).
                markExtraInfo = markInfo[1]
                print "mark  ID: %d" % (markExtraInfo[0])
                print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscribe("LandmarkDetector")
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
        app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()

~~~

### 랜드마크 감지의 Callback

ALMemory에서 올바른 Event를 요청받음으로써 랜드마크 검출에 반응한다.

vision_onMarkDataChange.py
~~~
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Demonstrates how to use the ALLandMarkDetection module."""

import qi
import time
import sys
import argparse


class LandmarkDetector(object):
    """
    We first instantiate a proxy to the ALLandMarkDetection module
    Note that this module should be loaded on the robot's naoqi.
    The module output its results in ALMemory in a variable
    called "LandmarkDetected".
    We then read this ALMemory value and check whether we get
    interesting things.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)
        # Get the services ALTextToSpeech and ALLandMarkDetection.
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0 )
        self.got_landmark = False

    def on_landmark_detected(self, value):
        """
        Callback for event LandmarkDetected.
        """
        if value == []:  # empty value when the landmark disappears
            self.got_landmark = False
        elif not self.got_landmark:  # only speak the first time a landmark appears
            self.got_landmark = True
            print "I saw a landmark! "
            self.tts.say("I saw a landmark! ")
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of mark_Info's.
            markInfoArray = value[1]
            for markInfo in markInfoArray:

                # First Field = Shape info.
                markShapeInfo = markInfo[0]

                # Second Field = Extra info (ie, mark ID).
                markExtraInfo = markInfo[1]
                print "mark  ID: %d" % (markExtraInfo[0])
                print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscribe("LandmarkDetector")
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
        app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()

~~~

### 랜드마크 위치추적

transform을 사용해 랜드마크를 감지하고 로봇 공간안에서 위치를 추적한다.

vision_localization.py
~~~

#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Demonstrates a way to localize the robot with ALLandMarkDetection"""

import qi
import time
import sys
import argparse
import math
import almath


class LandmarkDetector(object):
    """
    We first instantiate a proxy to the ALLandMarkDetection module
    Note that this module should be loaded on the robot's naoqi.
    The module output its results in ALMemory in a variable
    called "LandmarkDetected".
    We then read this ALMemory value and check whether we get
    interesting things.
    After that we get the related position of the landmark compared to robot.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)
        # Get the services ALTextToSpeech, ALLandMarkDetection and ALMotion.
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.motion_service = session.service("ALMotion")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0 )
        self.got_landmark = False
        # Set here the size of the landmark in meters.
        self.landmarkTheoreticalSize = 0.06 #in meters
        # Set here the current camera ("CameraTop" or "CameraBottom").
        self.currentCamera = "CameraTop"

    def on_landmark_detected(self, markData):
        """
        Callback for event LandmarkDetected.
        """
        if markData == []:  # empty value when the landmark disappears
            self.got_landmark = False
        elif not self.got_landmark:  # only speak the first time a landmark appears
            self.got_landmark = True
            print "I saw a landmark! "
            self.tts.say("I saw a landmark! ")

            # Retrieve landmark center position in radians.
            wzCamera = markData[1][0][0][1]
            wyCamera = markData[1][0][0][2]

            # Retrieve landmark angular size in radians.
            angularSize = markData[1][0][0][3]

            # Compute distance to landmark.
            distanceFromCameraToLandmark = self.landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))

            # Get current camera position in NAO space.
            transform = self.motion_service.getTransform(self.currentCamera, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)

            # Compute the rotation to point towards the landmark.
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

            # Compute the translation to reach the landmark.
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

            # Combine all transformations to get the landmark position in NAO space.
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform *cameraToLandmarkTranslationTransform

            print "x " + str(robotToLandmark.r1_c4) + " (in meters)"
            print "y " + str(robotToLandmark.r2_c4) + " (in meters)"
            print "z " + str(robotToLandmark.r3_c4) + " (in meters)"

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscribe("LandmarkDetector")
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
        app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()
~~~

