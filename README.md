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