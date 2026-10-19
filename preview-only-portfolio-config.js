// preview-only Portfolio 탭(pf-login)의 Firebase 설정(2026-10-19). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
// Firebase 콘솔 → 프로젝트 설정 → 내 앱(웹)의 firebaseConfig 값을 그대로 붙여 넣는다(pipeline/portfolio/SETUP.md).
// 이 값들은 원래 공개용이다(비밀 키 아님). 데이터 보호는 Firestore 규칙(pipeline/portfolio/firestore.rules)이 맡는다.
// 비어 있으면 화면이 "설정 전"으로 뜬다.
export const firebaseConfig = {
  apiKey: 'AIzaSyBD4ccaIsVJhav69KDOjkGSo2F7LJyqmLk',
  authDomain: 'stock-portfolio-15b6a.firebaseapp.com',
  projectId: 'stock-portfolio-15b6a',
  appId: '1:603634904731:web:442b93109bebc4363be03e',
};
