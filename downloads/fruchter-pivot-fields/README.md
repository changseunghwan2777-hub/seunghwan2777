# Moving Centres — Fruchter House / 독립 중심과 연속 회전

기존의 흑백 면·방향별 해치 표현을 유지하고, 동일한 복사 배열을 20개의 독립 중심과 회전각을 가진 배치로 발전시킨 결과입니다. 기존 파일은 수정하지 않았습니다.

## 결과물

- **Fruchter_Moving_Centres_A2.pdf**: A2 가로 7쪽. 9개 대안 비교, 생성 규칙과 각도표, figure–ground, 방향 해치, 접합 확대도, 글자 없는 드로잉 2쪽.
- **Fruchter_Moving_Centres_Editable.zip**: SVG·PDF·PNG·2D Rhino 모델·HTML·데이터·소스·검토 기록.
- `output/Clean_Organic_Figure_Ground.png`, `output/Clean_Organic_Hatch.png`: 흰 배경 7016 × 4961px, A2 약 300dpi 크기.
- `output/Moving_Centres_Explorer.html`: 9개 규칙/강도 비교, 중심·각도와 이동 궤적 확인, SVG 저장. 내려받아 브라우저에서 열면 오프라인 사용 가능.
- `output/Directional_Hatch_Studio.html`: 해치 시드·밀도·굵기 조절, SVG/PNG 저장. seed=42가 기본이며 seed=3, 7도 동일한 건축 형상에 미세한 선 변화만 줍니다.
- `output/Moving_Centres_2D.3dm`: 4,378개 곡선의 레이어별 2D 모델. 모든 Z=0. 3D 건물 모델이 아닙니다.
- `design/pivots-and-angles.csv`: 모듈별 초기 위치, 이동한 회전 중심, 회전각.

## 설계의 핵심

세 날개가 합쳐진 M4 전체를 하나의 모듈 U로 유지합니다. 두 제어점의 반대 회전 영향을 거리에 따라 합성해 20개의 개별 중심 P를 이동시키고, 각 P에서 U를 −39.6°~+39.6°로 회전합니다. 두 제어점은 실제 모듈 회전축이 아닙니다.

39개 접합 중 가는 7개를 주요 연결에서 제외해도 나머지 32개로 모든 모듈이 연결됩니다. 중정 20개를 보존하며, 이웃 바닥이 침범하는 3곳은 최종 바닥에서 해당 부분을 제거했습니다. 강체 원형과 최종 잘린 바닥을 구별해 기록했습니다.

상세한 비교 근거·계산식·용도 해석은 `design/design-reasoning.md`에 있습니다. u는 상대 단위이며 원본 주택의 실치수가 아닙니다. 이번 수정은 배치·중첩과 공용 오피스의 공간 관계에 대한 개념 설계입니다. 가구·설비·피난 계획은 아직 확정하지 않았습니다.

## 편집

기본 SVG는 텍스트가 살아 있습니다. 동봉된 Noto Sans KR / Instrument Sans를 설치한 뒤 Illustrator에서 여세요. `_outlined.svg`는 글자를 외곽선으로 바꾼 버전입니다. 선·면은 벡터이며 레이어 역할의 그룹으로 분리했습니다. Illustrator의 그룹/레이어 처리는 버전에 따라 다를 수 있습니다. Illustrator 직접 실행 검증은 하지 않았습니다.

PDF는 전 페이지 594 × 420mm로 확인했습니다. Rhino 파일은 rhino3dm으로 저장 후 다시 읽어 객체 수를 검사했습니다. Rhino 데스크톱 직접 실행 검증은 하지 않았습니다.

## 적용한 스킬

이전 세션에서 설치한 네 스킬을 이어서 적용했습니다.

- [Rhino Modeling](https://github.com/DukeYau11135/rhino-modeling-skill/blob/main/SKILL.md): 강체 변환·상대 단위·레이어별 2D 모델.
- [Canvas Design — Anthropic](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md): 흑백 표현 유지, A2 보드의 시각 위계.
- [D3 Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill/blob/main/SKILL.md): 규칙 비교와 모듈 중심·각도 인터랙션.
- [Algorithmic Art — Pardesco](https://github.com/Pardesco/algorithmic-art-skill/blob/main/SKILL.md): 방향별 선 생성, 9개 시드 × 2회 시각 검토, 4배 출력 확인.

폰트·D3·Pardesco 템플릿의 저작권 고지를 assets에 보존했습니다. 사용자 발표 PDF와 참고 이미지는 공개 저장소에 재업로드하지 않았습니다.

## 재생성

Python 3과 requirements.txt를 설치한 뒤 아래 순서로 실행합니다. 의존성은 기존 도구 환경에서 사용한 버전입니다.

```sh
python scripts/fields.py
python scripts/selected.py
python scripts/draw.py
python scripts/hatching.py
python scripts/boards.py
python scripts/interactive.py
python scripts/rhino_export.py
python scripts/verify_geometry.py
python scripts/print_exports.py
```

review에는 기하 검사, 브라우저 검사, 시각 검토와 9개 시드 비교 이미지가 있습니다. 검토 스크립트는 별도로 Playwright와 /usr/bin/chromium을 사용합니다.
