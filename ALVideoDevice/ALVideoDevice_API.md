## ALVideoDevice API

### Method list
다른 모듈처럼 이 모듈은 ALModule API로부터 method를 상속받는다. 또한 다음과 같은 구체적인 방법이 있다.

(해당 모듈은 method가 많아 많이 사용하는 튜토리얼 코드 위주로 분석하였다.)

---

#### class ALVideoDeviceProxy
Module Subscription Management

- ALVideoDeviceProxy::subscribeCamera
- ALVideoDeviceProxy::subscribeCameras
- ALVideoDeviceProxy::unsubscribe
- ALVideoDeviceProxy::getSubscribers

#### Camera Management
- ALVideoDeviceProxy::getCameraIndexes
- ALVideoDeviceProxy::hasDepthCamera
- ALVideoDeviceProxy::getCameraModel
- ALVideoDeviceProxy::getCameraName
- ALVideoDeviceProxy::getActiveCamera()
- ALVideoDeviceProxy::setActiveCamera
- ALVideoDeviceProxy::getFrameRate()
- ALVideoDeviceProxy::getResolution()
- ALVideoDeviceProxy::getColorSpace()
- ALVideoDeviceProxy::getHorizontalFOV
- ALVideoDeviceProxy::getVerticalFOV
- ALVideoDeviceProxy::getParameter
- ALVideoDeviceProxy::getParameterRange
- ALVideoDeviceProxy::setParameter
- ALVideoDeviceProxy::setParameterToDefault
- ALVideoDeviceProxy::setAllParametersToDefault
- ALVideoDeviceProxy::openCamera
- ALVideoDeviceProxy::closeCamera
- ALVideoDeviceProxy::isCameraOpen
- ALVideoDeviceProxy::startCamera
- ALVideoDeviceProxy::stopCamera
- ALVideoDeviceProxy::isCameraStarted

#### Mono Stream Management
- ALVideoDeviceProxy::getActiveCamera()
- ALVideoDeviceProxy::setActiveCamera
- ALVideoDeviceProxy::getFrameRate()
- ALVideoDeviceProxy::setFrameRate
- ALVideoDeviceProxy::getResolution()
- ALVideoDeviceProxy::setResolution
- ALVideoDeviceProxy::getColorSpace()
- ALVideoDeviceProxy::setColorSpace
- ALVideoDeviceProxy::getCameraParameter
- ALVideoDeviceProxy::getCameraParameterRange
- ALVideoDeviceProxy::setCameraParameter
- ALVideoDeviceProxy::setCameraParameterToDefault
- ALVideoDeviceProxy::setAllCameraParametersToDefault
- ALVideoDeviceProxy::getDirectRawImageLocal
- ALVideoDeviceProxy::getDirectRawImageRemote
- ALVideoDeviceProxy::releaseDirectRawImage
- ALVideoDeviceProxy::getImageLocal
- ALVideoDeviceProxy::getImageRemote
- ALVideoDeviceProxy::releaseImage

#### Multi Stream Management
- ALVideoDeviceProxy::getActiveCameras
- ALVideoDeviceProxy::setActiveCameras
- ALVideoDeviceProxy::getResolutions
- ALVideoDeviceProxy::setResolutions
- ALVideoDeviceProxy::getColorSpaces
- ALVideoDeviceProxy::setColorSpaces
- ALVideoDeviceProxy::getCamerasParameter
- ALVideoDeviceProxy::setCamerasParameter
- ALVideoDeviceProxy::setCamerasParameterToDefault
- ALVideoDeviceProxy::getDirectRawImagesLocal
- ALVideoDeviceProxy::getDirectRawImagesRemote
- ALVideoDeviceProxy::releaseDirectRawImages
- ALVideoDeviceProxy::getImagesLocal
- ALVideoDeviceProxy::getImagesRemote
- ALVideoDeviceProxy::releaseImages
Simulation
- ALVideoDeviceProxy::putImage
- ALVideoDeviceProxy::getExpectedImageParameters
Conversion
- ALVideoDeviceProxy::getAngularPositionFromImagePosition
- ALVideoDeviceProxy::getImagePositionFromAngularPosition
- ALVideoDeviceProxy::getAngularSizeFromImageSize
- ALVideoDeviceProxy::getImageSizeFromAngularSize
- ALVideoDeviceProxy::getImageInfoFromAngularInfo
- ALVideoDeviceProxy::getImageInfoFromAngularInfoWithResolution
#### Deprecated Methods
- ALVideoDeviceProxy::onClientDisconnected
- ALVideoDeviceProxy::subscribe
- ALVideoDeviceProxy::unsubscribeAllInstances
- ALVideoDeviceProxy::getVIMResolution
- ALVideoDeviceProxy::getVIMColorSpace
- ALVideoDeviceProxy::getVIMFrameRate
- ALVideoDeviceProxy::getGVMResolution
- ALVideoDeviceProxy::getGVMColorSpace
- ALVideoDeviceProxy::getGVMFrameRate
- ALVideoDeviceProxy::startFrameGrabber()
- ALVideoDeviceProxy::stopFrameGrabber()
- ALVideoDeviceProxy::isFrameGrabberOff()
- ALVideoDeviceProxy::getCameraModelID
- ALVideoDeviceProxy::setParam
- ALVideoDeviceProxy::getParam
- ALVideoDeviceProxy::setParamDefault
- ALVideoDeviceProxy::getAngPosFromImgPos
- ALVideoDeviceProxy::getAngSizeFromImgSize
- ALVideoDeviceProxy::getImgInfoFromAngInfo
- ALVideoDeviceProxy::getImgInfoFromAngInfoWithRes
- ALVideoDeviceProxy::getImgPosFromAngPos
- ALVideoDeviceProxy::getImgSizeFromAngSize
- ALVideoDeviceProxy::getExpectedImageParameters()
- ALVideoDeviceProxy::setSimCamInputSize
- ALVideoDeviceProxy::putImage()
- ALVideoDeviceProxy::resolutionToSizes
- ALVideoDeviceProxy::sizesToResolution
- ALVideoDeviceProxy::startFrameGrabber()
- ALVideoDeviceProxy::stopFrameGrabber()
- ALVideoDeviceProxy::isFrameGrabberOff()
- ALVideoDeviceProxy::getHorizontalAperture
- ALVideoDeviceProxy::getVerticalAperture
- ALVideoDeviceProxy::recordVideo
- ALVideoDeviceProxy::stopVideo

---

### Module Subscription

std::string ALVideoDeviceProxy::subscribeCamera(const std::string& Name, const int& CameraIndex, const int& Resolution, const int& ColorSpace, const int& Fps)

ALVideoDevice를 요청하십시오. 비디오 모듈이 ALVideoDevice에 등록되면, 요청된 이미지 형식의 버퍼가 버퍼 목록에 추가된다.


#### Parameters:	
- Name – 요청 받는 모듈의 이름.
- CameraIndex – 비디오 시스템의 카메라 인덱스
  
Parameter ID Name | ID Value | More details ...
-------- | -------- | --------
AL::kTopCamera | 0 | 2D Cameras
AL::kBottomCamera | 1 | 2D Cameras
AL::kDepthCamera | 2 | Reconstructed 3D Sensor
AL::kStereoCamera | 3 | Stereo Camera

- Resolution – 해상도 

Parameter ID Name	| ID Value	| Description
-------- | -------- | --------
AL::kQQQQVGA	| 8	| Image of 40*30px
AL::kQQQVGA	| 7	 | Image of 80*60px
AL::kQQVGA	| 0	| Image of 160*120px
AL::kQVGA	| 1	| Image of 320*240px
AL::kVGA	| 2	| Image of 640*480px
AL::k4VGA	| 3	| Image of 1280*960px
AL::k16VGA	| 4	| Image of 2560*1920px



- ColorSpace – 색공간

Parameter ID Name	| ID Value	| Number of layers	| Number of channels	| Description
-------- | -------- | -------- | -------- | -------- 
AL::kYuvColorSpace | 0 |	1 |	1 |	Buffer only contains the Y (luma component) equivalent to one unsigned char
AL::kRGBColorSpace	| 11  | 3	| 3	| Buffer contains triplet on the format 0xBBGGRR, equivalent to three unsigned char
- Fps – Fps
- 
#### Returns:	
모듈이 ALVideoDevice에 등록한 문자열. 오류가 발생한 경우 문자열이 비어있다.

##### 경고 : 같은 이름은 6번만 사용할 수 있다.

메모 : 로컬 모듈에 비해 원격 모듈이 가지는 프레임 속도는 사용하는 네트워크 대역에 따라 달라진다. (예:HD 카메라와의 기가비트 이더넷 연결시 1280x960@10fps까지 가능하다.)

---
std::string ALVideoDeviceProxy::subscribeCameras(const std::string& Name, const AL::ALValue& CameraIndexes, const AL::ALValue& Resolutions, const AL::ALValue& ColorSpaces, const int& Fps)

#### Parameters:
ALVideoDeviceProxy::subscribeCamera와 사용법은 동일 하나 여러개의 카메라를 요청할 수 있으며 배열로 작성한다. 동일한 카메라 인덱스를 여러 번 요청할 수 없다.
 
 메모 : 기본적으로 액티브 카메라는 어레이의 첫 번째 카메라가 된다. 반환된 요청 이름은 구독 모듈 이름과 다를 수 있다.

 ---

 bool ALVideoDeviceProxy::unsubscribe(const std::string& Handle)

ALVideoDevice에서 모듈을 해제한다.

#### Parameters:	
- Handle – 요청한 subscriber의 식별 ID.
#### Returns:	
- 성공했다면 True, 실패했다면 False.

alvideodevice_subscribe.cpp
~~~ cpp
#include <alproxies/alvideodeviceproxy.h>
#include <alvision/alvisiondefinitions.h>

#include <iostream>

int main(int argc, char **argv)
{
  if (argc < 2) {
    std::cerr << "Usage: videodevice_subscribe pIp" << std::endl;
    return 1;
  }
  const std::string pIp = argv[1];

  // Proxy to ALVideoDevice.
  AL::ALVideoDeviceProxy cameraProxy(pIp);

  // Subscribe a Vision Module to ALVideoDevice, starting the
  // frame grabber if it was not started before.
  std::string subscriberID = "subscriberID";
  int fps = 5;
  // The subscriberID can be altered if other instances are already running
  subscriberID = cameraProxy.subscribe(subscriberID, AL::kVGA, AL::kRGBColorSpace, fps);

  // Do something...

  // Unsubscribe the V.M.
  cameraProxy.unsubscribe(subscriberID);

  return 0;
}

~~~

alvideodevice_subscribe.py
~~~ py
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Shows how images can be accessed through ALVideoDevice"""

import qi
from naoqi import ALProxy
import sys
import time
import vision_definitions


video_service = ALProxy("ALVideoDevice" ,nao_ip, 9559)


# Register a Generic Video Module
resolution = vision_definitions.kQQVGA
colorSpace = vision_definitions.kYUVColorSpace
fps = 20

nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

print 'getting images in remote'
for i in range(0, 20):
    print "getting image " + str(i)
    sub_nameId = video_service.getImageRemote(nameId)
    time.sleep(0.05)

video_service.unsubscribe(sub_nameId)

~~~