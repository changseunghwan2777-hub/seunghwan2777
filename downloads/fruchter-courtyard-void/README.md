# Fruchter House — Expand / Overlap / Carve

사용자가 제시한 **사잇공간을 넓히는 중정**과 **중첩을 비워 만드는 중정**을 병렬로 검토한 수정안입니다. 선정안은 중첩 전체를 삭제하지 않고 실내 연결 띠를 남겨, 외부 진입 마당(E)·실내 공유 갤러리(G)·하늘에 열린 빛마당(V)을 구분했습니다. 기존 결과물은 보존했습니다.

## 결과물

| 파일 | 내용 |
|---|---|
| `Fruchter_Courtyard_Study_A2.pdf` | 아래 3개 A2 도판의 인쇄용 합본 |
| `01_Expansion_Overlap_Process_A2.pdf/svg/png` | 벌림·중첩의 각 5단계, 전부 비웠을 때의 연결 실패와 수정 |
| `02_Spatial_Comparison_A2.pdf/svg/png` | 같은 상대 축척의 대안 비교, 실내·중정 면적과 선택의 비용 |
| `03_Library_Courtyard_Plan_A2.pdf/svg/png` | 도서관·공유작업소 선정 평면, 벽·유리·문·가구·동선·개념 단면 |
| `*_outlined.svg` | 글자를 벡터 윤곽선으로 바꾼 SVG |
| `Courtyard_Explorer.html` | 원형·벌림·중첩·전체 삭제·선정안, 레이어 전환, 현재 SVG 저장 |
| `Fruchter_Courtyard_Editable_2D.3dm` | Rhino 8 형식의 편집용 2D 곡선: 원형, 벌림, 중첩, 선정안을 나란히 배치 |
| `design/design-reasoning.md` | 생성 규칙·프로그램·면적 손실·검증 범위·원본과 가설의 구분 |
| `design/study.json` | 모든 대안의 도형·벽·가구·동선과 산정 수치 |
| `scripts/` | 재생성·검증 코드 |
| `review/` | 기하·파일·브라우저·Rhino 파일 재읽기 검증 결과 |

## 열기와 편집

- PDF는 흰 바탕의 **594×420mm A2 가로형**, 100% 크기 인쇄용입니다. 실제 건축 축척은 미확정입니다.
- Illustrator에서 일반 `.svg`는 글자와 선을 수정할 수 있습니다. `assets/NotoSansKR-Study.ttf`, `assets/InstrumentSans-Regular.ttf`를 설치하세요. 글꼴 없이 열려면 `_outlined.svg`를 사용하세요. PDF의 문자는 윤곽선이므로 텍스트 검색은 되지 않습니다.
- `Courtyard_Explorer.html`을 다운로드한 뒤 브라우저에서 열면 인터넷 없이 작동합니다. GitHub 파일 미리보기에서는 앱이 실행되지 않습니다.
- `.3dm`은 실제 생성하고 재읽기한 Rhino 형식 파일입니다. 84개 유효 곡선, 31개 레이어를 확인했습니다. 모든 객체는 Z=0이며 **3D 건물 모델이 아닙니다**. Rhino 데스크톱 앱에서의 열기 검증은 하지 않았습니다. 좌표는 U 상대 단위, 문서 단위는 None입니다. 원형·벌림·중첩·선정안은 X 방향으로 5 U씩 떨어져 있습니다.
- 전체 ZIP에는 위 파일과 글꼴·D3 사용 허가문이 들어 있습니다. `manifest.json`은 ZIP 내부 파일의 SHA-256과 크기 목록입니다.

## 설계 판단

A 벌림안은 큰 공동 마당을 얻지만 외곽을 확장합니다. B 중첩안은 연결된 실내와 안쪽 빛마당을 얻지만 실내 도형 면적이 원래 세 공간군 합의 **63.2%**로 줄어듭니다. 이 비용을 숨기지 않고 도서관·공유작업소의 내부 연결을 우선하는 연구안으로 B를 선정했습니다.

회전은 A −14°, B +18°, C +10°이며 A/B의 이동량은 서로 다릅니다. U는 원본 A 안쪽 변 길이로, 미터가 아닙니다. 새 프로그램·벽·개구부·가구·중정·대지 여지는 모두 가설입니다. 도형과 동선 중심선의 충돌을 검사했으나 유효 통로폭·피난·구조·채광·배수·수용 인원은 검증하지 않았습니다. 상세 근거는 `design/design-reasoning.md`를 읽으세요.

## 사용한 공개 스킬

- [Rhino Modeling](https://github.com/DukeYau11135/rhino-modeling-skill): 설명 가능한 매개변수·곡선·레이어와 편집용 Rhino 파일 구성. 이 환경에서는 Rhino 데스크톱 대신 rhino3dm으로 네이티브 파일을 기록·검사했습니다.
- [D3 Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill/blob/main/SKILL.md): 도형 데이터 결합, 상태·레이어 전환, SVG 저장.
- [Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design): 표현 원칙, 흰 바탕 A2 도판, 선·해치·색·타이포그래피와 시각 검토.

## 재생성

Python 3.12에서 `requirements.txt`를 설치하고 `scripts/design.py`, `scripts/draw_boards.py`, `scripts/build_explorer.py`, `scripts/export_rhino.py` 순서로 실행하면 `output/`에 새 결과가 생깁니다. `source/rotation-study.json`은 이전 작업에서 이어받은 추출 좌표입니다. 변화시키려면 `design.py`의 `angles`, `TA`, `TB`, `retained_band`부터 조정하세요. 임의의 매개변수에서 모든 접합부가 자동으로 성립하는 최적화기는 아니며, 유효성 검사와 새 문·가구·동선 배치가 필요합니다.
