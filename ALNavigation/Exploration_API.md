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
- 