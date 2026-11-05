# Fruchter House — 규칙 기반 중첩 모델 연구

**다섯 배치 모델 → 아홉 반경·회전 조합 → 네 비움 정책 → 원래 외곽 재적용 → 선정안 발전**을 담았습니다. 기존 자료는 보존하고 새 연구로 추가했습니다.

우선 발전안은 **M4: 120° 간격 배치 + 세 군에 동일한 15° 회전**입니다. 한 겹은 독립 활동, 정확히 두 겹은 공유 접점, 세 겹은 하늘에 열린 중정으로 제안했습니다. 세 공유 접점이 120° 회전으로 서로 일치하는지 검사했고, 각 군의 긴 축이 중앙에 앞서 공유 접점을 만나는 순서를 확인했습니다.

## 도판과 편집 파일

| 파일 | 내용 |
|---|---|
| `Fruchter_Rule_Based_Overlap_A2.pdf` | A2 가로 도판 5장 합본 |
| `01_Overlap_Model_Families_A2.*` | M1 동심·M2 연쇄·M3 대칭 방사·M4 동일 위상·M5 둘레 순환 비교 |
| `02_Parameter_Selection_A2.*` | R 0.40/0.45/0.50u × φ 0/15/30°, 선정 근거와 비용 |
| `03_Void_Policy_And_Lineage_A2.*` | 네 삭제 규칙, 원형 외곽을 재적용한 민감도 검토 |
| `04_Overlap_Development_A2.*` | 여섯 발전 단계와 AB·BC·CA 공유 접점 확대 |
| `05_Selected_Model_Plan_A2.*` | 선정 평면·벽·개구부·가구·경로·개념 단면·입체 |
| `Overlap_Rule_Explorer.html` | 오프라인 대화형 비교와 현재 도형 SVG 저장 |
| `Fruchter_Rule_Models.3dm` | 다섯 입체 매스 + 평면 곡선 + 선정안 상세 2D 레이어 |
| `M4_Selected_Massing.obj` | 선정안의 단일 닫힌 매스 모델 |
| `design/design-reasoning.md` | 배치·삭제·프로그램 판단, 원형과 가설, 검증 범위 |
| `design/study.json` | 모든 기하·수치·벽·가구·경로 |
| `review/` | 기하·브라우저·네이티브 모델·파일 검사 기록 |

각 도판은 PDF, PNG, 일반 SVG, `_outlined.svg`로 제공합니다. 전체는 `Fruchter_Rule_Models_Package.zip`에 들어 있습니다.

## 사용 방법

- **인쇄:** 흰 바탕 594×420mm A2 가로형, 100% 인쇄. 실제 건축 축척은 미확정입니다.
- **Illustrator:** 일반 SVG는 도형과 글자를 편집할 수 있습니다. `assets/NotoSansKR-Study.ttf`, `assets/InstrumentSans-Regular.ttf`를 설치하세요. 글꼴 없이 열려면 `_outlined.svg`를 사용하세요. PDF 글자는 윤곽선입니다.
- **HTML:** 다운로드 후 브라우저로 여세요. D3가 내장되어 인터넷 없이 작동합니다. GitHub 미리보기에서는 앱이 실행되지 않습니다. 모델 메뉴의 ‘반경·회전 조합 비교’를 선택하면 R·φ 설정이 나타납니다.
- **Rhino:** `.3dm`은 Rhino 8 형식입니다. M1–M5 입체가 X축 4u 간격으로 나란히 있고 평면은 그 아래 Y=-4u에 있습니다. `M4` 레이어들이 선정안입니다. 단위는 None, 모든 수치는 상대 u입니다.
- **입체의 범위:** 실제 생성·재읽기한 닫힌 매스 메쉬입니다. 공통 높이 0.55u는 개념 가설입니다. 입체에는 문·유리·가구가 구현되지 않았고 해당 정보는 2D 레이어에 있습니다. 구조 모델·BIM이나 기존 건물의 정확한 복원이 아닙니다. Rhino 데스크톱 앱에서의 열기 검증은 하지 않았습니다.

## 반드시 구분할 설계 가정

원형의 세 군을 각각 **1.25u×0.80u 공통 모듈로 정규화**했습니다. 총면적은 유지하지만 개별 외곽·종횡비·면적은 달라집니다. `u=√[(원도 추출 A+B+C 면적)/3]`로 이전 작업의 변 길이 기준 U와 다르며 미터가 아닙니다.

원래 외곽에 같은 규칙을 재적용하면 세 접점은 유지되지만 삼중 영역은 약 82% 작아집니다. 이 차이도 도판 3에 공개했습니다. 따라서 선정안은 원형 외곽을 그대로 보존한 회전안으로 읽으면 안 됩니다.

M3는 M4보다 접점이 넓고, M5는 실내 보존에 더 유리합니다. 선택하지 않은 이유와 장점도 함께 기록했습니다. 선정은 설계 목표에 따른 판단이며 성능 최적화나 법규 검증 결과가 아닙니다. 벽·가구·동선 중심선의 교차를 확인했으나 유효 폭·피난·위생·구조·배수·채광·수용 인원은 미검증입니다.

## 적용한 공개 스킬

- [Rhino Modeling](https://github.com/DukeYau11135/rhino-modeling-skill): 설명 가능한 변수·곡선·레이어·매스의 구성. 현재 환경에서는 rhino3dm으로 네이티브 파일을 기록하고 검사했습니다.
- [D3 Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill/blob/main/SKILL.md): 모델·파라미터·레이어 비교와 SVG 저장.
- [Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design): 표현 원칙, A2 편집, 선·색·해치·글자 위계와 시각 검토.

## 재생성

Python 3.12에서 `requirements.txt`를 설치한 뒤 `scripts/design.py`, `scripts/draw.py`, `scripts/export_models.py`, `scripts/build_explorer.py`를 실행하면 `output/`에 개별 결과물이 생깁니다. `scripts/validate.py`는 기하·글자 검사입니다. `check_browser.py`에는 Playwright와 Chromium이 필요합니다. 전체 합본·ZIP은 `package_outputs.py`가 만듭니다.

변경 출발점은 `design.py`의 모듈 L/W, θ, R, φ입니다. 임의의 변경에서도 문·가구·경로가 자동 완성되는 최적화기는 아닙니다. 검사가 실패하면 접합부와 프로그램 배치를 다시 설계해야 합니다. `manifest.json`은 패키지 파일별 크기와 SHA-256입니다.
