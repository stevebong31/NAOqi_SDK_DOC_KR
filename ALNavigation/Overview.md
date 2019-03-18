## ALNavigation

### ALNavigation은 무엇을 하는가
ALNavigation API는 사용자가 로봇을 사용할 때 안전한 이동을 수행할 수 있도록 도와준다.

#### Pepper only

또한 페퍼는 몇 가지 모드에서 ALNavigation API를 사용할 수 있다:
- ALNavigationProxy::navigateTo Method와 함께 장애물 회피;
- 이동할 수 있는 공간 찾기 ALNavigationProxy::findFreeZone (이미지로 출력 예제)
- ALNavigationProxy::moveAlong Method와 함께 안전한 trajectory 실행
- 미지의 환경 탐사 그리고 위치 추적

### 어떻게 동작하는가

#### 장애물 회피 
움직이는 동안, 로봇은 모든 센서를 사용하여 이동 방향의 장애물을 감지한다.

### Safety map

Safety map은 motion safy, local navigation, 그리고 free zone API를 사용한다.

이 지도는 3D camera, laser ,sonar 등과 같이 탐지에 도움되는 모든 센서에서 나오는 데이터를 합쳐 만든 것이다.

잠재적 장애물은 직접적으로 보이지 않더라도 메모리에 남아 있을 수 있다. 이 메모리는 최대 15초까지 유지된다.

### 탐색과 위치 추적

페퍼는 다음 기능이 가능하다:
- 자동으로 미지의 환경을 탐험한다;
- 환경에 대해 지도를 작성한다;
- 맵으로 내비게이션을 하며 자신의 위치를 파악한다.

자신의 위치를 파악하고 미지의 환경을 매핑하는 과정은 SLAM 이라고 알려져 있다.
탐사 중, 페퍼는 자신의 Odometry와 레이저 센서로 SLAM을 수행한다.

페퍼가 한번 탐사를 끝내면, 맵은 2D 이미지로 변환된다.
 