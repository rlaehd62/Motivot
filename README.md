# (주)모티버스
> **초등/중등 지역사 교육을 위한 메타버스 플랫폼과 연동할 규칙 기반의 챗봇**
- **경북대학교 산학협력 프로젝트 <span style="color:orange">(팀장)</span>**
- **<span style="color:orange">한국정보처리학회 ASK 2024 게제승인 및 제1저자</span>**
- **[시작] 2024년 03월 01일**
- **[종료] 2024년 06월 09일**
> **설명 : 형식에 맞게 정제된 질의응답 데이터를 폴더에 추가하면 동작하는 방식입니다.**

## 시나리오
- **전체 사용자 : 500명**
- **동시 사용자 : 30명**
- **⚠️ 제약 조건**
  - **학생에게 정확한 역사 정보를 제공해야 한다.**
  - **내부 데이터를 쉽게 확장할 수 있어야 한다.**
  - **최소 예산으로 프로젝트를 완성해야 한다.**
> **🚩 목표 : 학생이 보낸 질문에 정확한 응답을 제공하자**

## 스택

#### Server-Side
> FastAPI, Pandas, Pytorch, KoNLPy, OpenAI

#### Infrastructure
> GCP, Docker, Nginx

## 아키텍처 
- **전체/세부 아키텍처** <br>
![전체 아키텍처](/docs/architecture1.png)
![세부 아키텍처](/docs/architecture2.png)

- **간략 배포도**
![간략 배포도](/docs/architecture3.png)
## 성능 평가
> **🚨 해당 평가는 주어진 원문과 데이터를 기반으로 수행되었음을 알립니다.**

> **💡 질문의 도메인은 메타버스 내의 위치에 따라서 변경되는 방식입니다.** 

- **챗봇 평가**
![평가1](/docs/test1.png)
![평가2](/docs/test2.png)

- **트래픽 평가**
![트래픽 평가](/docs/measurement.png)

## 트러블슈팅

#### 제악조건 문제
우리가 챗봇을 구현하기 위해서 선택한 방식은 문제가 하나 존재하였다. 데이터를 전처리를 거쳐 텐서로 변환하고 하나로 저장한다면 데이터가 늘어나고 이를 증강하였을 때, 오버헤드가 폭발적으로 생긴다는 것이었다.
제약조건과 더불어 매번 이를 검색할 때마다 수 많은 데이터를 검색하는 과정을 거쳐야만 한다. 다른 것은 감당하여도 이것만은 피해야한다고 생각하였다. 따라서 내부의 Intent Column를 기준으로 텐서를 별도 저장/로드하여 사용하도록 하여 해당 문제를 해결하였다.

#### 하드코딩 문제
초기 해당 프로젝트에서는 Column의 이름, 모델의 이름 등을 하드코딩하여 사용해왔다. 초기에는 빠른 개발을 위하여 해당 방식을 유지하였지만 어느정도 이후엔 이 문제를 해결해야겠다고 생각했다.
추후에 더 좋은 모델이 나와서 해당 모델로 교체할 수도 있고, Column의 이름, Folder의 이름 등이 다양하고 변할 수 있어야 한다고 생각하여 별도의 설정 파일을 분리하고 Hashing 방식을 통해서 해당 문제를 해결하였다.
또한 설정파일을 분리한 이유는, 이 프로그램이 나의 손을 떠나도 다른 개발자에 의해 개선되거나 운여될 것을 고려하여 설정파일을 분리한 것이다.

#### 데이터 문제
우리는 전통적인 방식으로 챗봇을 구현하였다, 사람이 질문을 추가해줘야하는 불편함이 존재하는데 이를 최소 비용으로 해결해보고자 데이터 증강을 도입하였다.
데이터를 다양한 어휘, 구조로 증강하고 이를 전처리 과정을 거쳐 사용하게 되면 올바른 질문으로 대응할 확률을 높일 수 있다고 생각하였고 이를 GPT와 연동하여 구현했다.
난 해당 과정을 자동화하지 않았는데, 이는 자동적으로 돈이 빠져나가는 등의 문제도 존재하며 선택에 따라서 증강을 수행할 수 있도록 서버에 추가하지 않았다.

## 프로젝트 후기
> **여러 제약조건으로 초기에 계획했던 RAG 챗봇을 만들지 못한 것이 다소 아쉽다. <br> 그러나 자연어 처리, 도커, 로드 밸런싱, 트래픽 평가 등의 새로운 경험이 있기에 <br> 학습 목적으로는 다소 성공적인 프로젝트라고 생각한다.**
