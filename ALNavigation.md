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
