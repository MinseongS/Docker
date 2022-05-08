# DataEngineer
신민성


## 구현 기능

### API1 : 일기예보 데이터 수집
- 처음 실행 될 때, 현재 시점부터 24시간 전까지의 데이터를 수집한다. (가능한 데이터 모두 수집)
- 한 시간마다 한 번씩 데이터를 수집한다.

### API2 : x, y 좌표에 대한 날씨 통계 데이터 조회
- 특정 x, y, 날짜에 대한 온도, 습도, 풍속의 최대값, 최소값, 중간값 1일간 누적 강수량을 데이터베이스에서 조회한다.

### API3 : 모든 좌표에 대한 날씨 통계 데이터 조회

- 모든 좌표의 특정 날짜에 대한 모든 데이터를 조회한다.



 
### 로컬 테스트

1. `Docker` 및 `docker-compose` 설치


2. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.

   ```
   $ git clone https://github.com/MinseongS/DataEngineer.git
   
   $ cd DataEngineer
   ```

3. docker-compose를 통해서 db와 API 1을 실행시킨다.

   ```
   $ docker-compose run -rm api1
   ```
   API 1 container는 계속 실행 중이고 한 시간에 한 번씩 날씨 데이터를 받아옵니다.

4. 1 - 새로운 cmd 창을 통해 API2 와 API3 를 각각 실행하고 원하는 parameter를 입력한다.

   ```
   $ docker-compose run -rm api2
   ```
   ```
   $ docker-compose run -rm api3
   ```
   2 - jupyter notebook파일 api2_graph, api3_graph 를 실행시켜 data를 시각화 하여 확인한다.
  
