## Exploration API

~~~ py 
class ALNavigationProxy 
~~~

페퍼와 함께 exploration method를 사용할 수 있다:

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

--- 
### Experimental Methods

#### qi::Future<int> ALNavigationProxy::explore(float radius)

페퍼는 파라미터로 전달받은 반지름의 범위 내에서 자신의 주변 환경을 자율적으로 탐색한다.

#### Parameters:	
반지름 – 최대 탐색 거리 (meter).
#### Returns:	
최종 상태의 에러 코드를 보유하는 데이터.

---
#### void ALNavigationProxy::stopExploration()
진행중인 탐색이나 위치 추정을 중지한다. 

---

#### std::string ALNavigationProxy::saveExploration()¶
현재 탐색 데이터를 디스크에 저장하여 나중에 사용할 수 있게 한다.

- Return : 생성된 .explo 파일의 경로의 문자열

---
#### ALValue ALNavigationProxy::getMetricalMap()
현재 불러온 탐색을 바탕으로 지도를 반환한다 : [mpp, width, height, [originOffsetX, originOffsetY], [pxlVal, ...]]

- mpp는 화소 당 미터 단위의 지도 해상도,
- width와 height는 이미지 픽셀의 사이즈,
- originOffset은 지도 픽셀 (0,0)의 계측적 오프셋이다.
- 그리고 [pxlVal, ...]은 0(사용한 공간/갈 수 없는)에서 100(자유 공간/갈 수 있는)사이의 픽셀 부동 소수점 값의 버퍼이다. 
  
---

#### qi::Future<int> ALNavigationProxy::navigateToInMap(const std::vector<float>& target)
탐색한 지도를 바탕으로 페퍼가 원하는 목표로 이동하도록 한다.

예외 : 탐색을 로드하지 못했거나 위치 추정을 실행하지 못했을 경우.

참고 : 현재, 페퍼는 최종 목표로 theta를 사용하지 않는다. 최종 방향의 각도를 조절하기 위해서 ALMotion.moveTo를 사용할 수 있다.

- Parameters:	
target – [x, y, theta] 탐색한 맵 프레임에서의 목표.
- Returns:	
에러 코드.
---

#### ALValue ALNavigationProxy::getRobotPositionInMap()

현재 탐색한 지도 프레임에서 로봇의 위치를 추정한다.

예외 : 탐색을 로드하지 못했거나 위치 추정을 실행하지 못했을 경우.

- Returns : 추정된 위치 Pose의 ALValue

---
#### qi::Future<bool> ALNavigationProxy::loadExploration(std::string path)
디스크에 위치한 .explo를 불러온다. 

- Returns: 탐색 파일 로드를 성공 했을 때 반환.

---

#### qi::Future<ALValue> ALNavigationProxy::relocalizeInMap(const std::vector<float>& estimation)

localizer에게 추정된 포즈 주위로 다시 추정 할 것을 요청한다.

예외 : 탐색을 불러오지 못했을 경우.

- Parameters:	
estimation – [x, y, theta] 지도 프레임에서 로봇의 추정된 포즈
- Returns:	
a Future holding the resulting localized pose formatted as follow.


---
#### void ALNavigationProxy::startLocalization()

로봇의 위치 추정을 계산하는 탐색 루프를 시작한다. 

예외 : 탐색 파일을 로드하지 못했을 경우.

---
#### void ALNavigationProxy::stopLocalization()

로봇이 위치 추정을 계산하는 탐색 루프를 정지한다.

위치 추정 루프가 실행중이 아니라면 동작하지 않는다. 


### Custom types

#### Localized Pose

위치 추정 포즈는 다음과 같이 정의된다 :

[Pose, Uncertainty]

- 포즈는 localizer가 계산한 [X, Y, theta].
- Uncertainty는 위치 추정 포즈의 불확실성 정의하는 [radiusX, radiusY, orientation] 파라미터를 가진 타원이다.