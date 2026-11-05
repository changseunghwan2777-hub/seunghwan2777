# Fruchter House — Rotation → Interstice / Library + Workshop

두 과제를 같은 선정 평면 R2로 연결한 결과물입니다. **과제 1은 회전에 따라 달라지는 틈을 분석하고, 과제 2는 그 차이를 작은 공공도서관·공유작업실의 활동으로 발전시킵니다.**

## 파일 안내

| 파일 | 내용 |
|---|---|
| `Project01_Rotation_Interstice_A2.pdf/svg/png` | 원형·고정 조건의 네 회전안·세 틈의 확대 분석·비교표 |
| `Project02_Library_Workshop_A2.pdf/svg/png` | 선정 평면, 선택적 해체, 새 경계·가구·프로그램·동선 |
| `Fruchter_Two_Projects_A2.pdf` | 위 두 A2 도판의 2페이지 인쇄용 합본 |
| `Library_Workshop_Editable_Plan.svg/pdf/png` | 설명·동선 표기를 뺀 편집용 프로그램 평면 |
| `*_outlined.svg` | 글자를 벡터로 바꾼 폰트 독립 버전 |
| `Rotation_Explorer.html` | R0~R3 선택, 레이어 표시, 현재 SVG 저장이 가능한 D3 비교 도구 |
| `rhino/rotation_study_rhino8.py` | Rhino 8 Python 3 ScriptEditor용 평면 곡선 생성 스크립트 |
| `rhino/rotation_ghpython.py` | Grasshopper Python 3 컴포넌트용 각도 입력 스크립트 |
| `design/` | 회전·프로그램 좌표 JSON, 설계 설명과 표현 원칙 |
| `review/` | 기하·브라우저·Rhino 문법·파일 확인 기록 |

전체 파일은 `Fruchter_Rotation_Programme_Package.zip`에 들어 있습니다. 이전 도면과 모델은 수정하지 않았습니다.

## 사용 방법

1. **인쇄:** PDF는 모두 594×420mm A2 가로형, 흰색 배경입니다. 실제 크기 100%로 인쇄하세요. 원도에 실측 치수가 없어 건축 축척은 NTS 비례 연구입니다.
2. **Illustrator:** `fonts/`의 Noto Sans KR과 Instrument Sans를 설치하고 일반 SVG를 열면 글자와 도형을 수정할 수 있습니다. 폰트 없이 열려면 `_outlined.svg`를 사용하세요. PDF의 글자는 윤곽선이므로 검색 가능한 텍스트는 아닙니다.
3. **대화형 비교:** ZIP을 푼 뒤 `Rotation_Explorer.html`을 브라우저에서 여세요. D3가 내장되어 인터넷이 없어도 동작하도록 구성했습니다. GitHub 파일 미리보기에서는 HTML 앱이 실행되지 않습니다.
4. **Rhino:** `rhino/README.md`를 확인하세요. 이 환경에는 Rhino 8이 없어 스크립트는 문법 검사만 했습니다. Rhino/Grasshopper에서 실행 검증한 파일로 표현하지 않습니다.

## 설계의 기준

공간군의 형태·면적·회전축·이격을 고정한 R0~R3 비교에서 R2를 선정했습니다. U는 기존 A의 중심 측 변 길이를 기준으로 한 상대 단위이며 미터가 아닙니다. 최단거리는 실제 통로폭과 다릅니다. 해치 면은 분석 범위이고 새로운 폐합 중앙 실내가 아닙니다.

프로그램 평면에서는 조용한 학습·열람(A), 열린 서가·모임(B), 공유작업·운영(C)을 연결합니다. 내부 칸막이 일부를 열고 서비스 경계를 추가했습니다. 문턱과 회랑은 반외부 공간이며, 외부 여지에 고정된 책이나 서가는 두지 않았습니다. 위생 기구·실제 문폭·수용 인원·구조·피난·배수는 후속 검토 사항입니다.

## 적용한 공개 스킬

- [Rhino Modeling](https://github.com/DukeYau11135/rhino-modeling-skill): 매개변수와 회전 변환, RhinoCommon/GhPython 스크립트 구조.
- [D3 Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill/blob/main/SKILL.md): 실제 D3 SVG 레이어·대안 전환·SVG 내보내기.
- [Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design): 표현 원칙, A2 편집, 선·색·해치와 글자 위계, 최종 시각 검토.

스킬 지침은 작업 저장소의 `.agents/skills/`에 적용했습니다. 공개 배포 결과물에는 실행에 필요한 글꼴과 D3 사용 허가문을 함께 넣었습니다. CAD2BIM에 의한 3D 변환은 이번 두 과제의 결과에 포함하지 않았습니다.
