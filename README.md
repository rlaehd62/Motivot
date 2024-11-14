<div align="center">

<!-- logo -->
<img src="https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=Motivot" width=""/>
<br/> 
<img src="https://img.shields.io/badge/프로젝트 기간-2024.03.01 ~ 2024.06.09-green?style=flat&logo=&logoColor=white" />

</div> 

## 📝 소개
 초등/중등 지역사 교육을 위한 메타버스 플랫폼과 연동할 규칙 기반의 챗봇
- 경북대학교 산학협력 프로젝트 <span style="color:orange"></span>
- <span style="color:orange">한국정보처리학회 ASK 2024 게제승인 및 제1저자</span>

<br />

## 🚀 시나리오
- 전체 사용자 : 500명
- 동시 사용자 : 30명
- ⚠️ 제약 조건
  - 학생에게 정확한 역사 정보를 제공해야 한다.
  - 내부 데이터를 쉽게 확장할 수 있어야 한다.
  - 최소 예산으로 프로젝트를 완성해야 한다.
> 🚩 목표 : 학생이 보낸 질문에 정확한 응답을 제공하자

<br />

### 💻 프로토타입
> (주)모티버의 메타버스와 연동되는 챗봇 엔진으로 실제 연동하여 사용된 사진입니다.

>  🚨멘토의 요청에 따라서 세부적인 요소는 공개하지 못함을 알립니다.

![image](https://github.com/user-attachments/assets/69e58a76-453a-4552-b3c5-2f39e5201ad8)
<br />

## ⚙ 기술 스택
### Back-End
- `Python`, `FastAPI`, `Pandas`, `Pytorch`, `KoNLPy`, `OpenAI`

### Infra
- `GCP Compute Engine`, `Docker`, `Nginx`

### Tools
- `GitHub`

<br />

## ⚙️ **기능 명세**
-   **질의응답**: Vector Search를 기반으로 사용자의 질문에 응답합니다.
-   **데이터 증강**: 내장된 질의응답 데이터의 질문을 다양한 표현으로 증강합니다.

<br />

## 🛠️ 프로젝트 아키텍쳐
- **전체/세부 아키텍처** <br>
![전체 아키텍처](/docs/architecture1.png)
![세부 아키텍처](/docs/architecture2.png)

- **간략 배포도**
![간략 배포도](/docs/architecture3.png)

<br />

## 🧪 평가
**응답 평가**
![평가1](/docs/test1.png)
![평가2](/docs/test2.png)

**트래픽 평가**
![트래픽 평가](/docs/measurement.png)

<br />

## 🤔 기술적 이슈와 해결 과정
#### 제악조건 문제
- 챗봇 구현을 위해 데이터 전처리를 거쳐 하나의 텐서로 저장하면 검색에 많은 시간이 소모된다.
- 오버헤드를 줄이고 빠른 검색을 유도하기 위하여, 각 텐서를 HashTable과 같이 각각 저장하여 해결.

#### 하드코딩 문제
- 초기 프로젝트 진행하며 모델 이름, 컬럼 등의 요소를 하드코딩으로 사용했다.
- 하드코딩 등의 리터널 사용은 가독성, 유지보수성에서 매우 좋지 않다.
- 따로 설정파일을 분리하고, 시스템에서 이를 로드하도록 변경하여 가독성, 유지보수성 개선

#### 데이터 문제
- GPU 자원, 비용 등의 문제로 전통적인 방식의 챗봇을 구현하였다.
- 사람이 수동으로 데이터를 구성해야하는 불편함이 존재한다.
- 해당 문제를 해결하기 위하여 각 질문을 패러프레이징하여 자동으로 데이터를 증강하도록 구성하였다.
- 이를 통해 더욱 다양한 질문으로 구성되어 응답 성공률을 높일 수 있을 것으로 기대한다.

#### Latency 및 Parallelism 문제
- 현재 챗봇은 코사인 유사도와 SBert 모델을 기반으로 Vector Search를 구현한다.
- GPU 자원은 존재하지 않으며 다양한 제약조건으로 GPT를 통해 RAG를 구성할 수 없는 환경이다.
- Nginx와 Docker를 통해서 수평 확장하여 부하를 분산하여 조금이라도 Latency를 줄이도록 노력하였다.
- 각 서버가 자원을 따로 점유하여 여러 개의 코어를 Time Sharing으로 동시에 잘 활용하도록 하였다.
  
<br />

## 💁‍♂️ 프로젝트 팀원
|BE/PM|Data Mining|Data Mining|
|:---:|:---:|:---:|
| <img src="https://github.com/rlaehd62.png?size=120" width="120px" /> | <img src="https://github.com/knh6110.png?size=120" width="120px" /> | <img src="https://github.com/heesdajoy.png?size=120" width="120px" /> |
|[`김동주`](https://github.com/rlaehd62)|[`김나현`](https://github.com/knh6110)|[`김다희`](https://github.com/heesdajoy)

