# Python SDK - Overview

## Python SDK는 무엇인가.

Aldebaran 로봇을 위한 Python SDK는 다음 기능을 수행한다.

원격 머신의 C++ API를 모두 사용하게 하거나
원격 또는 로봇에서 작동 가능한 Python 모듈을 생성한다.

Python을 사용하는 것은 Aldebaran 로봇을 프로그래밍하는 가장 빠른 방법 중 하나이다.


## 핵심 개념 마스터하기

먼저 핵심 개념을 읽어보십시오.

기본 접근법은 다음과 같다.

1. ALProxy 
2. 사용할 모듈에 ALProxy 생성 
3. method 호출

이는 다음 예에서 확인 할 수 있으며, 자세한 것은 튜토리얼에서 설명합니다. : Making NAO speak

~~~
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "<IP of your robot>", 9559)
tts.say("Hello, world!")
~~~

Python SDK의 일부는 Choregraphe 내부적으로 사용하거나 자동으로 생성되므로, 이곳에 문서화되지 않은 것은 사용하지말거나, API 변경을 기다리십시오.


## ALProxy 

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


# ALBroker, ALModule