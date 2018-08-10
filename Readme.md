# 재밌었다....


# 명세



- 목표 : 유투브 동영상이 얼마나 대박을 칠지 예측하는 기능을 구현해보자



가설 : 동영상의 부수적인 정보를 통해서 특정 동영상의 흥행정도를 파악할 수 있을까





**Step 1** 

- 특징 설명

  - 데이터 출처, 데이터 개요

  - 특징 설명 : 변수명, 변수내용

    



<u>Q : 그렇다면 흥행이란 무엇일까?</u> 

**Step 2** 

- 흥행의 기준 :
  - 제공된 데이터셋에는 흥행여부에 대한 정보가 없다
  - 흥행의 수치적 기준을 세울 필요가 있다
  - **등급제 도입 : 1 ~ 9등급 (수능등급제 적용)**
    - **X : 조회수, Y : 동영상 수**



<u>Q : 조회수가 많은 유투버의 동영상엔 특별한 무엇이 있을까?</u>

**Step 3** : 

- 원본 데이터 특징 추출
  - Numeric 데이터 테이블 (등급 포함) 및 각 특징별 분포(그래프)

- 추가적인 정보 추출

  Q : 정성적 데이터를 한 번 입양해볼까?

  - title, tags, description 데이터는 너무 광범위하다. (전처리가 필요하다)
  - 위 데이터를 정량화 시키기 위한 작업 수행 :
    - 데이터 클러스터링(감성)을 통한 데이터 정형화



<u>Q : 위에서 얻은 분포를 수치적으로 분석해보도록 하자</u>

**Step 4 : 특징간의 상관관계 분석**

- 일반적으로 3차 이상의 교호작용은 나오기 힘드므로 2차까지만 파악하도록 한다

  - Multicolinearity 문제가 발생 가능성을 배제하기 위함

- 그래프 및 수치(R) 제공

  결과가 있든 없든 알려주기



(상태 : 사용하고자 하는 특징이 추출된 상태)

<u>Q : 추출한 특징 중, 결과값에 가장 큰 영향을 미치는 요인이 무엇일까?</u>

**Step 5 :**

- 특징 Xi 가 등급을 얼마나 잘 나누는지 정도를 파악하도록 한다

  - 만약 특징 Xi가 등급별로 상이한 값을 갖는다면, 등급을 구분 짓는 좋은 변수로 생각 할 수 있다

  - X축 - 조회수 (등급별), Y축 - 특징 Xi for all Xs

    - 그래프, 테이블(잔차 점수)
    - 구간별 평균(9개) 도축
    - 전체평균에서 각각의 차이의 합 (residual 합)
    - 잔차가 가장 큰 특징 Xi가 가장 좋은 등급 구분 기준으로 판단할 수 있다

    누군가 유튜브 조회수에 영향을 주는 요인이 무엇인가 묻는다면 나는 Xi라 대답할 것이다



Q : 







