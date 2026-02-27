# 🎮 게임 아케이드 - 마더 PRD

## 프로젝트 개요
HTML/CSS/JS로 만든 미니 웹 게임 모음 사이트.
메인 페이지(포트 8000)에 게임 목록이 표시되고, 선택하면 해당 게임을 플레이할 수 있다.

## 프로젝트 구조
```
game-arcade/
├── PRD.md                      # 이 파일 (마더 PRD)
├── random_seed.py              # 난수 시드 생성기
├── index.html                  # 메인 페이지 (게임 목록)
├── games.json                  # 게임 레지스트리
├── logs/
│   └── [게임이름].log          # 게임별 작업 로그
├── games/
│   ├── [게임이름]/
│   │   ├── index.html          # 게임 본체 (화면 + 렌더링)
│   │   ├── game-logic.js       # 순수 로직 함수 (테스트 가능)
│   │   ├── game-logic.test.js  # 로직 유닛 테스트
│   │   ├── game-scenario.spec.js  # 플레이 시나리오 테스트 (Playwright)
│   │   └── PRD.md              # 서브 PRD (게임별 기획서)
│   └── .../
└── tests/
    └── game-test.spec.js       # Playwright 범용 테스트 (전 게임 공통)
```

## 서버 구성
- **포트 8000**: 프로덕트 서버 (검증 완료된 게임만 서비스)
  - Ralph Loop **밖에서** 별도로 실행한다: `python3 -m http.server 8000`
  - 루프가 이 서버를 관리하지 않는다. 사람이 별도 터미널에서 띄워둔다.
- **포트 38000**: 테스트 서버 (새 게임 검증용)
  - Playwright의 `webServer` 설정으로 **자동 관리**된다.
  - 테스트 시작 시 자동 실행, 테스트 종료 시 자동 종료.
  - 수동으로 관리할 필요 없다.

---

## 매 반복(iteration)마다 수행할 작업

---

### 1단계: 초기 세팅 확인
아래 항목들이 세팅되어 있는지 확인한다. 이미 완료된 항목은 건너뛴다.

#### 1-1. npm 프로젝트 및 의존성 설치
```bash
# package.json이 없으면 초기화
npm init -y

# 개발 의존성 설치
npm install --save-dev html-validate eslint @playwright/test

# Playwright 브라우저 설치 (chromium만, headless 사용)
npx playwright install --with-deps chromium
```

#### 1-2. eslint 설정 파일 생성
`.eslintrc.json`이 없으면 생성:
```json
{
  "env": {
    "browser": true,
    "node": true,
    "es2021": true
  },
  "parserOptions": {
    "ecmaVersion": 2021
  },
  "rules": {
    "no-undef": "error",
    "no-unused-vars": "warn",
    "no-unreachable": "error"
  }
}
```

#### 1-3. Playwright 설정 파일 생성
`playwright.config.js`가 없으면 생성:
```javascript
const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './',
  testMatch: ['tests/**/*.spec.js', 'games/**/*.spec.js'],
  use: {
    baseURL: 'http://localhost:38000',
    headless: true,
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'python3 -m http.server 38000',
    port: 38000,
    reuseExistingServer: true,
  },
});
```
> **참고**: `webServer` 설정으로 Playwright가 테스트 전에 자동으로 포트 38000 서버를 켜고, 테스트 후 자동으로 끈다. 수동으로 서버를 관리할 필요가 없다.

#### 1-4. 프로젝트 파일 생성
- `games.json`: 없으면 빈 배열(`[]`)로 생성
- `index.html`: 없으면 하단 "메인 페이지 요구사항"에 맞게 생성
- `tests/game-test.spec.js`: 없으면 하단 "Playwright 범용 테스트 항목"에 맞게 생성
- `logs/`: 없으면 디렉토리 생성
- `.gitignore`: 없으면 생성 (node_modules, test-results 등 제외)

```
node_modules/
test-results/
playwright-report/
```

#### 1-5. 초기 세팅 완료 확인
위 1-1 ~ 1-4가 모두 완료되었는지 확인한 후 다음 단계로 진행한다.

---

### 2단계: 시드 생성 & 기존 게임 확인
1. `python3 random_seed.py` 를 실행하여 랜덤 시드를 생성한다.
2. 출력된 JSON에서 genre, theme, mechanics 등의 제약 조건을 확인한다.
3. `games.json`을 읽고 이미 만든 게임 목록을 확인한다.
4. 기존 게임과 **이름, 장르, 핵심 메카닉이 겹치지 않는지** 확인한다.

---

### 3단계: 서브 PRD 작성
시드와 제약 조건을 기반으로 `games/[게임이름]/PRD.md` 파일을 작성한다.

**이 단계에서는 다음 페르소나를 적용한다:**

> 너는 30년 경력의 천재 게임 디자이너다.
> 닌텐도, 밸브, 슈퍼셀에서 히트작을 만든 전설적인 기획자로,
> 어떤 난수를 받아도 그 속에서 재미있는 게임 아이디어를 뽑아내는 능력이 있다.
> 시드의 문자 패턴, 숫자 배치, 반복 구조를 직감적으로 해석하여
> 장르, 테마, 메카닉 제약 조건 안에서 가장 중독성 있고 독창적인 게임을 설계한다.
> "단순하지만 깊이 있는" 게임을 최고의 가치로 여긴다.
> 3초 안에 조작법을 이해할 수 있고, 30초 만에 빠져들 수 있는 게임을 만든다.

서브 PRD에 반드시 포함할 항목:
```markdown
# [게임 이름]

## 시드 정보
- seed: (random_seed.py 출력값)
- genre: 
- theme:
- primary_mechanic:
- secondary_mechanic:
- difficulty_curve:
- visual_style:

## 게임 설명
(2~3문장으로 게임의 핵심 컨셉 설명)

## 조작법
- PC: (키보드/마우스 조작)
- 모바일: (터치 조작)

## 게임 규칙
1. (시작 조건)
2. (핵심 플레이 루프)
3. (점수 획득 방법)
4. (게임오버 조건) — **반드시 생명(HP/목숨) 시스템을 포함할 것. 최소 3개의 생명으로 시작하며, 1회 실패 시 생명이 1 감소하고 게임은 계속 진행된다. 생명이 0이 되었을 때만 게임오버.**
5. (난이도 상승 방식)

## 화면 구성
- 게임 영역: (크기, 배치)
- 점수 표시: (위치)
- 조작법 안내: (위치)
- 메인으로 돌아가기 링크: (위치)

## 비주얼 디자인
visual_style 제약 조건에 맞추되, 아래 기준을 반드시 따른다.

### 색상
- 메인 컬러 1개 + 보조 컬러 2개 + 배경색 1개로 구성되는 색상 팔레트를 정의한다.
- 색상 코드(hex)를 CSS 변수로 선언한다: `--color-primary`, `--color-secondary`, `--color-accent`, `--color-bg`
- 플레이어, 적, 아이템, 배경이 색상만으로 즉시 구분 가능해야 한다.

### 연출
- 점수 획득 시 시각적 피드백이 있어야 한다 (예: 숫자 팝업, 색 변화, 스케일 애니메이션)
- 게임오버 시 화면 전환 효과가 있어야 한다 (예: 페이드, 흔들림)
- 플레이어 조작 시 즉각적인 시각 반응이 있어야 한다 (예: 클릭/터치 시 ripple, 이동 시 잔상)
- CSS transition/animation을 적극 활용한다. requestAnimationFrame 기반 애니메이션도 권장.

### 타이포그래피 & 레이아웃
- 게임 타이틀은 크고 눈에 띄게, 점수는 항상 보이게
- 게임 영역은 화면 중앙 정렬, 최대 너비 480px
- 여백과 패딩으로 요소 간 시각적 호흡을 준다
- 버튼은 충분히 크게 (최소 44x44px, 모바일 터치 대응)

### 금지 사항
- 단색 배경 + 단색 도형만으로 구성하지 않는다 (최소한의 그라데이션이나 그림자는 적용)
- 기본 시스템 폰트만 사용하지 않는다 (Google Fonts 없이도 font-family 조합으로 분위기 낸다)
- 게임 요소가 배경과 구분이 안 되는 배색을 사용하지 않는다

### 게임 오브젝트 비주얼 (필수)
외부 이미지 파일은 사용할 수 없다. 대신 아래 기법으로 풍부한 비주얼을 구현한다:

- **인라인 SVG**: 플레이어, 적, 아이템 등 게임 오브젝트를 SVG로 직접 그린다. 단순 원/사각형이 아니라, 캐릭터나 사물의 형태가 인식 가능한 수준으로 디테일을 넣는다.
- **CSS 그라데이션/그림자**: 배경, 버튼, UI 요소에 linear-gradient, radial-gradient, box-shadow, text-shadow를 적극 활용한다.
- **CSS 애니메이션**: 유휴 상태에서도 미세한 움직임을 준다 (예: 떠다니기, 깜빡임, 회전). @keyframes를 활용.
- **이모지 활용**: 게임 테마에 맞는 이모지를 오브젝트로 활용해도 좋다 (예: 우주 테마면 🚀⭐🌍, 동물 테마면 🐱🐟🦴).
- **Canvas 드로잉**: canvas 게임의 경우, arc/bezierCurve/fillStyle gradient 등으로 오브젝트를 표현력 있게 그린다. 단순 fillRect만 사용하지 않는다.

예시 - 나쁜 비주얼:
```javascript
// ❌ 단색 사각형
ctx.fillStyle = 'red';
ctx.fillRect(x, y, 30, 30);
```

예시 - 좋은 비주얼:
```javascript
// ✅ 그라데이션 + 그림자 + 형태가 있는 오브젝트
const grad = ctx.createRadialGradient(x+15, y+15, 5, x+15, y+15, 15);
grad.addColorStop(0, '#ff6b6b');
grad.addColorStop(1, '#c92a2a');
ctx.shadowColor = 'rgba(255,0,0,0.5)';
ctx.shadowBlur = 10;
ctx.beginPath();
ctx.arc(x+15, y+15, 15, 0, Math.PI * 2);
ctx.fillStyle = grad;
ctx.fill();
```

## 필수 플레이 시나리오 테스트
게임의 핵심 메카닉이 의도대로 동작하는지 검증하기 위한 시나리오를 최소 5개 작성한다.
각 시나리오는 Playwright로 자동 수행할 수 있도록 구체적인 입력과 기대 결과를 명시한다.

### 시나리오 1: 정상 플레이
- 입력: (구체적 키 입력 시퀀스. 예: "→ → → ↑ → →")
- 기대 결과: (점수 변화, 화면 상태 등)
- 판정 기준: (어떤 DOM 요소/텍스트로 성공 여부를 확인하는가)

### 시나리오 2: 실패/게임오버 케이스
- 입력: (게임오버를 유발하는 키 입력 또는 무입력)
- 기대 결과: (게임오버 화면 표시, 점수 고정 등)
- 판정 기준: (게임오버 텍스트 또는 요소가 화면에 존재하는가)

### 시나리오 3: 점수 획득 & 난이도 상승
- 입력: (점수를 올리는 연속 플레이 입력)
- 기대 결과: (점수 증가 확인, 난이도 변화 체감 요소)
- 판정 기준: (점수 요소의 숫자가 증가했는가)

### 시나리오 4: 생명 시스템 검증 (필수)
- 입력: (1회 실패를 유발하는 입력)
- 기대 결과: 생명이 1 감소하고 게임이 **계속 진행**됨. 즉사하면 이 테스트는 실패다.
- 판정 기준: 생명 표시 요소의 숫자/아이콘이 줄었는가 + 게임오버 화면이 표시되지 않았는가
- **주의: 모든 게임은 생명 시스템이 필수이므로, 이 시나리오를 스킵할 수 없다.**

### 시나리오 5: 최소 생존 시간
- 입력: (합리적인 플레이 입력을 5초 이상 반복)
- 기대 결과: 5초 동안 게임오버가 발생하지 않음
- 판정 기준: 5초 후에도 게임오버 화면이 표시되지 않았는가

(게임 특성에 따라 시나리오를 추가해도 좋다. 배경/장식 오브젝트가 플레이어에게 피해를 주지 않는지도 검증할 것.)

## 기술 제약
- 단일 HTML 파일 (HTML + CSS + JS 인라인) + 분리된 game-logic.js
- 외부 라이브러리 사용 금지
- 모바일 터치 지원 필수
```

---

### 4단계: 서브 PRD대로 게임 코드 작성
`games/[게임이름]/PRD.md`를 읽고 아래 3개 파일을 생성한다.

#### 4-1. game-logic.js (순수 로직)
- 게임의 핵심 로직을 **순수 함수(pure function)**로 작성한다.
- DOM, canvas, 이벤트 등 브라우저 API를 사용하지 않는다.
- Node.js에서 단독 실행 가능해야 한다.
- **파일 구조는 반드시 아래 패턴을 따른다** (브라우저/Node 호환):

```javascript
// ===== 게임 로직 함수들 =====

function initGameState() { /* ... */ }
function updateState(state, input) { /* ... */ }
function checkCollision(state) { /* ... */ }
function calculateScore(state) { /* ... */ }
function isGameOver(state) { /* ... */ }

// ===== 내보내기 (Node.js 호환) =====
// 이 가드가 없으면 Node.js에서 테스트가 안 되고,
// 이 가드가 없으면 브라우저에서 에러가 난다. 반드시 넣을 것.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { initGameState, updateState, checkCollision, calculateScore, isGameOver };
}
```

> **중요**: 이 파일에는 `document`, `window`, `canvas`, `addEventListener` 등 브라우저 전용 API를 절대 사용하지 않는다. 브라우저 관련 코드는 전부 index.html에 작성한다.

#### 4-2. game-logic.test.js (유닛 테스트)
- game-logic.js의 모든 exported 함수에 대한 테스트를 작성한다.
- Node.js 내장 `assert` 또는 `node:test`를 사용한다. (외부 라이브러리 금지)
- 최소 테스트 항목:
  - `initGameState()`: 초기 상태가 올바른지
  - `updateState()`: 입력에 따라 상태가 정확히 변하는지
  - `checkCollision()`: 충돌/비충돌 케이스 각각 확인
  - `calculateScore()`: 점수가 정확히 계산되는지
  - `isGameOver()`: 게임오버 조건이 정확한지

테스트 실행: `node game-logic.test.js`

#### 4-3. game-scenario.spec.js (플레이 시나리오 테스트)
- 서브 PRD의 **"필수 플레이 시나리오 테스트"** 항목을 Playwright 테스트 코드로 변환한다.
- 각 시나리오마다:
  1. `http://localhost:38000/games/[게임이름]/index.html` 접속
  2. 서브 PRD에 정의된 키 입력 시퀀스를 전송
  3. 기대 결과를 DOM 요소/텍스트로 검증
- 이 테스트는 **게임마다 고유**하므로 범용 테스트(tests/game-test.spec.js)와 별도로 관리한다.

테스트 실행: `npx playwright test games/[게임이름]/game-scenario.spec.js`

#### 4-4. index.html (게임 본체)
- game-logic.js의 함수들을 `<script src="game-logic.js">`로 불러온다.
  - 단, 브라우저에서는 module.exports가 안 되므로 game-logic.js 상단에 아래 가드를 넣는다:
    ```javascript
    if (typeof module !== 'undefined') { module.exports = { ... }; }
    ```
- 화면 렌더링(canvas 또는 DOM), 이벤트 처리, 게임 루프를 담당한다.
- 서브 PRD에 정의된 규칙, 조작법, 화면 구성을 정확히 따른다.

코드 규격:
- **외부 라이브러리 없이** 순수 HTML/CSS/JS로 구현
- **모바일 터치 입력** 지원
- 게임 화면에 **조작법 안내** 표시
- **점수 시스템** 포함 (game-logic.js의 calculateScore 사용)
- **게임 시작/게임오버 화면** 포함 (game-logic.js의 isGameOver 사용)
- 상단 또는 하단에 **"← 메인으로 돌아가기"** 링크 포함 (href="../../index.html")

---

### 5단계: 4중 검증 (유닛테스트 → 린터 → Playwright 범용 → 시나리오 테스트)

가벼운 검증부터 무거운 검증 순서로 진행한다. 앞 단계를 통과해야 다음 단계로 넘어간다.

#### 5-1. 유닛 테스트 (로직 검증)
게임 로직이 의도대로 동작하는지 함수 단위로 검증한다.

```bash
cd games/[게임이름]
node game-logic.test.js
```

- 모든 테스트가 통과해야 다음 단계로 진행
- 실패 시 game-logic.js를 수정하고 재실행

#### 5-2. 린터 검증 (문법 검증)
코드 문법 에러를 잡는다.

1. **JS 문법 검증**: `npx eslint games/[게임이름]/game-logic.js`
2. **HTML 문법 검증**: `npx html-validate games/[게임이름]/index.html`
3. 에러가 있으면 수정 후 린터 재실행
4. **경고(warn)는 무시해도 되지만, 에러(error)는 반드시 수정**
5. 린터 통과 후 다음 단계로 진행

#### 5-3. Playwright 범용 테스트 (기본 브라우저 검증)
실제 브라우저에서 게임이 정상 작동하는지 기본 항목을 검증한다.

> 테스트 서버(포트 38000)는 playwright.config.js의 webServer 설정에 의해 자동으로 실행/종료된다.

```bash
GAME_PATH=games/[게임이름]/index.html npx playwright test tests/game-test.spec.js
```

**범용 테스트 항목:**
1. **페이지 로딩**: 게임 페이지가 정상 로딩되는가 (200 OK)
2. **JS 에러 없음**: 브라우저 콘솔에 에러(error)가 없는가
3. **게임 요소 존재**: canvas, 게임 컨테이너, 또는 주요 게임 UI 요소가 렌더링 되는가
4. **조작법 표시**: 조작법 안내 텍스트가 화면에 존재하는가
5. **메인 링크 존재**: "메인으로 돌아가기" 링크가 존재하고 클릭 가능한가
6. **키보드 반응**: 키보드 입력(방향키 또는 스페이스) 전송 시 화면에 변화가 있는가 (스크린샷 비교)
7. **점수 표시**: 점수를 표시하는 요소가 존재하는가

#### 5-4. 시나리오 테스트 (기획 의도 검증)
서브 PRD에 정의한 플레이 시나리오가 의도대로 동작하는지 검증한다.

```bash
npx playwright test games/[게임이름]/game-scenario.spec.js
```

- 이 테스트는 게임마다 고유하며, 서브 PRD의 시나리오를 그대로 자동화한 것이다.
- 예시:
  - 시나리오 1 "정상 플레이": 키 입력 → 점수 증가 확인
  - 시나리오 2 "게임오버": 충돌 유발 → 게임오버 화면 확인
  - 시나리오 3 "점수 누적": 연속 플레이 → 점수 요소 숫자 증가 확인

#### 검증 실패 시
- 에러 내용을 분석하고 **서브 PRD를 참고하여** 코드를 수정한다.
- 수정 후 **실패한 단계부터** 다시 실행한다.
  - 유닛테스트 실패 → game-logic.js 수정 → 5-1부터 재시작
  - 린터 실패 → 해당 파일 수정 → 5-2부터 재시작
  - Playwright 범용 실패 → index.html 수정 → 5-3부터 재시작
  - 시나리오 실패 → game-logic.js 또는 index.html 수정 → 5-1부터 재시작
- **3회 시도해도 같은 단계에서 실패하면** 해당 게임 폴더를 삭제하고, 2단계부터 새 게임으로 다시 시작한다.

---

### 6단계: 프로덕트에 등록
테스트 통과 후:

1. `games.json`에 새 게임 정보를 추가한다:
```json
{
  "id": "게임-폴더명",
  "name": "게임 이름 (한글)",
  "description": "한 줄 설명",
  "genre": "장르",
  "theme": "테마",
  "path": "games/[게임이름]/index.html",
  "seed": "시드값",
  "addedAt": "2026-02-27"
}
```

2. `index.html` 메인 페이지를 갱신하여 새 게임 카드를 추가한다.

---

### 7단계: 로그 기록
매 iteration의 결과를 `logs/[게임이름].log` 에 기록한다. 게임 실패로 폴더를 삭제한 경우에도 로그는 남긴다.

로그 형식:
```
========================================
Game: [게임이름]
Seed: [시드값]
Timestamp: [현재 시각]
Status: SUCCESS / FAILED
========================================

[1] Seed Generated
    genre: ...
    theme: ...
    primary_mechanic: ...

[2] Sub PRD Created
    path: games/[게임이름]/PRD.md

[3] Code Generated
    files: game-logic.js, game-logic.test.js, game-scenario.spec.js, index.html

[4] Validation Results
    4-1. Unit Test:      PASS / FAIL (에러 메시지)
    4-2. Linter:         PASS / FAIL (에러 메시지)
    4-3. Playwright:     PASS / FAIL (에러 메시지)
    4-4. Scenario Test:  PASS / FAIL (에러 메시지)
    Retry Count: 0/3

[5] Registration
    Added to games.json: YES / NO
    Updated index.html: YES / NO

[6] Notes
    (실패 사유, 특이사항, 포기한 경우 이유 등 자유 기술)
========================================
```

> **중요**: 게임이 실패하여 폴더를 삭제하는 경우에도, 실패 로그는 반드시 남긴다. 이 로그가 있어야 나중에 어떤 게임이 왜 실패했는지 추적할 수 있다.

---

### 8단계: 완료 신호
위 과정이 모두 정상 완료되면 `<promise>DONE</promise>`을 출력한다.

---

## 메인 페이지(index.html) 요구사항
- 깔끔한 카드 레이아웃으로 게임 목록 표시
- 각 카드에 게임 이름, 설명, 장르, 테마 표시
- 카드 클릭 시 해당 게임 페이지로 이동
- `games.json`을 fetch하여 동적으로 목록 생성
- 게임이 0개일 때 "아직 게임이 없습니다" 안내 표시
- 모바일 반응형 디자인
- 상단에 "🎮 게임 아케이드" 타이틀

---

## 제약 조건
- 모든 게임은 **index.html + game-logic.js** 로 구성 (+ 테스트 파일들)
- **외부 CDN, 라이브러리 사용 금지** (순수 HTML/CSS/JS)
- 게임 하나당 **하나의 iteration**에서 완료
- 이전 게임의 코드를 수정하지 않는다 (새 게임만 추가)
- 서브 PRD에 정의된 내용을 코드에 정확히 반영한다
- game-logic.js에는 브라우저 API를 절대 사용하지 않는다
- 게임 폴더명은 영문 소문자와 하이픈만 사용한다 (예: `space-dodge`, `color-match`)
- **언어 규칙**: 코드 주석, 변수명, 서브 PRD는 모두 **영어**로 작성한다. 단, 게임의 유저 대면 텍스트(UI, 조작법 안내, 게임오버 메시지 등)는 **한글**로 작성한다.

## 안전장치
- `--max-iterations`으로 최대 반복 횟수 제한
- 린터/테스트 3회 연속 실패 시 해당 게임 포기하고 새 시드로 재시작
- 무한루프 방지: 같은 게임 이름을 두 번 시도하지 않는다
- games.json에 이미 있는 장르+테마 조합은 피한다
- 포트 38000은 Playwright가 자동 관리하므로 수동으로 서버를 조작하지 않는다
- 게임 폴더 삭제 시 `rm -rf games/[게임이름]` 후 games.json에서도 해당 항목을 제거한다 (존재하는 경우)