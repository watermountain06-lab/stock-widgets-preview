# Portfolio 탭 Firebase 설정 순서

2026-10-19. preview 전용 Portfolio 탭(나만 쓰기)을 여는 데 필요한 콘솔 설정이다. 약관 동의와 프로젝트 만들기는
사용자가 직접 한다. 무료 Spark 플랜이라 결제 수단이 필요 없다.
공개 저장소라 이 문서와 규칙 틀에는 소유자 이메일을 쓰지 않는다 — 이메일은 콘솔에서만 넣는다.

## 1. 프로젝트 만들기

1. https://console.firebase.google.com 에 Google 계정으로 들어가 **프로젝트 추가**를 누른다.
2. 이름은 아무거나 쓴다(예: `stock-portfolio`). Google 애널리틱스는 **사용 안 함**으로 둔다.

## 2. 웹 앱 등록 → 설정값 복사

1. 프로젝트 개요 화면에서 웹 아이콘(`</>`)을 누른다. 앱 별명은 `preview`로 쓰고, Firebase 호스팅은 체크하지 않는다.
   로그인에 필요한 기본 사이트를 만들라는 안내가 나오면 진행한다(화면은 계속 GitHub Pages에 둔다).
2. 화면에 나온 `firebaseConfig`의 `apiKey`, `authDomain`, `projectId`, `appId` 네 값을
   `preview-only-portfolio-config.js`에 붙여 넣는다(Claude에게 값을 보내 줘도 된다 — 공개용 값이다. 서비스 계정 비밀키와는 다르다).
3. Claude가 값을 넣고 preview에 push한다. 배포가 끝나야(몇 분) 5번 시험을 할 수 있다.

## 3. Google 로그인 켜기

1. 빌드 → **Authentication** → 시작하기 → 로그인 방법에서 **Google**을 사용 설정한다. 프로젝트 지원 이메일을 하나 고르고 저장한다.
   이 주소는 로그인 동의 화면에 개발자 연락처로 보일 수 있다 — 로그인 버튼은 공개 페이지에 있으므로 누구나 볼 수 있다.
   드러나도 괜찮은 주소를 고른다.
2. Authentication → 설정 → **승인된 도메인**에 `watermountain06-lab.github.io`를 추가한다.
   로컬(`localhost`)에서 로그인을 시험할 때만 `localhost`도 추가한다 — 최근 프로젝트에는 기본으로 들어 있지 않다.

## 4. 데이터베이스 만들기와 규칙

1. 빌드 → **Firestore Database** → 데이터베이스 만들기. 버전은 **Standard**, 데이터베이스 ID는 기본값 `(default)`
   그대로 둔다(화면 코드가 기본 데이터베이스를 쓴다). 위치는 `nam5 (us-central)` 또는 가까운 곳, **프로덕션 모드**로 시작한다(처음엔 모두 거부).
2. 규칙 탭에 `pipeline/portfolio/firestore.rules` 내용을 붙여 넣고, 콘솔 편집기에서 `OWNER_EMAIL`만 로그인할 내 Gmail 주소로
   바꾼 뒤 **게시**한다. 주소는 **소문자로** 쓴다(로그인 토큰의 이메일과 글자 그대로 비교한다). 저장소의 파일은 자리표시자 그대로 둔다.

## 5. 잠금 확인 (실제 값을 넣기 전에 반드시)

2-3의 배포가 끝난 뒤 한다.

| 확인 | 기대 |
|---|---|
| 내 계정으로 로그인 → 데이터 올리기에서 `sample.json`을 **두 번** 고르기 | "올렸습니다"가 뜨고 4구역이 가짜 데이터로 보인다 |
| 그 뒤 새로고침 | 다시 로그인 없이 같은 내용이 보인다(저장이 됐다는 확인) |
| 다른 Google 계정으로 로그인 | "이 계정은 볼 수 없습니다" |
| 로그아웃 상태 / 다른 브라우저 | 로그인 버튼만 보인다 |
| 탭을 닫고 **새 탭에 주소를 직접 입력** | 다시 로그인을 묻는다('닫은 탭 다시 열기'는 로그인을 되살릴 수 있어 시험에 쓰지 않는다) |
| Firestore → 규칙 → **규칙 플레이그라운드**: 위치 `users/<내 uid>/portfolio/main`, 읽기, 인증 안 함 | 거부 |
| 같은 위치, 인증 = 다른 uid·다른 이메일(Google 공급자) | 거부 |
| 위치 `users/<다른 uid>/portfolio/main`, 인증 = 내 uid·내 이메일 | 거부(uid 조건) |
| 같은 위치, 인증 = 내 uid·내 이메일(Google 공급자, email_verified true), 읽기와 쓰기 | 둘 다 허용 |
| 위치 `users/<다른 uid>/portfolio/main`, 인증 = 그 다른 uid·다른 이메일(자기 칸) | 거부(이메일 조건) |
| 위치 `users/<내 uid>/other/x`, 인증 = 나 | 거부(경로 조건) |
| 같은 위치(`.../portfolio/main`), 인증 = 내 uid·내 이메일이지만 email_verified false 또는 공급자가 google.com이 아님 | 거부 |

내 uid는 Authentication → 사용자 목록에서 본다. 플레이그라운드의 인증 토큰 칸 이름은 `email`, `email_verified`, `firebase.sign_in_provider`다.

## 6. 키 제한(권장, 5번을 통과한 뒤)

Google Cloud 콘솔 → API 및 서비스 → 사용자 인증 정보 → 자동 생성된 Browser key → **웹사이트 제한**에
`https://watermountain06-lab.github.io/*`와 **로그인 창 주소 `https://<projectId>.firebaseapp.com/*`**(설정값 authDomain)를 넣는다
(로컬 시험 시 `http://localhost:*/*`도). authDomain을 빼면 로그인 창이 막힌다. 키는 `firebaseConfig.apiKey`와 같은 값인지 확인한다.
API 제한 목록은 자동으로 정해진 그대로 둔다. 이 키를 다른 유료 API에 쓰지 않는다.
키가 공개되어도 데이터는 4번 규칙이 지킨다 — 이 단계는 남이 내 프로젝트 한도를 쓰는 것을 줄인다.
제한을 건 뒤 5번 첫 줄(내 계정 로그인)을 다시 한다. 로그인이 안 되면 제한을 풀고 Claude에게 오류 문구를 보낸다.
다른 Google 계정도 로그인 자체(Auth 사용자 목록에 생기는 것)는 될 수 있다. 데이터는 규칙 때문에 못 읽는다.

## 한계

- 데이터는 GitHub이 아니라 Google(Firebase)에 저장된다. 보호는 4번 규칙이 전부다 — 규칙을 바꾸면 5번을 다시 한다.
- 문서 하나에 전체 JSON을 넣는다. 파일은 900KB 이하(Firestore 문서 한도 1 MiB).
- 실제 보유·금액은 vault `finance/portfolio.md` 규칙을 바꾸기 전에는 올리지 않는다(2026-10-19 보류).
