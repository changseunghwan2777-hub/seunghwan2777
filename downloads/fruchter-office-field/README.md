# Fruchter House — Shared Edges / 공용 오피스 반복·중첩 스터디

1106 발표자료 마지막의 정규화 M4 모듈을 반복해 발전시킨 새 작업입니다. 기존 결과물은 수정하지 않았습니다.

## 먼저 볼 파일

- `Fruchter_Shared_Office_A2.pdf`: A2 가로 7쪽. 비교 1장, 규칙 1장, figure–ground 1장, 해치 1장, 오피스 개념 평면 1장, 글자 없는 도면 2장.
- `Fruchter_Shared_Office_Editable.zip`: 전체 SVG/PDF/PNG, 2D Rhino 모델, HTML 2종, 데이터·소스·검토 기록.
- `output/Clean_Figure_Ground.png`, `output/Clean_Layered_Hatch.png`: 흰 배경 드로잉. 7016 × 4961px로 A2 약 300dpi 출력 크기입니다.
- `output/Office_Field_Explorer.html`: 9개 배열 비교와 SVG 다운로드. 내려받아 브라우저에서 열면 오프라인 작동.
- `output/Directional_Hatch_Studio.html`: 선 밀도·굵기·시드 조절 및 SVG/PNG 출력. 시드는 건축 형태를 바꾸지 않습니다.
- `output/Office_Field_2D.3dm`: 2,557개 곡선의 레이어별 2D Rhino 모델. 모든 Z=0이며 3D 건물 모델이 아닙니다.

## 핵심 선택

한 모듈은 세 날개의 합집합에서 내부 삼중 중첩을 뺀 M4 형태입니다. 이 전체를 반 간격씩 어긋난 배열로 반복합니다. 선택한 간격은 1.65u, 4열 × 3행입니다. 12개 모듈 사이에 23개 접합이 생기며, 반복 모듈 간 중첩 면적은 전체 바닥의 16.52%입니다.

기존 모듈의 중정 12개는 유지합니다. 반복으로 생긴 자연 틈은 6개입니다. 반복 모듈끼리 겹치는 영역은 실내 공유 공간으로 남깁니다. 한 모듈 안의 비움과 여러 모듈 사이의 공유를 구별하는 것이 이번 안의 핵심입니다.

`design/design-reasoning.md`에 다른 8개 대안의 비교와 선정 근거, 단위, 계산, 한계를 설명했습니다.

## 편집

`output/*.svg`는 선과 면이 벡터입니다. Illustrator에서 파일을 직접 열 수 있습니다. 텍스트가 살아 있는 기본 SVG는 동봉된 Noto Sans KR / Instrument Sans 설치 후 사용하세요. `_outlined.svg`는 글자를 외곽선으로 바꾼 버전입니다. PDF도 벡터 기반입니다.

기본 SVG의 레이어는 SVG 그룹으로 보존되며 Illustrator의 그룹/레이어 처리는 버전에 따라 다를 수 있습니다. Illustrator 자체 실행 검증은 하지 않았습니다. 출력 PDF의 페이지 크기는 594 × 420mm로 확인했습니다.

도면은 상대 단위 u를 사용하며 실치수는 정하지 않았습니다. 치수, 실제 대지·방위, 구조·설비, 수용 인원과 법규는 별도 설계가 필요합니다. 오피스 가구는 사용 예시이며 완성된 실시설계가 아닙니다.

## 이번 세션에서 설치·적용한 스킬

1. [Rhino Modeling](https://github.com/DukeYau11135/rhino-modeling-skill/blob/main/SKILL.md): 모듈 매개변수·단위·레이어, .3dm과 Rhino 8 가져오기 스크립트.
2. [Canvas Design — Anthropic](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md): 디자인 철학, A2 보드와 시각 위계, PDF/PNG 구성.
3. [D3 Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill/blob/main/SKILL.md): 실제 D3 v7 데이터 바인딩을 사용한 배열 비교·레이어 조작·SVG 저장.
4. [Algorithmic Art — Pardesco](https://github.com/Pardesco/algorithmic-art-skill/blob/main/SKILL.md): 시드 기반 해치, 템플릿 뷰어, 9개 시드 × 2회 시각 검토, 고해상도 확인.

앞의 세 스킬은 이미 로컬에 설치되어 있었고, Pardesco를 이번에 추가했습니다. `design/skills-installed.json`에 SKILL.md 해시와 설치 경로를 기록했습니다. 스킬 폴더 자체는 이 배포 묶음에 넣지 않았습니다.

## 검증 범위

기하: 중정 보존, 바닥 연결성, 동선이 바닥 밖으로 나가지 않는지 검사. 브라우저: 9개 대안·레이어 전환·SVG 내보내기·동일 시드 재현 검사. Rhino: rhino3dm으로 저장 후 다시 읽어 객체 수 확인. Rhino 데스크톱 실행은 하지 않았습니다. `review/`에 결과와 두 차례의 시각 검토 기록을 넣었습니다.

## 소스 재생성

Python 3 및 `requirements.txt` 의존성을 설치한 뒤 이 디렉터리에서 실행:

```sh
python scripts/geometry.py
python scripts/develop.py
python scripts/draw.py
python scripts/hatching.py
python scripts/boards.py
python scripts/interactive.py
python scripts/rhino_export.py
```

`Rhino8_import.py`는 Rhino 8 Python 3에서 실행하는 별도 선택 도구입니다. `design/selected.json`을 고르면 RhinoCommon으로 곡선을 불러옵니다. 브라우저 검토 스크립트는 Playwright와 `/usr/bin/chromium`을 사용합니다.

D3, 폰트 및 Pardesco 템플릿의 저작권 고지/라이선스는 `assets/`에 보존했습니다. 사용자가 제공한 발표 PDF와 참고 이미지는 이 공개 저장소에 다시 업로드하지 않았습니다.
