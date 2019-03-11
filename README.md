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

관절의 뻣뻣함을 0이 아닌 다른 값으로 설정하면, 로봇이 움직이지 않는다. (1~0)

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

또한 파일에서 판독한 결과를 어떻게 디코딩 하는지 주의해라. fp.read에 의해 반환된 객체는 유니코드 객체인데, 우리는 그것을 다시 인코딩해서  i’UTF-8’로 인코딩된 str 객체를 TTS 프록시가 사용할 수 있도록 만들어야한다.

파이썬은 'ASCII'(로봇의 현재 로컬)을 사용하여 문자열을 디코딩하려고 시도하므로 Print를 실행하면 작동하지 않는다.