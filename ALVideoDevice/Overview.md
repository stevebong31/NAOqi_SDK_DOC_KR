## ALVideoDevice
### ALVideoDevice은 무엇을 하는가
ALVideoDevice 모듈은 비디오 소스(예: 로봇의 카메라, 시뮬레이터)에서 ALFaceDetection또는 ALVisionRecognition과 같이 비디오 소스를 처리하는 모든 모듈에 영상을 효율적으로 제공하는 역할을 한다.

---

### 어떻게 동작 하는가

ALVideoDevice 모듈은 이미지를 필요로 하는 모듈과, 그 요구 사항을 매 순간 알고 있기 때문에, 처리하는 자원을 절약하면서 모든 모듈의 요구 사항을 충족시킬 비디오 장치에 대한 최소한의 구성을 설정할 수 있다.

---

### 다중 카메라 지원

각각의 알데바란 로봇은 특정한 카메라 모델을 가지고 있고, 로봇은 하나 이상의 카메라를 가지고 있다.

---

### 성능과 제한

#### 성능
로봇 카메라가 제공하는 기본 색상 공간을 직접 처리할 때 최고의 성능을 낸다. (YUV422) 기타 색상표의 경우 ALVideoDevice 모듈에 의해 변환되므로 주요 색상표의 처리 시간은 다음과 같다:

YUV422 < Yuv < YUV < RGB/BGR < HSY (기능성 측면에서 HSV/HSL에 가깝지만 처리속도가 더 빠름).

YUV 색상 공간은 RGB보다 강력해서 편하다:

- 휘도가 Y 채널에 있으므로 그레이 레벨 이미지를 얻기 위해 세 개의 RGB 레이어를 평균화할 필요가 없다.
- 색차는 순전히 U채널과 V채널에 모두 내장되어 있기 때문에, 휘도와 색차가 상관관계가 있는 RGB에 비해 작업하는 것이 더 쉽다.
- 상관관계가 없는 휘도와 색도 채널을 사용하므로, 처리하는데 CPU의 시간을 소비하지 않고 HSV/HSL와 동일한 이점을 제공한다.

#### 제한
현재 ATOM CPU에서 5FPS의 1280x960 HD이미지를 원격으로 요청하면 프레임 손실이 발생한다.(getImageRemote) 따라서 네트워크롤 통해 5fps HD 이상의 이미지를 가져오는 것은 추천하지 않는다. HD 이미지를 처리하는 모든 모듈이 로컬로 호출되는 경우 위와 같은 제한은 없다.(getImageLocal)

NAO v4(*)에서 압축되지 않은 YUV422 영상을 요청할 때 사용하는 해상도와 FPS는 다음과 같다.


local |	Gb Ethernet	 |100Mb Ethernet |	WiFi g
-------- | -------- | -------- | --------
40x30 (QQQQVGA) | 30fps | 30fps | 30fps	| 30fps
80x60 (QQQVGA)	| 30fps	| 30fps	| 30fps	| 30fps
160x120 (QQVGA)	| 30fps	| 30fps	| 30fps	| 30fps
320x240 (QVGA)	| 30fps	| 30fps	| 30fps	| 11fps
640x480 (VGA)	| 30fps	| 30fps	| 12fps	| 2.5fps
1280x960 (4VGA)	| 29fps	| 10fps	| 3fps	| 0.5fps

(*)

- 원격 성능은 클라이언트의 네트워크 구성에 따라 달라진다.
- 윈도우에서 모니터는 보통 21fps에서 차단되는 것으로 나타난다.
- 다른 원격 모듈은 그러한 제한을 받지 않는다.
1280x960의 GB Ethernet 성능은  WindowXP에서 테스트했다.

---

### 시작하기

1. ALVideoDeviceProxy::subscribeCamera에 요청해, 해상도, 색상공간 밑 프레임 등의 매개 변수를 전달하여 비전 모듈을 ALVideoDevice 프록시에 연걸하십시오.
2. 메인 루프에서 ALVideoDeviceProxy::getImageLocal 또는 ALVideoDeviceProxy::getImageRemote를 요청받아 이미지를 받아오십시오.
3. ALVideoDeviceProxy::releaseImage를 사용해 이미지 호출을 해제하십시오.
4. 모듈을 중지하려면 기본 루프에서 빠져나와 ALVideoDeviceProxy::unsubscribe를 요청하십시오.
---

### 추가 라이브러리 

#### OpenCV

C++에서 자신만의 비전 모듈을 개발하려면 OpenCV에 관심 있을 수 있다. 그것은 Vision 처리에 있어서 강력한 라이브러리이다. 우리는 현재 OpenCV 2.4를 사용하고 있다.

OpenCV에 대한 자세한 내용은 http://opencv.willowgarage.com/wiki/을 참조하십시오.

튜토리얼: http://doc.aldebaran.com/2-5/dev/cpp/examples/vision/opencv.html#cpp-tutos-opencv

#### ~~pYUV~~


### 시각 / 움직임 변환

변환 method는 좌표를 각도로 변환하는데 사용할 수 있고 반대의 경우도 유용할 수 있다. 예를 들어 감지 프로세스가 개체의 위치를 픽셀로 표시하면 이 위치를 각도로 변환하여 ALMotionProxy::setAngeles를 사용하여 로봇이 탐지된 개체 방향을 바라보게 할 수 있다. 

---
### 시뮬레이션 관리 

#### 로봇에서 비디오 재생하기. 

로봇에서 비디오를 재생하려면 비디오 장치를 시뮬레이터 모드로 구성하고 ALVideoDeviceProxy::putImage를 사용하십시오.